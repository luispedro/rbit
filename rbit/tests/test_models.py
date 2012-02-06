from rbit.models import Message
from rbit.tests.tools import in_memory_sessionmaker, _open
from rbit.sync import get_text, message_to_model, save_attachment


def test_from_email_message():
    import email
    message = email.Message.Message()
    message['To'] = 'rita@ritareis.org'
    message['From'] = 'Luis Pedro Coelho <luis@luispedro.org>'
    message['Date'] = 'Mon, 23 Jan 2012 23:00:47 -0000'
    message.set_payload('I love you')
    m = Message.from_email_message(message, 123)
    assert m.to == 'rita@ritareis.org'

def test_header8():
    session = in_memory_sessionmaker()()
    session.add(message_to_model(_open('header8.eml').read(), 'test', 128))
    session.commit()

def test_baddate():
    session = in_memory_sessionmaker()()
    session.add(message_to_model(_open('bad-date.eml').read(), 'test', 128))
    session.commit()

