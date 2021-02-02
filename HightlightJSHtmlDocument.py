import os

from HtmlDocument import HtmlDocument
from utils import read_file_content, HIGHLIGHT_JS_PATH


class HighlightJSHtmlDocument(HtmlDocument):

    def __init__(self) -> None:
        super().__init__()

        self.addCSS(read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "default.min.css")))
        self.addJS(read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "highlight.min.js")))

        self.addJS("""
                document.querySelectorAll('pre.highlight').forEach(block => {
                  hljs.highlightBlock(block);
                });
        """)
