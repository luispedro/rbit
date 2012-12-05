from rbit.html import text_from_html, format_as_html

def test_text_from_html():
    assert text_from_html('<html><body><p>This is the text</p></body></html>') == "This is the text"

def test_format_as_html():
    html = format_as_html(u'Paragraph 1.\n\nParagraph 2.\n')
    assert html.count('<p>') == 2

    html = format_as_html(u'Paragraph 1.\nContinue 1.\n')
    assert html.count('<p>') == 1

    html = format_as_html(u'Paragraph 1.\r\n\r\nParagraph 2.\r\n')
    assert html.count('<p>') == 2

    html = format_as_html(u'Paragraph 1.\r\n  \t \r\nParagraph 2.\r\n')
    assert html.count('<p>') == 2

