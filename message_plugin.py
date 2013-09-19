from yapsy.IPlugin import IPlugin

class MessagePlugin(IPlugin):

    def message_received(self, msg):
        msg.reply("Acknowledged.").send()
