from PIL import Image
import os

def save_upload(name, content):
    """
    保存图片内容到文件.
    :param name:
    :param content:
    :return:
    """
    with open('static/uploads/{}'.format(name),'wb') as f:
        f.write(content)
    return 'uploads/{}'.format(name)


def make_thumb(name,size):
    """

    :param name:   保存图片的名字
    :param size:    一个长和宽的元组.
    :return:
    """
    file, ext = os.path.splitext(name)
    im = Image.open('static/uploads/{}'.format(name))
    im.thumbnail(size)
    url = "uploads/thumbs/{}_{}x{}.jpg".format(file, size[0],size[1])
    im.save("static/{}".format(url), "JPEG")

    return url

# class UploadImageSave(object):
#     """
#     辅助保存用户上传的图片,生成缩略图,保存图片相关url 用来存到数据库.
#     """
#     upload_dir = 'uploads'
#
#     def __init__(self, static_path, name):
#         self.static_path = static_path
#         self.name = name
#
#     @property
#     def upload_url(self):
#         """
#         生成用来保存图片相对路径的 url.
#         :return:
#         """
#         return os.path.join(self.upload_dir, self.name)
#
#     @property
#     def upload_path(self):
#         return os.path.join(self.static_path, self.name)


