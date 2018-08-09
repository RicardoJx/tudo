import tornado.web
from .main import AuthBaseHandler
from utils.account import authenticate


class LoginHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        username=self.get_argument('username',None)
        password=self.get_argument('password',None)

        passed=authenticate(username,password)
        if passed:
            self.session.set('tudo_user',username)
            self.redirect('/')
        else:
            self.write({'msg':'login fail'})


class LogoutHandler(AuthBaseHandler):
    def get(self, *args, **kwargs):
        self.session.delete('tudo_user')
        self.redirect('/login')
