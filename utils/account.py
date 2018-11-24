
import hashlib

from models.account import User

def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()

USER_DATA = {
    "name": 'simon',
    "password": hashed('123')

}



def authenticate(username, password):
    """
    校验用户名和密码是否符合记录.
    :param username:
    :param password:
    :return: True 代表验证通过, False 代表验证失败.
    """
    print(username, password)
    if username and password:
        return username == username and hashed(password) == hashed(password)

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

