# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from HTMLParser import HTMLParser
import re

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


def format_as_html(text):
    '''
    html = format_as_html(text)

    Format as HTML
    '''
    if '<html>' in text or \
        '<body>' in text or \
        '<p>' in text: return text
    start = u'<html><head></head><body>'
    end = u'</body></html>'
    text = text.replace('\r\n', '\n')
    text = re.sub('^\s*$','', text, flags=re.M)
    paragraphs = text.split('\n\n')
    paragraphs = [u'<p>{}</p>'.format(p) for p in paragraphs]
    html = u''.join([start]+paragraphs+[end])
    return html

