# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from nose.tools import with_setup
import email

from rbit.sync import get_text, message_to_model, save_attachment
from rbit.tests.tools import _open

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

def test_latin():
    m = email.message_from_string(_open('latin.eml').read())
    t = get_text(m)
    assert type(t) is unicode

def test_signed():
    m = email.message_from_string(_open('signed.eml').read())
    t = get_text(m)
    assert type(t) is unicode
    m = _open('signed.eml').read()
    (model,) = message_to_model(m, 'folder', 20, [])
    assert model.to == 'pythonvision@googlegroups.com'

def test_unknown_8bit():
    m = email.message_from_string(_open('unknown.eml').read())
    t = get_text(m)
    assert type(t) is unicode

def test_inline():
    m = email.message_from_string(_open('inline.eml').read())
    t = get_text(m)
    assert type(t) is unicode


def test_attachment():
    @with_setup(setup=_mk_tmp,teardown=_rm_tmp)
    def try_save_attachment(message):
        m = email.message_from_string(_open(message + '.eml').read())
        m = m.get_payload()[1]
        for inner in m.walk():
            if inner.get_filename():
                f = save_attachment('INBOX', 8, inner)

    yield try_save_attachment, 'forwarded'
    yield try_save_attachment, 'filename8'
    yield try_save_attachment, 'filename_empty'


