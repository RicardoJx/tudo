import uuid
import os
from PIL import Image
from modles.users import Post,session,User,Like


class UploadImage(object):
    upload_dir='uploads'
    thumb_dir='thumbs'
    thumb_size=(200,200)

    def __init__(self,static_path,upload_name):
        self.static_path=static_path
        self.upload_name=upload_name
        self.name = self.gen_name

    @property
    def gen_name(self):
        _,ext=os.path.splitext(self.upload_name)
        return uuid.uuid4().hex + ext


    @property
    def save_to(self):
        return os.path.join(self.static_path,self.upload_url)

    def save_upload(self,content):
        with open(self.save_to,'wb') as f:
            f.write(content)

    @property
    def upload_url(self):
        return os.path.join(self.upload_dir,self.name)

    def make_thumb(self):
        im = Image.open(self.save_to)
        im.thumbnail(self.thumb_size)
        im.save(os.path.join(self.static_path,self.thumb_url),'JPEG')

    @property
    def thumb_url(self):
        filename, ext=os.path.splitext(self.name)
        return os.path.join(self.upload_dir,
                            self.thumb_dir,
                            '{}_{}x{}{}'.format(
                                filename,
                                self.thumb_size[0],
                                self.thumb_size[1],
                                ext))


def add_post(username,image_url,thumb_url):
    user=session.query(User).filter_by(name=username).first()
    post=Post(image_url=image_url,thumb_url=thumb_url,user_id=user.id)
    session.add(post)
    session.commit()

def get_posts():
    posts = session.query(Post).all()
    return posts

def get_posts_for(username):
    user=session.query(User).filter_by(name=username).scalar()
    return user.posts


def get_post(post_id):
    post=session.query(Post).filter_by(id=post_id).scalar()
    return post

def get_like_posts(user_id):
    return session.query(Post).filter(Like.user_id==user_id,
                                      Post.id==Like.post_id,
                                      Post.user_id!=user_id).all()

def get_like_users(post_id):
    return session.query(User).filter(Like.post_id==post_id,
                                      User.id==Like.user_id).all()