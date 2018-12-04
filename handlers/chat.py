import uuid

import tornado.escape
import tornado.websocket
import tornado.web
import tornado.httpclient
import tornado.gen
from pycket.session import SessionMixin

from .main import AuthBaseHandler
from utils.account import add_post_for
from utils.photo import UploadImageSave

class RoomHandler(AuthBaseHandler):
    """
    聊天室页面.
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        print("new connection: %s" % self)
        self.render('room.html', messages=ChatSocketHandler.history)


class ChatSocketHandler(tornado.websocket.WebSocketHandler,SessionMixin):
    """
    处理响应 websocket 的链接
    """
    waiters = set() #等待接收信息的用户
    history = []    #历史消息.
    history_size = 200   #限制历史消息列表大小.

    def get_current_user(self):
        return self.session.get('simon_user_info', None)


    def open(self, *args, **kwargs):
        """
        新的 websocket 连接打开,自动调用.

        """
        print("new ws connection: %s" % self)
        ChatSocketHandler.waiters.add(self)


    def on_close(self):
         """websocket 连接断开,自动调用"""
         print("close ws connection: %s" % self)
         ChatSocketHandler.waiters.remove(self)

    @tornado.gen.coroutine
    def on_message(self, message):
        """websocket 服务端接收到消息,自动调用"""

        print("got message: %s" % message)
        parsed = tornado.escape.json_decode(message)
        body = parsed['body']
        if body and body.startswith('http://'):
            client = tornado.httpclient.AsyncHTTPClient()
            # save_api_url = "http://192.168.2.250:8080/save?save_url={}&user={}&from=room".format(body, self.current_user)

            resp = yield client.fetch(body)
            ims = UploadImageSave(self.settings['static_path'], 'x.jpg')
            ims.save_upload(resp.body)
            ims.make_thumb()
            post = add_post_for(self.current_user, ims.image_url, ims.thumb_url)

            # post_id = resp.body.decode('utf-8')


            body = "http://192.168.2.250:8080/post/{}".format(post.id)

        chat = {
            'id':str(uuid.uuid4()),
            'body':body,
        }

        msg = {
            'html':tornado.escape.to_basestring(
                self.render_string('message.html', message=chat,user=self.current_user)
            ),
            'id':chat['id']
        }

        ChatSocketHandler.update_history(msg)
        ChatSocketHandler.send_updates(msg)

    @classmethod
    def send_updates(cls,msg):
        """给每个等待接收的用户发新的消息."""

        for w in ChatSocketHandler.waiters:
            w.write_message(msg)


    @classmethod
    def update_history(cls, msg):
        """更新消息列表,加入新的(历史)消息"""
        cls.history.append(msg)
        if len(cls.history) > cls.history_size:
            cls.history = cls.history[-cls.history_size]