# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from multi import multi_tree_learner
from rbit import models
from rbit.backend import call_create_session

from vw_learner import VWLearner

def train_on_all(create_session=None):
    '''
    model = train_on_all(create_session={backend.create_session})

    Train a model on all messages

    Parameters
    ----------
    create_session : callable, optional

    Returns
    -------
    model : A Model
    '''
    session = call_create_session(create_session)
    ms = session.query(models.Message.folder, models.Message.mid).all()
    labels = [m.folder for m in ms]
    learner = multi_tree_learner(VWLearner())
    mids = [m.mid for m in ms]
    return learner.train(mids, labels)


if __name__ == '__main__':
    import pickle
    model = train_on_all()
    pickle.dump(model, file('model.pp','w'))
