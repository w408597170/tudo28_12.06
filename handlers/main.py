import tornado.web
# import glob

from pycket.session import SessionMixin

from utils.photo import  UploadImageSave
from utils.account import add_post_for, get_post_for, get_post, get_all_post


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
        # names = glob.glob('static/uploads/*.jpg')
        posts = get_post_for(self.current_user)
        self.render('index.html',posts=posts)


class ExploreHandler(AuthBaseHandler):
    """
    发现页,最新上传的图片.
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        # names = glob.glob('static/uploads/thumbs/*.jpg')
        posts = get_all_post()
        self.render('explore.html',posts=posts)


class PostHandler(tornado.web.RequestHandler):
    """
    单个图片的详情页.
    """
    def get(self, *args, **kwargs):

        post = get_post(kwargs['post_id'])
        if post:

            # self.render('post.html',post_id = kwargs['post_id'])
            self.render('post.html',post=post)
        else:
            self.write('post id {} is wrong'.format(kwargs['post_id']))

class UploadHandler(AuthBaseHandler):
    '提供表单和和处理上传的图片.'


    @tornado.web.authenticated  #验证用户是否登陆,如果没有提示登陆.
    def get(self,*args,**kwargs):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self,*args,**kwargs):
        file_list = self.request.files.get('newimg', None)
        post_id = 0
        for upload in file_list:
            name = upload['filename']
            content = upload['body']
            # with open('static/uploads/{}'.format(name), 'wb') as f:
            #     f.write(content)
            imgsave = UploadImageSave(self.settings['static_path'], name)
            imgsave.save_upload(content)
            imgsave.make_thumb()

            post = add_post_for(self.current_user, imgsave.image_url, imgsave.thumb_url)
            post_id = post.id



        self.redirect('/post/{}'.format(post_id))   #上传完成后跳转到图片详情页.
