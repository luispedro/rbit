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

text_header = 'Messages in INBOX'
blank = urwid.Divider()
listbox_content = []
for message in q:
    summary = "%s: %s\n%s" % (message.from_, message.subject, " ".join(message.body.split()[:32]))
    listbox_content.extend([urwid.Text(summary), blank])
header = urwid.AttrWrap(urwid.Text(text_header), 'header')
listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header)
palette = [
        ('body','black','light gray', 'standout'),
        ('header','white','dark red', 'bold'),
        ]
screen = urwid.raw_display.Screen()

def unhandled(key):
    if key in ('q','Q'):
        raise urwid.ExitMainLoop()

urwid.MainLoop(frame, palette, screen, unhandled_input=unhandled).run()

