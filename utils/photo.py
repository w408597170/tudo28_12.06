from PIL import Image
import os
import uuid

# def save_upload(name, content):
#     """
#     保存图片内容到文件.
#     :param name:
#     :param content:
#     :return:
#     """
#     with open('static/uploads/{}'.format(name),'wb') as f:
#         f.write(content)
#     return 'uploads/{}'.format(name)
#
#
# def make_thumb(name,size):
#     """
#
#     :param name:   保存图片的名字
#     :param size:    一个长和宽的元组.
#     :return:
#     """
#     file, ext = os.path.splitext(name)
#     im = Image.open('static/uploads/{}'.format(name))
#     im.thumbnail(size)
#     url = "uploads/thumbs/{}_{}x{}.jpg".format(file, size[0],size[1])
#     im.save("static/{}".format(url), "JPEG")
#
#     return url

class UploadImageSave(object):
    """
    辅助保存用户上传的图片,生成缩略图,保存图片相关url 用来存到数据库.
    """
    upload_dir = 'uploads'
    thumb_dir = 'thumbs'
    size = (200,200)

    def __init__(self, static_path, name):
        self.static_path = static_path
        self.name = name
        self.new_name = self.gen_new_name()

    def gen_new_name(self):
        """
        生成一个随机的唯一字符串,并用来作为图片的名字.
        :return:
        """

        _, ext = os.path.splitext(self.name)    #_ 可以看作一个临时变量 .
        return uuid.uuid4().hex + ext


    @property   #把方法当成属性来调用.
    def image_url(self):
        """
        生成用来保存图片相对路径的 url.
        :return:
        """
        return os.path.join(self.upload_dir, self.new_name)

    @property
    def upload_path(self):
        return os.path.join(self.static_path, self.image_url)


    def save_upload(self, content):
        """
        保存图片内容到文件.
        :param name:
        :param content:
        :return:
        """
        with open(self.upload_path,'wb') as f:
            f.write(content)

    @property
    def thumb_url(self):
        filename, ext = os.path.splitext(self.new_name)
        thumb_name = '{}_{}x{}'.format(filename, self.size[0], self.size[1]) + ext
        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)


    def make_thumb(self):
        """
        生成指定大小(size)的缩略图.
        """

        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        save_thumb_to = os.path.join(self.static_path, self.thumb_url)
        im.save(save_thumb_to, "JPEG")

