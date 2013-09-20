jabber-hal
==========

Jabber bot for performing actions in single and multi-user chat. Features can be added by creating plugins (via YAPSY).

Installation
------------

Install requirements via pip:

```pip install -r requirements.txt```

Running
-------

```python jabber-hal.py```

Options can be provided via command line parameters. For details:

```python jabber-hal.py --help```

Parameters can also be provided from an ini file ("connect.ini"):

```
[account]
jid=user@server.ext
pwd=password

[muc]
room=room_name
nick=nick_name
```

Activating Plugins
------------------

To activate a plugin, copy the plugin's files from "plugins_all" to "plugins_enabled", in the project's base directory.
