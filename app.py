import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options
from handlers import main,auth,chat,service

define('port',default='8000',help='Listening port',type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/',main.IndexHandler),
            ('/explore',main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)',main.PostHandler),
            ('/upload',main.UploadHandler),
            ('/login',auth.LoginHandler),
            ('/logout',auth.LogoutHandler),
            ('/signup',auth.SignupHandler),
            ('/profile/(?P<post_id>[0-9]+)',main.ProfileHandler),
            ('/profile',main.ProfileHandler),
            ('/room',chat.RoomHandler),
            ('/ws',chat.ChatSocketHandler),
            ('/save',service.AsyncSaveURLHandler),
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
            cookie_secret='derius214dfaledjk2318',
            login_url='/login',
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    # 'password': '',
                    'db_sessions': 5,  # redis db index
                    'db_notifications': 11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                },
            }
        )

        super(Application,self).__init__(handlers,**settings)

applications = Application()

if __name__=='__main__':
    tornado.options.parse_command_line()
    applications.listen(options.port)
    print("server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()