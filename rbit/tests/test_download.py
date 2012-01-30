# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
import email
from os import path

from rbit.download import get_text

def _open(fname):
    return open(path.join(
                path.dirname(path.abspath(__file__)),
                'data',
                fname))

def test_latin():
    m = email.message_from_string(_open('latin.eml').read())
    t = get_text(m)
    assert type(t) is unicode

