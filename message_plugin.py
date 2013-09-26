from yapsy.IPlugin import IPlugin

class MessagePlugin(IPlugin):

    def message_received(self, msg, nick=""):
        if (msg['type'] == 'groupchat' and msg['body'].startswith("%s " % nick)) or msg['type'] in ('chat', 'normal'):
            msg.reply("Message received").send()
