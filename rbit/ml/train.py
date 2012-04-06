# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from multi import multi_tree_learner
from rbit import models
from rbit.backend import call_create_session

from vw_learner import VWLearner

def train_model(create_session=None):
    session = call_create_session(create_session)
    ms = session.query(models.Message).all()
    labels = [m.folder for m in ms]
    learner = multi_tree_learner(VWLearner())
    return learner.train(ms, labels)

if __name__ == '__main__':
    import pickle
    model = train_model()
    pickle.dump(model, file('model.pp','w'))
