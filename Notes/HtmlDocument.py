class HtmlDocument:
    def __init__(self) -> None:
        self.jsContent = ""
        self.cssContent = ""

    def addJS(self, js):
        self.jsContent = self.jsContent + "<script>{}</script>".format(js)

    def addCSS(self, style):
        self.cssContent = self.jsContent + "<style>{}</style>".format(style)

    def make(self, content):
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
        """.format(self.cssContent, content, self.jsContent)
        return html
