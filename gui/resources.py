# Copyright (C) 2013 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from __future__ import print_function

from contextlib import contextmanager

class imap_manager(object):
    def __init__(self):
        from gevent.coros import Semaphore
        self.client = None
        self.sem = Semaphore(1)
        self.count = 0

    def close(self, current):
        import gevent
        gevent.sleep(360)
        self.sem.acquire()
        if self.count == current:
            self.client.close()
            self.client = None
        imap_sem.release()

    @contextmanager
    def get(self):
        import gevent
        self.count += 1
        self.sem.acquire()
        self.count += 1
        if self.client is None:
            from rbit import config
            from rbit import backend
            from rbit import imap
            cfg = config.Config('config', backend.create_session)
            self.client = imap.IMAPClient.from_config(cfg)
        yield self.client
        self.sem.release()
        gevent.spawn(lambda : self.close(self.count))



