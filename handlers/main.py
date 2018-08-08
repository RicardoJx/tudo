import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('explore.html')


class PostHandler(tornado.web.RequestHandler):
    def get(self,post_id):
        self.render('post.html',post_id=post_id)