from rbit.html2text import html2text

def test_smoke():
    assert html2text('<html></html>') == ''
    assert html2text('<html><head></head></html>') == ''
    assert html2text('<html><head></head><body><p>Hello World</p></html>') == 'Hello World'

def test_p_only():
    assert html2text('<p>Text only</p>') == 'Text only'
