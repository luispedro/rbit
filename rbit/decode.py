# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

_default_charsets = ['utf-8', 'latin1']
def decode_unicode(text, charsets):
    '''
    uni = decode_unicode(text)

    Decode string to unicode

    Parameters
    ----------
    text : str or unicode
    charsets : list of str
        Charsets to try

    Returns
    -------
    uni : unicode
    '''
    from itertools import chain
    if isinstance(text, unicode):
        return text
    for charset in chain(charsets, _default_charsets):
        try:
            return unicode(text, charset)
        except:
            pass
    return unicode(text, 'utf-8', 'replace')


def decode_header(encoded):
    '''
    dec = decode_header(encoded)

    Decodes RFC 2047 strings.

    Parameters
    ----------
    encoded : str

    Returns
    -------
    dec : unicode
    '''
    from email import header
    if isinstance(encoded, unicode):
        return encoded
    if '=?' in encoded:
        import pyzmail
        return pyzmail.parse.decode_mail_header(encoded)
    return decode_unicode(encoded, [])

