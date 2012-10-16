# -*- coding: utf-8 -*-
# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from rbit import decode
from six import u
def test_decode_header():
    assert decode.decode_header('=?iso-8859-1?Q?=A1Hola,_se=F1or!?=') == u('¡Hola, señor!')
    assert decode.decode_header('ascii') == 'ascii'

def test_decode_with_nospace():
    s = '=?UTF-8?Q?Adri=C3=A1n=20Chaves=20Fern=C3=A1ndez=20?=<test@example.com>'
    assert decode.decode_header(s) == u('Adrián Chaves Fernández <test@example.com>')
