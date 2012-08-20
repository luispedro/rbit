# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

def callonce():
    '''
    @callonce()
    def f(...):
        ...

    Makes sure that ``f`` is not called twice concurrently.
    '''
    def capture(f):
        inside = [False]
        def captured(*args, **kwargs):
            if inside[0]:
                raise RuntimeError('Synchronized function called twice')
            inside[0] = True
            try:
                return f(*args, **kwargs)
            finally:
                inside[0] = False
        return captured
    return capture
