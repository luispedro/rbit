# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

import datetime
import time
import urwid
import urwid.raw_display
import urwid.web_display

from rbit import config
from rbit import backend
from rbit import imap
from rbit import models

backend.init()
session = backend.create_session()
q = session.query(models.Message).all()

def list_messages(folder):
    text_header = 'Messages in %s' % folder
    blank = urwid.Divider('=', bottom=1)
    listbox_content = []
    for message in q:
        first_words = " ".join(message.body.split()[:32]) + "..."
        text = urwid.Text([
            ('bold_underline', message.from_),
            " ",
            ('bold', message.subject or "<no subject>"),
            " ",
            first_words])
        listbox_content.extend([text, blank])

    header = urwid.AttrWrap(urwid.Text(text_header), 'header')
    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
    return frame

def unhandled(key):
    if key in ('q','Q'):
        raise urwid.ExitMainLoop()

palette = [
        ('body','black','white', 'standout'),
        ('header','white','dark red', 'bold'),
        ('bold','black,bold','white', 'bold'),
        ('bold_underline','black,bold,underline','white', 'bold,underline'),
        ]
frame = list_messages('INBOX')
screen = urwid.raw_display.Screen()

urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()

