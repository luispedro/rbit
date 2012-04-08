#!/usr/bin/env python
# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from rbit import signals
from rbit.sync import update_all_folders
from rbit import config
from rbit import backend
from rbit import imap

def print_status(_, s):
    print s

signals.register('status',print_status)

cfg = config.Config('config', backend.create_session)
client = imap.IMAPClient.from_config(cfg)
update_all_folders(client)
client.close()

