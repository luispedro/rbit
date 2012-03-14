# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from rbit import config
from rbit import backend
from rbit import imap
from rbit import models
from rbit import index


index = index.get_index()
cfg = config.Config('config', backend.create_session)
session = backend.create_session()
