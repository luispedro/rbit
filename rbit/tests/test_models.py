from rbit.models import Message

def test_from_email_message():
    import email
    message = email.Message.Message()
    message['To'] = 'rita@ritareis.org'
    message['From'] = 'Luis Pedro Coelho <luis@luispedro.org>'
    message['Date'] = 'Mon, 23 Jan 2012 23:00:47 -0000'
    message.set_payload('I love you')
    m = Message.from_email_message(message, 123)
    assert m.to == 'rita@ritareis.org'

