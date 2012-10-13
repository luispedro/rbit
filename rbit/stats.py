# -*- coding: utf-8 -*-
# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from rbit import models
from rbit.backend import call_create_session
def day_hour_grid(normed=True, create_session=None):
    '''
    grid = day_hour_grid(normed=True, create_session={backend.create_session})

    Computes a grid of day × hour usage (for all messages)

    Parameters
    ----------
    normed : boolean, optional
        Whether the grid should be normalised

    Returns
    -------
    grid : ndarray
    '''
    import numpy as np
    session = call_create_session(create_session)
    grid = np.zeros((7,24))
    for d in session.query(models.Message.date):
        (d,) = d
        grid[d.weekday(), d.hour] += 1
    if normed:
        grid /= grid.sum()
    return grid

