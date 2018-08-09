import tornado.web
from pycket.session import SessionMixin
from utils import photo


class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user',None)


class IndexHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    def get(self):
        urls=photo.get_images('uploads/thumbs')
        self.render('explore.html',urls=urls)


class PostHandler(tornado.web.RequestHandler):
    def get(self,post_id):
        self.render('post.html',post_id=post_id)


class UploadHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg',None)
        for img in img_files:
            print("got {}".format(img['filename']))
            save_to = 'static/uploads/{}'.format(img['filename'])
            with open(save_to, 'wb') as f:
                f.write(img['body'])
                print(f)
            photo.make_thumb(save_to)
            self.redirect('/explore')