import tornado.ioloop  #io事件循环
import tornado.web  #web服务器
import tornado.options  #命令行解析模块,让模块定义自己的选项.
from tornado.options import define,options

from handlers import main

define('port',default=8083,help='run port',type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', main.IndexHandler),
            (r'/explore', main.ExploreHandler),
            (r'/post/(?P<post_id>[0-9]+)', main.PostHandler),
        ]
        settings = dict(
            template_path = 'templates',    #设置模板路径.
            debug=True,  #开启调试模式,代码有修改的时候自动重启服务,生产者模式切记不能开启.
            static_path='static'

        )

        super(Application,self).__init__(handlers,**settings)



application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()