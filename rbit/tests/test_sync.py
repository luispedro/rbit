# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from nose.tools import with_setup
import email
from os import path

from rbit.sync import get_text, message_to_model, save_attachment

_tmp_dir = '/tmp/rbit-tests/'

def _mk_tmp():
    from os import mkdir
    try:
        mkdir(_tmp_dir)
    except:
        pass

def _rm_tmp():
    from shutil import rmtree
    rmtree(_tmp_dir)

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

def test_inline():
    m = email.message_from_string(_open('inline.eml').read())
    t = get_text(m)
    assert type(t) is unicode


@with_setup(setup=_mk_tmp,teardown=_rm_tmp)
def test_attachment():
    m = email.message_from_string(_open('forwarded.eml').read())
    m = m.get_payload()[1]
    result = save_attachment('INBOX', 8, m, basedir=_tmp_dir)
