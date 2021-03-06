import unittest

from HtmlDocument import HtmlDocument


class HtmlDocumentTest(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_it_should_content(self):
        htmlDocument = HtmlDocument()
        content = "This is my test content"
        self.assertTrue(content in htmlDocument.make(content))

    def test_can_add_inline_js_content(self):
        js = "var a = 12;"
        htmlDocument = HtmlDocument()
        htmlDocument.addJS(js)
        self.assertTrue(js in htmlDocument.make(""))

    def test_can_add_css_content(self):
        style = ".header{background-color:green}"
        htmlDocument = HtmlDocument()
        htmlDocument.addCSS(style)
        self.assertTrue(style in htmlDocument.make(""))

if __name__ == "__main__":
    unittest.main()