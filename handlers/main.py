import tornado.web
import glob

from pycket.session import SessionMixin

from utils.photo import save_upload, make_thumb


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    """
    基础的认证 handler
    """
    def get_current_user(self):
        return self.session.get('simon_user_info', None)




class IndexHandler(AuthBaseHandler):
    """
    首页,显示用户关注的图片流.
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        names = glob.glob('static/uploads/*.jpg')
        self.render('index.html',names=names)


class ExploreHandler(AuthBaseHandler):
    """
    发现页,最新上传的图片.
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        names = glob.glob('static/uploads/thumbs/*.jpg')
        self.render('explore.html',names=names)


class PostHandler(tornado.web.RequestHandler):
    """
    单个图片的详情页.
    """
    def get(self, *args, **kwargs):
        self.render('post.html',post_id = kwargs['post_id'])
        

class UploadHandler(tornado.web.RequestHandler):
    '提供表单和和处理上传的图片.'
    def get(self,*args,**kwargs):
        self.render('upload.html')

    def post(self,*args,**kwargs):
        file_list = self.request.files.get('newimg', None)
        for upload in file_list:
            name = upload['filename']
            content = upload['body']
            # with open('static/uploads/{}'.format(name), 'wb') as f:
            #     f.write(content)
            save_upload(name,content)
            make_thumb(name,(200, 200))
        self.write('upload done')
