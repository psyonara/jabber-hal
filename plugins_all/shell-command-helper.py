from ConfigParser import ConfigParser
from subprocess import check_output

from message_plugin import MessagePlugin

class ShellCommandHelper(MessagePlugin):

    def execute_commands(self, commands, message):
        for cmd in commands:
            print(cmd[0])
            print(message)
            if message.strip() == cmd[0].strip():
                return check_output(['bash', '-c', cmd[1]])
        return None

    def message_received(self, msg, nick=""):
        conf = ConfigParser()
        conf.read("plugins_enabled/shell-command-helper.ini")

        # commands available to single and multi user chat
        if msg['type'] in ('chat', 'normal'):
            reply_all = self.execute_commands(conf.items("commands_all"), msg["body"])
            if reply_all:
                msg.reply(reply_all).send()
            else:
                # Single user chat
                msg.reply(self.execute_commands(conf.items("commands_single"), msg["body"])).send()
        elif msg['type'] == 'groupchat' and msg['body'].startswith("%s " % nick):
            reply_all = self.execute_commands(conf.items("commands_all"), msg["body"].replace(nick, ""))
            if reply_all:
                msg.reply(reply_all).send()
            else:
                # Multi user chat
                msg.reply(self.execute_commands(conf.items("commands_multi"), msg["body"].replace(nick, ""))).send()
