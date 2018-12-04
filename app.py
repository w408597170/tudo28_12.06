import tornado.ioloop  #io事件循环
import tornado.web  #web服务器
import tornado.options  #命令行解析模块,让模块定义自己的选项.
from tornado.options import define,options


from handlers import main, auth, chat, service

define('port',default=8080,help='run port',type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
            (r'/upload', main.UploadHandler),
            (r'/profile', main.ProfileHandler),
            (r'/login', auth.LoginHandler),
            (r'/logout', auth.LogoutHandler),
            (r'/signup', auth.SignupHandler),
            (r'/room', chat.RoomHandler),
            (r'/ws', chat.ChatSocketHandler),
            (r'/sync', service.URLSaveHandler),
            (r'/save', service.URLSaveHandler),
        ]
        settings = dict(
            template_path = 'templates',    #设置模板路径.
            debug=True,  #开启调试模式,代码有修改的时候自动重启服务,生产者模式切记不能开启.
            static_path='static',
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': '192.168.2.250',
                    'port': 6379,
                    # 'password': '',
                    'db_sessions': 5,  # redis db index
                    'db_notifications': 11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                },
            },
            cookie_secret = 'sdlkmjinklsjdlfkj',
            login_url = '/login',

        )

        super(Application,self).__init__(handlers,**settings)



application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()