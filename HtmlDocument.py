import os

from utils import read_file_content, HIGHLIGHT_JS_PATH


class HtmlDocument:
    def __init__(self, styles="") -> None:


        self.highlightjs_js = read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "highlight.min.js"))
        self.highlightjs_css = read_file_content(os.path.join(HIGHLIGHT_JS_PATH, "default.min.css"))
        self.styles = styles

    def make(self, content):
        hljs = """
            <style>{}</style>
            <script>{}</script> 
            """.format(self.highlightjs_css, self.highlightjs_js)

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
