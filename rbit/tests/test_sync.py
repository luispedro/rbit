# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
import email
from os import path

from rbit.sync import get_text, message_to_model

def _open(fname):
    return open(path.join(
                path.dirname(path.abspath(__file__)),
                'data',
                fname))

def test_latin():
    m = email.message_from_string(_open('latin.eml').read())
    t = get_text(m)
    assert type(t) is unicode

def test_signed():
    m = email.message_from_string(_open('signed.eml').read())
    t = get_text(m)
    assert type(t) is unicode
    m = _open('signed.eml').read()
    model = message_to_model(m, 'folder', 20)
    assert model.to == 'pythonvision@googlegroups.com'

def test_unknown_8bit():
    m = email.message_from_string(_open('unknown.eml').read())
    t = get_text(m)
    assert type(t) is unicode
