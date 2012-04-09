# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from rbit import models
from rbit import config


model = None

def init():
    '''
    init()

    Loads model from database
    '''
    global model
    cfg = config.Config('machine-learning', None)
    model = cfg.get('folder-model', 'model')

def predict_inbox(message, folder, _uid, **kwargs):
    '''
    predict_inbox(message, folder, _uid, session)

    This matches the new-message signal
    '''
    if folder != u'INBOX':
        return
    session = kwargs['session']
    value,folder = model.apply(message)
    pred = models.Prediction(type='folder', strength=value, value=folder)
    message.predictions.append(pred)
    session.add(pred)


