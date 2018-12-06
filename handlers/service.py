import tornado.web
import tornado.gen
import tornado.escape
from tornado.httpclient import AsyncHTTPClient
import requests


from utils.account import add_post_for
from .main import AuthBaseHandler
from utils.photo import UploadImageSave
from .chat import ChatSocketHandler, make_chat

class URLSaveHandler(AuthBaseHandler):
    """
    实现保存指定URL 的图片功能 同步版本 /sync
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        url = self.get_argument('save_url','')

        resp = requests.get(url)
        ims = UploadImageSave(self.settings['static_path'],'x.jpg')
        ims.save_upload(resp.content)
        ims.make_thumb()

        post = add_post_for(self.current_user, ims.image_url, ims.thumb_url)
        self.redirect('/post/{}'.format(post.id))


class AsyncURLSaveHanlder(AuthBaseHandler):
    """
    实现保存指定 URL 的图片功能,异步版本 /save?url=xxx
    """
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        url = self.get_argument('save_url','')
        is_from_room = self.get_argument('from', '') == 'room'
        user = self.get_argument('user','')
        if not (is_from_room and user):
            self.write('wrong call')
            return
        client = AsyncHTTPClient()

        resp = yield client.fetch(url)
        ims = UploadImageSave(self.settings['static_path'],'x.jpg')
        ims.save_upload(resp.body)
        ims.make_thumb()

        post = add_post_for(user, ims.image_url, ims.thumb_url)
        chat = make_chat('{} post new image:http://192.168.2.250:8080/post/{} '.format(user, post.id),img_url=post.thumb_url)
        # self.write(str(post.id))
        msg = {
            'html':tornado.escape.to_basestring(
                self.render_string('message.html', message=chat,)
            ),
            'id':chat['id'],
        }

        ChatSocketHandler.update_history(msg)
        ChatSocketHandler.send_updates(msg)
