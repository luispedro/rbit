from rbit import contact
from rbit.tests.tools import in_memory_sessionmaker
def test_get_or_create():
    session = in_memory_sessionmaker()()
    c = contact.get_or_create('Luis Pedro Coelho', None, lambda: session)
    session.add(c)
    session.commit()

    c = session.query(contact.Contact).one()
    assert len(c['name']) == 1

    c = contact.get_or_create('Luis Pedro Coelho', 'luis@luispedro.org', lambda: session)
    assert len(c['email']) == 0
    c.add_info('email', 'luis@luispedro.org')
    assert len(c['email']) == 1
    session.add(c)
    session.commit()

    c = session.query(contact.Contact).one()
    assert len(c['email']) == 1

    c = contact.get_or_create(None, 'luis@luispedro.org', lambda: session)
    assert len(c['email']) == 1
