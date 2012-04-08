# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from os import path

from rbit import models
from rbit import config
from rbit.backend import call_create_session

from rbit.ml.multi import multi_tree_learner
from rbit.ml.vw_learner import VWLearner

def _maybemkdir(dir):
    from os import makedirs
    try:
        makedirs(dir)
    except OSError:
        pass

_basedir = path.expanduser('~/.local/share/rbit/vw/')

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
    ms = session.query(models.Message.folder, models.Message.mid).all()
    # The reason for the shuffle is to improve the learning
    # Without it, the online learner sees 1 1 1 1 1 1 1 ... 1 -1 -1 -1 -1 ... -1
    # which is likely to not be as good as a random mix of +/-1
    random.shuffle(ms)
    labels = [m.folder for m in ms]
    learner = multi_tree_learner(VWLearner(_basedir))
    mids = [m.mid for m in ms]
    model = learner.train(mids, labels)

    cfg = config.Config('machine-learning', create_session)
    cfg.set('folder-model', 'model', model)

def cleanup_models(basedir):
    '''
    cleanup_models(basedir)

    Delete all model associated files
    '''
    from shutil import rmtree
    rmtree(basedir)

if __name__ == '__main__':
    retrain_folder_model()
