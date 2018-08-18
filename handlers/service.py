from datetime import datetime
import tornado.web
import tornado.gen
import tornado.escape
from tornado.httpclient import HTTPClient, AsyncHTTPClient
import uuid

from .main import AuthBaseHandler
from .chat import ChatSocketHandler
from utils import photo


class AsyncSaveURLHandler(AuthBaseHandler):
    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        url=self.get_argument('url','')
        post_user = self.get_argument('user',None)
        is_room=self.get_argument('from',None) =='room'
        if not (is_room and post_user):
            print("no user and room --{} {}:{}".format(datetime.now(),post_user, url))
            return

        async_client=AsyncHTTPClient()
        print("--{}-start fetch:#{}".format(datetime.now(), url))
        resp=yield async_client.fetch(url,request_timeout=20)
        im=photo.UploadImage(self.settings['static_path'],'x.jpg')
        if not resp.body:
            self.write('empty response')
            return
        im.save_upload(resp.body)
        im.make_thumb()
        post=photo.add_post(post_user,im.upload_url,im.thumb_url)
        print("--{}-end fetch:#{}".format(datetime.now(),post.id))

        body= '{} post :{}'.format(post_user, "http://127.0.0.1:8000/post/{}".format(post.id))
        chat_msg=ChatSocketHandler.make_chat(body, img=post.thumb_url)
        chat_msg['html'] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat_msg)
        )
        ChatSocketHandler.update_cache(chat_msg)
        ChatSocketHandler.send_updates(chat_msg)
        print("message sent!")


class SaveURLHandler(AuthBaseHandler):
    """
    tongbu
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        url = self.get_argument('url',)
        client = HTTPClient()
        print('----going to fetch:{}'.format(url))
        resp = client.fetch(url)
        im=photo.UploadImage(self.settings['static_path'],'x.jpg')
        im.save_upload(resp.body)
        im.make_thumb()
        post=photo.add_post(self.current_user,im.upload_url,im.thumb_url)
        self.redirect('/post/{}'.format(post.id))