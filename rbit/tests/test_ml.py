def test_formatted_headers():
    from rbit.ml.vw_learner import _formatted_headers
    headers  = {
     'To': ['Luis Pedro Coelho <luis@luispedro.org>, Somebody else <else@gmail.com>'],
     'X-DH-Virus-Scanned': ['Debian amavisd-new at diehard.dreamhost.com'],
     'X-Original-To': ['luis@luispedro.org'],
     'X-Spam-Flag': ['NO'],
     'X-Spam-Level': [''],
     'X-Spam-Score': ['0.001'],
     'X-Spam-Status': ['No, score=0.001 tagged_above=-999 required=999\r\n\ttests=[HTML_MESSAGE=0.001] autolearn=disabled']}

    f = _formatted_headers(headers)
    assert len(f)


def test_as_features():
    from rbit.ml.vw_learner import _as_features
    assert 'a' != _as_features('a')


def test_parse_label():
    from rbit.ml.vw_learner import _parse_label
    val, s = _parse_label('1:0 2:1 3:0')
    assert val == 2
    assert s == 1

    val, s = _parse_label('1:0 2:1 3:2')
    assert val == 3
    assert s == 2

    val, s = _parse_label('1:0 2:1 3:2\n')
    assert val == 3
    assert s == 2
