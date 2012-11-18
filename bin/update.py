#!/usr/bin/env python
# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from gevent import monkey
monkey.patch_all(thread=False)

from rbit import signals
from rbit.sync import update_all_folders
from rbit import config
from rbit import backend
from rbit import models
from rbit import imap
from rbit.ml import predict

def print_status(_, s):
    print s

predict.init()
signals.register('status', print_status)
signals.register('new-message', predict.predict_inbox)

cfg = config.Config('config', backend.create_session)
client = imap.IMAPClient.from_config(cfg)
update_all_folders(client)

