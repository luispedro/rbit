# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from __future__ import print_function
from six import u

def _monthname(m):
    months = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
        ]
    return months[m-1]

def reldate(date, base=None):
    '''
    r = reldate(date, base={now()})

    Relative dates
    '''
    from datetime import datetime
    if base is None:
        base = datetime.now()
    diff = base - date
    if diff.days > 30:
        if base.year != date.year:
            return u('{0} {1} {2} at {3}:{4}').format(date.day, _monthname(date.month), date.year, date.hour, date.minute)
        return u('{0} {1} at {2}:{3}').format(date.day, _monthname(date.month), date.hour, date.minute)
    if diff.days > 1:
        return u('{0} days ago ({1} {2} at {3}:{4})').format(diff.days, date.day, _monthname(date.month), date.hour, date.minute)
    if diff.days == 1:
        return u('yesterday at {0}:{1}').format(date.hour, date.minute)
    if diff.days in (0,-1):
        return u('today at {0}:{1}').format(date.hour, date.minute)
    return u('{0} {1} at {2}:{3}').format(date.day, _monthname(date.month), date.hour, date.minute)
