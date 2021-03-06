import ConfigParser
import getpass
import logging
import os
import sys
from optparse import OptionParser

from message_plugin import MessagePlugin
from presence_plugin import PresencePlugin

import sleekxmpp
from yapsy.PluginManager import PluginManager

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

class MUCBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        # Load plugins
        self.plugin_manager = PluginManager()
        self.plugin_manager.setPluginPlaces(["plugins_enabled"])
        self.plugin_manager.setCategoriesFilter({
            "Message" : MessagePlugin,
            "Presence": PresencePlugin
        })
        self.plugin_manager.collectPlugins()
        # Activate all loaded plugins
        for pluginInfo in self.plugin_manager.getAllPlugins():
           self.plugin_manager.activatePluginByName(pluginInfo.name)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)
        self.add_event_handler("muc::%s::got_offline" % self.room, self.muc_offline)

    def start(self, event):
        self.get_roster()
        self.send_presence()
        if self.room and len(self.room) > 0:
            self.plugin['xep_0045'].joinMUC(self.room,
                                            self.nick,
                                            wait=True)

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            for pluginInfo in self.plugin_manager.getPluginsOfCategory("Message"):
                pluginInfo.plugin_object.message_received(msg)

    def muc_message(self, msg):
        if msg['mucnick'] != self.nick:
            for pluginInfo in self.plugin_manager.getPluginsOfCategory("Message"):
                pluginInfo.plugin_object.message_received(msg, nick=self.nick)

    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nick:
            for pluginInfo in self.plugin_manager.getPluginsOfCategory("Presence"):
                pluginInfo.plugin_object.got_online(self, presence)

    def muc_offline(self, presence):
        if presence['muc']['nick'] != self.nick:
            for pluginInfo in self.plugin_manager.getPluginsOfCategory("Presence"):
                pluginInfo.plugin_object.got_offline(self, presence)

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    jid, password, room, nick = None, None, None, None
    if os.path.exists("connect.ini"):
        conf = ConfigParser.ConfigParser()
        conf.read("connect.ini")

        jid = conf.get("account", "jid")
        password = conf.get("account", "pwd")
        room = conf.get("muc", "room")
        nick = conf.get("muc", "nick")

    if opts.jid is None:
        opts.jid = jid if jid else raw_input("Username: ")
    if opts.password is None:
        opts.password = password if password else getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = room if room else raw_input("MUC room: ")
    if opts.nick is None:
        opts.nick = nick if nick else raw_input("MUC nickname: ")

    xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick)
    xmpp.register_plugin('xep_0045') # Multi-User Chat

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
