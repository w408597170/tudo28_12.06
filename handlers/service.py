import tornado.web
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
import requests

from utils.account import add_post_for
from .main import AuthBaseHandler
from utils.photo import UploadImageSave


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

        self.write(str(post.id))