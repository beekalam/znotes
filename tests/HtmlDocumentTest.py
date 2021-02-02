import unittest

from HtmlDocument import HtmlDocument


class HtmlDocumentTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_it_should_content(self):
        htmlDocument = HtmlDocument()
        content = "This is my test content"
        self.assertTrue(content in htmlDocument.make(content))

    def test_html_content_can_accept_styles(self):
        styles = """
            .header{
                background-color:green
            }
        """
        htmlDocument = HtmlDocument(styles=styles)
        self.assertTrue(styles in htmlDocument.make("<style>{}</style>".format(styles)))
