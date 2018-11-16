from PIL import Image
import os

def save_upload(name, content):
    with open('static/uploads/{}'.format(name),'wb') as f:
        f.write(content)

def make_thumb(name,size):
    """

    :param name:   保存图片的名字
    :param size:    一个长和宽的元组.
    :return:
    """
    file, ext = os.path.splitext(name)
    im = Image.open('static/uploads/{}'.format(name))
    im.thumbnail(size)
    im.save("static/uploads/thumbs/{}_{}x{}.jpg".format(file, size[0],size[1],"JPEG"))


