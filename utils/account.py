
import hashlib

from models.account import User, session, Post, Like

def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()

# USER_DATA = {
#     "name": 'simon',
#     "password": hashed('123')
#
# }



def authenticate(username, password):
    """
    校验用户名和密码是否符合记录.
    :param username:
    :param password:
    :return: True 代表验证通过, False 代表验证失败.
    """
    print(username, password)
    if username and password:
        # return username == username and hashed(password) == hashed(password)
        hashed_password = User.get_password(username)
        return hashed(password) == hashed_password  #验证表单和数据库是否一样.
    else:
        return False


def register(username, password):
    """
    注册用户,增加用户信息到数据库
    :param username:
    :param password:
    :return:
    """
    if not User.is_exists(username):
        User.add_user(username, hashed(password))
        return {'msg': 'ok'}
    else:
        return {'msg':'用户名已存在,请重新注册. '}


def add_post_for(username, image_url, thumb_url):
    """
    保存用户上传的图片信息.
    :param username:
    :param image_url:
    :param thumb_url:
    :return:
    """

    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
    session.add(post)
    session.commit()
    return post

def get_post_for(username):
    """
    获取用户上传的图片.
    :param username:
    :return:
    """
    user = session.query(User).filter_by(name=username).first()
    if user:
        return user.posts   #反向查询.
    else:
        return []

def get_post(post_id):
    """
    获取指定 id 的 post 对象.
    :param post_id:
    :return:
    """
    post = session.query(Post).filter_by(id=post_id).scalar()
    return post

def get_all_post(): #获取所有缩略图.
    posts = session.query(Post).order_by(Post.id.desc()).all()
    return posts

def get_user(username):
    user = session.query(User).filter_by(name=username).first()
    return user


def get_like_posts(user):   #获取用户喜欢的图片.
    if user:

        posts = session.query(Post).filter(Like.user_id == user.id,
                                       Post.id == Like.post_id,Post.id != user.id).all()
    else:
        posts = []

    return posts


def get_like_count(post):   #获取喜欢一张图片的用户数.
    count = session.query(Like).filter_by(post_id=post.id).count()
    return count