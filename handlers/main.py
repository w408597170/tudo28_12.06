import tornado.web
import glob
import os
import photo


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        names = glob.glob('static/uploads/*.jpg')
        self.render('explore.html',names=names)


class PostHandler(tornado.web.RequestHandler):
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
            photo.save_upload(name,content)
            photo.make_thumb(name,(200, 200))
        self.write('upload done')
