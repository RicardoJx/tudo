import glob, os
from PIL import Image
from modles.users import Post,session,User

def get_images(path):
    os.chdir('static')
    fs = glob.glob(path + '/*.jpg')
    os.chdir('..')
    return fs


def make_thumb(path):
    im = Image.open(path)
    im.thumbnail((200,200))
    name = os.path.basename(path)
    filename,ext = os.path.splitext(name)
    im.save('static/uploads/thumbs/{}_{}x{}{}'.format(
        filename,200,200,ext
    ),'JPEG')

def add_post(username,image_url):
    user=session.query(User).filter_by(name=username).first()
    post=Post(image_url=image_url,user_id=user.id)
    session.add(post)
    session.commit()

def get_posts():
    posts = session.query(Post).all()
    return posts

def get_post(post_id):
    post=session.query(Post).filter_by(id=post_id).scalar()
    return post
