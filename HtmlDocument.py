import os

from utils import read_file_content, HIGHLIGHT_JS_PATH


class HtmlDocument:
    def __init__(self, styles="") -> None:
        self.jsContent = []
        self.cssContent = []
        # self.highlightjs_js = read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "highlight.min.js"))
        self.addJS(read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "highlight.min.js")))
        self.highlightjs_css = read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "default.min.css"))
        self.styles = styles

    def addJS(self, js):
        self.jsContent.append(js)

    def addCSS(self, style):
        self.cssContent.append(style)

    def make(self, content):
        hljs = """
            <style>{}</style>
            """.format(self.highlightjs_css)


        for css in self.cssContent:
            hljs += "<style>{}</style>".format(css)

        for js in self.jsContent:
            hljs += "<script>{}</script>".format(js)

        hljs = hljs + """
            <script>
                document.querySelectorAll('pre.highlight').forEach(block => {
                  // then highlight each
                  hljs.highlightBlock(block);
                });
            </script>
        """

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
