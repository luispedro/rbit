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

class Message(urwid.Text):
    def __init__(self, message):
        self.message = message

        first_words = " ".join(message.body.split()[:64]) + "..."
        super(Message, self).__init__([
            ('bold_underline', message.from_),
            " ",
            ('bold', message.subject or "<no subject>"),
            " ",
            first_words])

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key

class FolderView(urwid.Pile):
    def __init__(self, messages):
        self.messages = messages.get_body()
        self.main = urwid.Text("If you read this, there is a bug. list.py:62")
        super(FolderView, self).__init__([('fixed', 16, messages), urwid.Filler(self.main)])
        self._set_text()

    def keypress(self, size, key):
        if key != 'enter':
            return super(FolderView, self).keypress(size, key)
        self._set_text()

    def _set_text(self):
        infocus,_idx = self.messages.get_focus()
        text = infocus.message.body
        self.main.set_text(text)
        return None


def list_messages(folder):
    text_header = 'Messages in %s' % folder
    blank = urwid.Divider('=', bottom=0)
    listbox_content = []
    for message in q:
        text = Message(message)
        text = urwid.AttrWrap(text, None, 'in-focus')
        listbox_content.extend([text, blank])

    header = urwid.Text(text_header)
    header = urwid.AttrWrap(header, 'header')
    listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
    frame = urwid.Frame(urwid.AttrWrap(listbox, 'body'), header=header, footer=urwid.AttrMap(urwid.Divider('~'), 'header'))
    return frame

def quit_on_q(key):
    if key in ('q','Q'):
        raise urwid.ExitMainLoop()

palette = [
        ('body','black','white', 'standout'),
        ('header','white','dark red', 'bold'),
        ('bold','black,bold','white', 'bold'),
        ('bold_underline','black,bold,underline','white', 'bold,underline'),
        ('in-focus', 'white', 'dark blue'),
        ]

messages = list_messages('INBOX')
top = FolderView(messages)
screen = urwid.raw_display.Screen()

urwid.MainLoop(top, palette, screen, unhandled_input=quit_on_q).run()

