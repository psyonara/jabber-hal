from subprocess import check_output

from yapsy.IPlugin import IPlugin

class CommandPlugin(IPlugin):

    def command_received(self, xmpp_client, msg):
        if (msg['type'] == 'groupchat' and msg['body'].startswith("%s do " % xmpp_client.nick)) or (msg['type'] in ('chat', 'normal') and msg["body"].startswith("do ")):
            out = check_output(['bash', '-c', 'top -b -n 1 | head -n 20'])
            msg.reply(out).send()
