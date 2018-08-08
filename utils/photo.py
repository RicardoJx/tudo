import glob, os
from PIL import Image

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