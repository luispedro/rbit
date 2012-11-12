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

def test_load_model():
    def load_commit(message):
        session = in_memory_sessionmaker()()
        session.add_all(message_to_model(_open(message+'.eml').read(), 'acc', 'test', 128, []))
        session.commit()
    yield load_commit, 'header8'
    yield load_commit, 'bad-date'
    yield load_commit, 'github'
    yield load_commit, 'unknown'
    yield load_commit, 'filename8'

def test_list():
    from rbit import messages
    session = in_memory_sessionmaker()()
    for uid,message in enumerate(['header8', 'github']):
        session.add_all(message_to_model(_open(message+'.eml').read(), 'acc', 'test', 12+uid, []))
    session.commit()

    assert len(messages.list_uids('acc', create_session=(lambda:session))) == 2
    assert len(messages.list_uids('nope', create_session=(lambda:session))) == 0
    assert len(messages.list_uids('acc', folder='test',create_session=(lambda:session))) == 2
    assert len(messages.list_uids('acc', folder='nope',create_session=(lambda:session))) == 0
    assert messages.list_folders('acc', create_session=(lambda:session)) == ['test']
    assert messages.list_folders('nope', create_session=(lambda:session)) == []


def test_headers():
    import email
    message = _open('inline.eml').read()
    msg = email.message_from_string(message)
    model = Message.from_email_message(msg, 123)
    assert len(model.headers['References'])
    assert 'Received' not in model.headers
