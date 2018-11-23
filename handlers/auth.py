import tornado.web


from pycket.session import SessionMixin

from utils.account import authenticate, register
from .main import AuthBaseHandler

class LoginHandler(tornado.web.RequestHandler, SessionMixin):
    """
    登录接口
    """
    def get(self, *args, **kwargs):
        next = self.get_argument('next', '/')
        self.render('login.html',nextname = next) # 获取next并跳转路由.

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        next = self.get_argument('next', '/')   #路由跳转.
        if authenticate(username, password):
            self.session.set('simon_user_info', username)
            self.redirect(next)
        else:
            self.write('fail')


class LogoutHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.session.delete('simon_user_info')






class SignupHandler(AuthBaseHandler):
    """
    注册创建用户
    """
    def get(self, *args, **kwargs):
        self.render('signup.html', msg = '')

    def post(self, *args, **kwargs):
        name = self.get_argument('username', None)
        password1 = self.get_argument('password1', None)
        password2 = self.get_argument('password2', None)

        msg = ''

        if name and password1 and password2:
            if password1 == password2:
                ret = register(name, password1)
                if ret['msg'] == 'ok':  #如果注册成功,跳转到首页.
                    self.session.set('simon_user_info', name)
                    self.redirect('/')
                else:
                    msg = ret['msg']
            else:
                msg = 'password 不同,请重新输入.'

        else:
            msg = '帐号或者密码不能为空.'

        self.render('signup.html', msg=msg)