# -*- coding: utf-8 -*-
# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from rbit import decode
def test_decode_header():
    assert decode.decode_header('=?iso-8859-1?Q?=A1Hola,_se=F1or!?=') == u'¡Hola, señor!'
    assert decode.decode_header('ascii') == 'ascii'
