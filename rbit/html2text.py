# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from __future__ import print_function
from HTMLParser import HTMLParser
from six import u

_body_tags = frozenset(['body', 'p', 'div'])

class _HTML2Text(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []
        self.status = 'head'

    def handle_starttag(self, tag, _attrs):
        if tag in _body_tags:
            self.status = 'body'

    def handle_data(self, data):
        if self.status == 'body':
            self.text.append(data)

    def get_reset(self):
        text = u('').join(self.text)
        self.text = []
        return text

def html2text(html):
    '''
    text = html2text(html)

    Removes HTML formatting

    Parameters
    ----------
    html : str or unicode
        Possibly HTML text

    Returns
    -------
    text : str or unicode
        Simple text
    '''
    if not html:
        return u('')
    html = html.strip()
    if html.startswith('<'):
        parser = _HTML2Text()
        parser.feed(html)
        return parser.get_reset()
    return html
