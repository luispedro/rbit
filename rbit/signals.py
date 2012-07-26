# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

_registry = {}

def emit(name, args=(), kwargs=None):
    '''
    emit(name, args=(), kwargs={})

    For each handler call registered for ``name`` calls
    ``handler(*args, **kwargs)``

    Parameters
    ----------
    name : str
        Signal name
    args : sequence, optional
    kwargs : dict, optional

    See Also
    --------
    register : function
    '''
    if kwargs is None:
        kwargs = {}
    for f in _registry.get(name, []):
        f(*args, **kwargs)

def register(name, f, replace_all=False):
    '''
    register(name, f, replace_all=False)

    Register ``f`` as a handler for signal ``name``

    Parameters
    ----------
    name : str
        Signal name
    f : callable
    replace_all : boolean, optional
        If ``replace_all``, then all previous signals registered for this event
        are removed.

    See Also
    --------
    emit : function
    '''
    if replace_all:
        _registry[name] = [f]
    else:
        if name not in _registry:
            _registry[name] = []
        _registry[name].append(f)


NEW_MESSAGE = 'new-message'
DELETE_MESSAGE = 'delete-message'
FOLDER_UPDATE = 'folder-update'
STATUS = 'status'
