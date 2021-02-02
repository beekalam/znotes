import os

from utils import read_file_content, HIGHLIGHT_JS_PATH


class HtmlDocument:
    def __init__(self, styles="") -> None:
        self.jsContent = []
        self.cssContent = []
        self.addJS(read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "highlight.min.js")))
        self.addCSS(read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "default.min.css")))
        self.styles = styles

    def addJS(self, js):
        self.jsContent.append(js)

    def addCSS(self, style):
        self.cssContent.append(style)

    def make(self, content):
        hljs = ""

        self.addJS("""
            <script>
                document.querySelectorAll('pre.highlight').forEach(block => {
                  // then highlight each
                  hljs.highlightBlock(block);
                });
            </script>
        """)

        for css in self.cssContent:
            hljs += "<style>{}</style>".format(css)

        for js in self.jsContent:
            hljs += "<script>{}</script>".format(js)

        return """
        <html>
        <head>
            {}
        </head>
        <body>
            {}
            {}
        </body>
        </html>
        """.format(self.styles, content, hljs)
