from message_plugin import MessagePlugin
from presence_plugin import PresencePlugin

from Queue import Queue
from threading import Thread
import datetime


class LoggingHelper(MessagePlugin, PresencePlugin):

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

    def str_from_presence(self, presence, status):
        now = datetime.datetime.now()
        return "(%s) %s is %s.\n" % (now.strftime("%d/%m/%Y %H:%M:%S"), presence["from"].resource, status)

    def message_received(self, msg, nick=""):
        if msg['type'] == 'groupchat':
            item = {}
            item["room"] = msg["mucroom"]
            item["text"] = self.str_from_msg(msg)
            self.q.put(item)

    def got_online(self, xmpp_client, presence):
        item = {}
        item["room"] = presence["from"].bare
        item["text"] = self.str_from_presence(presence, "online")
        self.q.put(item)
