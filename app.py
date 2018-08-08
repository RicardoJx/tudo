import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define,options
from handlers import main

define('port',default='8000',help='Listening port',type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/',main.IndexHandler),
            ('/explore',main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)',main.PostHandler),
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
        )

        super(Application,self).__init__(handlers,**settings)

applications = Application()

if __name__=='__main__':
    tornado.options.parse_command_line()
    applications.listen(options.port)
    print("server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()