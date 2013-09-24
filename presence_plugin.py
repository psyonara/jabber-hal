from yapsy.IPlugin import IPlugin

class PresencePlugin(IPlugin):

    def got_online(self, xmpp_client, presence):
        xmpp_client.send_message(mto=presence['from'].bare, mbody="Greetings, %s." % (presence['muc']['nick']), mtype='groupchat')

    def got_offline(self, xmpp_client, presence):
        xmpp_client.send_message(mto=presence['from'].bare, mbody="We'll miss you, %s!" % (presence['muc']['nick']), mtype='groupchat')
