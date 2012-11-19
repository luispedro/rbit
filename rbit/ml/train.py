# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from os import path

from rbit import models
from rbit import config
from rbit.backend import call_create_session
from rbit.tools import callonce

from rbit.ml.multi import multi_tree_learner
from rbit.ml.vw_learner import VWLearner

def _maybemkdir(dir):
    from os import makedirs
    try:
        makedirs(dir)
    except OSError:
        pass

_basedir = path.expanduser('~/.local/share/rbit/vw/')

@callonce()
def retrain_folder_model(create_session=None):
    '''
    model = retrain_folder_model(create_session={backend.create_session})

    Train a model on all messages

    Parameters
    ----------
    create_session : callable, optional

    Returns
    -------
    model : A Model
    '''
    import random
    cleanup_models(_basedir)
    _maybemkdir(_basedir)

    session = call_create_session(create_session)
    ms = session. \
            query(models.Message.folder, models.Message.mid). \
            filter(models.Message.folder != u'INBOX'). \
            filter(models.Message.folder != u'INBOX.Sent'). \
            all()
    learner = multi_tree_learner(VWLearner(_basedir))
    if len(ms) > 0:
        from time import time
        # The reason for the shuffle is to improve the learning
        # Without it, the online learner sees 1 1 1 1 1 1 1 ... 1 -1 -1 -1 -1 ... -1
        # which is likely to not be as good as a random mix of +/-1
        random.shuffle(ms)
        labels = [m.folder for m in ms]
        mids = [m.mid for m in ms]
        model = learner.train(mids, labels)
        cfg = config.Config('machine-learning', create_session)
        cfg.set('folder-model', 'model', model)
        cfg.set('folder-model', 'retrained-time', int(time()))

def cleanup_models(basedir):
    '''
    cleanup_models(basedir)

    Delete all model associated files
    '''
    try:
        from shutil import rmtree
        rmtree(basedir)
    except OSError:
        pass

if __name__ == '__main__':
    retrain_folder_model()
