from rbit.html import text_from_html

def test_text_from_html():
    assert text_from_html('<html><body><p>This is the text</p></body></html>') == "This is the text"
