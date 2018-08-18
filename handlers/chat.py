import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import uuid
from pycket.session import SessionMixin
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from .main import AuthBaseHandler

class RoomHandler(AuthBaseHandler):
    """
    聊天室页面
    """
    @tornado.web.authenticated
    def get(self):
        self.render("room.html", messages=ChatSocketHandler.msg_list_cache)


class ChatSocketHandler(tornado.websocket.WebSocketHandler,SessionMixin):
    waiters = set()    # 等待接收信息的用户
    msg_list_cache = []         # 存放消息
    cache_size = 200   # 消息列表的大小

    def get_current_user(self):
        return self.session.get('tudo_user',None)

    def get_compression_options(self):
        """ 非 None 的返回值开启压缩 """
        return {}

    def open(self):
        """ 新的WebSocket连接打开，自动调用 """
        logging.info("new connection %s" % self)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        """ WebSocket连接断开，自动调用 """
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        """更新消息列表，加入新的消息"""
        cls.msg_list_cache.append(chat)
        if len(cls.msg_list_cache) > cls.cache_size:
            cls.msg_list_cache = cls.msg_list_cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        """给每个等待接收的用户发新的消息"""
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    @classmethod
    def make_chat(cls, body, sent_by='system', img=''):
        ret= {
            "id": str(uuid.uuid4()),
            "body": body,
            "sent_by":sent_by,
            "img":img,
        }
        return ret

    def on_message(self, message):
        """ WebSocket 服务端接收到消息，自动调用 """
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        if parsed['body'].startswith("http://"):
            save_url="http://localhost:8000/save?url={}&from=room&user={}".format(parsed['body'],self.current_user)
            client = AsyncHTTPClient()
            IOLoop.current().spawn_callback(client.fetch,save_url,request_timeout=20)
            body="亲爱的{}，您发送的URL:{} 正在处理。".format(self.current_user,parsed['body'])
            chat_msg = ChatSocketHandler.make_chat(body)
            chat_msg['html'] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat_msg)
            )
            self.write_message(chat_msg)
        else:
            chat_msg = ChatSocketHandler.make_chat(parsed['body'], self.current_user)
            chat_msg['html'] = tornado.escape.to_basestring(
                self.render_string("message.html", message=chat_msg)
            )
            ChatSocketHandler.update_cache(chat_msg)
            ChatSocketHandler.send_updates(chat_msg)