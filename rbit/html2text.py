# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from __future__ import print_function
from HTMLParser import HTMLParser

class HTML2Text(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.text = []
        self.status = 'head'

    def handle_starttag(self, tag, _attrs):
        if tag == 'body':
            self.status = 'body'

    def handle_data(self, data):
        if self.status == 'body':
            self.text.append(data)

    def get_reset(self):
        text = u''.join(self.text)
        self.text = []
        return text

def html2text(html):
    html = html.strip()
    output = file('test.txt', 'w')
    if html.startswith('<'):
        parser = HTML2Text()
        parser.feed(html)
        return parser.get_reset()
    return html
