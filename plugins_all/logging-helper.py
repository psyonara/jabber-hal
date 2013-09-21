from message_plugin import MessagePlugin

from Queue import Queue
from threading import Thread
import datetime


class LoggingHelper(MessagePlugin):

    def log_writer(self):
        while True:
            item = self.q.get()
            self.write_log_to_file(item)
            self.q.task_done()

    def __init__(self):
        self.q = Queue()
        t = Thread(target=self.log_writer)
        t.daemon = True
        t.start()

    def write_log_to_file(self, item):
        with open("logs/%s.log" % (item['room']), 'a') as fh:
            fh.write(item['text'])

    def str_from_msg(self, msg):
        now = datetime.datetime.now()
        return "(%s) %s: %s\n" % (now.strftime("%d/%m/%Y %H:%M:%S"), msg["mucnick"], msg["body"])

    def message_received(self, msg, nick=""):
        if msg['type'] == 'groupchat':
            item = {}
            item["room"] = msg["mucroom"]
            item["text"] = self.str_from_msg(msg)
            self.q.put(item)
