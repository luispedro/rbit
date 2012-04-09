# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from HTMLParser import HTMLParser
class _GetText(HTMLParser):
    def __init__(self):
        # Cannot call super() because HTMLParser is an old-style class!
        HTMLParser.__init__(self)
        self.in_body = False
        self.active = True
        self.texts = []
    def handle_starttag(self,tag, _):
        if tag == 'body':
            self.in_body = True
        if tag in ('style','script'):
            self.active = False
    def handle_endtag(self,tag):
        if tag == 'body':
            self.in_body = False
        if tag in ('style','script'):
            self.active = True
    def handle_data(self, data):
        if self.in_body and self.active:
            self.texts.append(data)

def text_from_html(html):
    '''
    text = text_from_html(html)

    Gets the text from the HTML representation

    Parameters
    ----------
    html : str or unicode
        HTML Representation

    Returns
    -------
    text : str or unicode
        Just the textual content of `html`
    '''
    parser = _GetText()
    parser.feed(html)
    return "".join(parser.texts)

