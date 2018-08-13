import hashlib
from modles.users import User,session


def hashed(text):
    return hashlib.md5(text.encode()).hexdigest()


def authenticate(username,password):
    if username and password:
        hash_pass=User.get_pass(username)
        return hash_pass and hash_pass==hashed(password)
    else:
        return False

def register(username,password):
    if User.is_exists(username):
        return {'msg':'username is exists'}
    else:
        User.add_user(username,hashed(password))
        return {'msg':'ok'}

def get_user(username):
    user=session.query(User).filter_by(name=username).first()
    return user