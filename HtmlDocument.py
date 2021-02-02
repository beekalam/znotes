import os

from utils import read_file_content, HIGHLIGHT_JS_PATH


class HtmlDocument:
    def __init__(self) -> None:
        self.jsContent = []
        self.cssContent = []
        self.addCSS(read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "default.min.css")))
        self.addJS(read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "highlight.min.js")))

    def addJS(self, js):
        self.jsContent.append(js)

    def addCSS(self, style):
        self.cssContent.append(style)

    def make(self, content):

        self.addJS("""
                document.querySelectorAll('pre.highlight').forEach(block => {
                  hljs.highlightBlock(block);
                });
        """)

        css_content = ""
        for css in self.cssContent:
            css_content = css_content + "<style>{}</style>".format(css)

        js_content = ""
        for js in self.jsContent:
            js_content = js_content + "<script>{}</script>".format(js)

        html = """
        <html>
        <head>
            {}
        </head>
        <body>
            {}
            {}
        </body>
        </html>
        """.format(css_content, content, js_content)
        return html
