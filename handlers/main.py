import tornado.web
from pycket.session import SessionMixin
from utils import photo
from utils.account import get_user


class AuthBaseHandler(tornado.web.RequestHandler,SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user',None)


class IndexHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        posts = photo.get_posts_for(self.current_user)
        self.render('index.html',posts=posts)


class ExploreHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        posts=photo.get_posts()
        self.render('explore.html',posts=posts)


class ProfileHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self):
        name=self.get_argument('name',None)
        if not name:
            name=self.current_user
        user=get_user(name)
        if not user:
            self.set_status(404)
            self.write('name出错了')
        else:
            like_posts=photo.get_like_posts(user.id)
            self.render('profile.html',user=user,like_posts=like_posts)


class PostHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self,post_id):
        post=photo.get_post(post_id)
        users=photo.get_like_users(post.id)
        self.render('post.html',post=post,users=users)


class UploadHandler(AuthBaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg',None)
        for img in img_files:

            im = photo.UploadImage('static',img['filename'])
            im.save_upload(img['body'])
            im.make_thumb()
            photo.add_post(self.current_user,im.upload_url,im.thumb_url)

        self.redirect('/explore')