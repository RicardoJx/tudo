import tornado.web
from pycket.session import SessionMixin
from utils import photo


class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user',None)


class IndexHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        posts = photo.get_posts()
        self.render('index.html',posts=posts)


class ExploreHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        urls=photo.get_images('uploads/thumbs')
        self.render('explore.html',urls=urls)


class PostHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self,post_id):
        post=photo.get_post(post_id)
        self.render('post.html',post=post)


class UploadHandler(AuthBaseHandler):
    @tornado.web.authenticated
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
            photo.add_post(self.current_user,save_to)
            photo.make_thumb(save_to)
            self.redirect('/explore')