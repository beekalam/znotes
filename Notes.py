import sys
import os
import urllib.parse

import markdown
from PyQt5 import QtGui, Qt
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import QApplication, QListWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, \
    QAction, QMainWindow, QDockWidget, QStatusBar, QWidget, QToolBar, QPushButton, QTextEdit
from PyQt5.QtWidgets import QTabWidget
from mdx_gfm import GithubFlavoredMarkdownExtension

from FileStorage import FileStorage
from HightlightJSHtmlDocument import HighlightJSHtmlDocument
from NewNote import NOTES_PATH, NewNote


class Notes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.list = QListWidget()
        self.web_view = QWebEngineView()
        self.noteContent = QPlainTextEdit()
        # self.noteContent = QTextEdit()
        self.noteContent.setFont(QtGui.QFont("Ubuntu Mono", 13))
        self.tab_bar = QTabWidget(self, tabsClosable=True)
        self.tab_bar.tabCloseRequested.connect(self.removeTab)
        self.search = QLineEdit(self)
        self.htmlDocument = HighlightJSHtmlDocument()
        self.current_note_path = None
        self.fs = FileStorage(NOTES_PATH)
        # Profile sharing
        self.profile = QWebEngineProfile()
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")

        self.InitializeUI()

    def removeTab(self, index):
        if (index > 1):
            self.tab_bar.removeTab(index)

    def InitializeUI(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Notes List")

        self.createSearchWidget()
        self.createNotePreview()
        self.createNoteList()
        self.createMenu()
        self.createStatusBar()

        self.setTabOrder(self.search, self.list)
        self.new = QPushButton('New')
        self.tab_bar.setCornerWidget(self.new)
        #############################################################
        navigation = self.addToolBar('Navigation')
        style = self.style()
        self.back = navigation.addAction('Back')
        self.back.setIcon(style.standardIcon(style.SP_ArrowBack))
        self.forward = navigation.addAction('Forward')
        self.forward.setIcon(style.standardIcon(style.SP_ArrowForward))
        self.reload = navigation.addAction('Reload')
        self.reload.setIcon(style.standardIcon(style.SP_BrowserReload))
        self.stop = navigation.addAction('Stop')
        self.stop.setIcon(style.standardIcon(style.SP_BrowserStop))
        self.urlbar = QLineEdit()
        navigation.addWidget(self.urlbar)
        self.go = navigation.addAction('Go')
        self.go.setIcon(style.standardIcon(style.SP_DialogOkButton))

        self.back.triggered.connect(self.on_back)
        self.forward.triggered.connect(self.on_forward)
        self.reload.triggered.connect(self.on_reload)
        self.stop.triggered.connect(self.on_stop)
        self.urlbar.returnPressed.connect(self.on_go)
        self.go.triggered.connect(self.on_go)
        self.new.clicked.connect(self.addBrowserTab)

        ###############################################################################f

        self.show()

    def on_back(self):
        if isinstance(self.tab_bar.currentWidget(), QWebEngineView):
            self.tab_bar.currentWidget().back()

    def on_forward(self):
        if isinstance(self.tab_bar.currentWidget(), QWebEngineView):
            self.tab_bar.currentWidget().forward()

    def on_reload(self):
        if isinstance(self.tab_bar.currentWidget(), QWebEngineView):
            self.tab_bar.currentWidget().reload()

    def on_stop(self):
        if isinstance(self.tab_bar.currentWidget(), QWebEngineView):
            self.tab_bar.currentWidget().stop()

    def on_go(self):
        if (self.tab_bar.currentIndex() > 1):
            url = self.urlbar.text() if self.urlbar.text().startswith("http") else "http://" + self.urlbar.text()
            self.tab_bar.currentWidget().load(QUrl(url))

    def create_new_note(self):
        print('on new note')
        dialog = NewNote(self)
        dialog.closeEvent = self.onNewNoteClosed

        widget = self.tab_bar.currentWidget()  # type: QWebEngineView
        if isinstance(widget, QWebEngineView):
            if selectedText := widget.page().selectedText():
                title = widget.page().title()
                dialog.set_title(title)
                url = widget.page().requestedUrl().toString()
                url = url + "#:~:text=" + urllib.parse.quote(selectedText[0:100])
                dialog.set_content(selectedText + "\n\n" + url)

        dialog.show()

    def onNewNoteClosed(self, event):
        # todo update notes list here.
        print("in........................")

    def createMenu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')

        self.new_act = QAction('New Note', self)
        self.new_act.setShortcut('Ctrl+N')
        self.new_act.triggered.connect(self.create_new_note)
        file_menu.addAction(self.new_act)

        self.save_act = QAction('Save', self)
        self.save_act.setShortcut('Ctrl+S')
        self.save_act.triggered.connect(self.update_current_note)
        file_menu.addAction(self.save_act)

        self.find_act = QAction('Find', self)
        self.find_act.setShortcut('Ctrl+F')
        self.find_act.triggered.connect(self.focus_search)
        file_menu.addAction(self.find_act)

        self.exit_act = QAction('Exit', self)
        self.exit_act.setShortcut('Ctrl+Q')
        self.exit_act.setStatusTip('Quit program')
        self.exit_act.triggered.connect(self.close)
        file_menu.addAction(self.exit_act)

    def focus_search(self):
        self.search.setFocus()

    def createStatusBar(self):
        self.setStatusBar(QStatusBar(self))

    def createSearchWidget(self):
        dock_widget = QDockWidget()
        dock_widget.setWindowTitle('Search')
        dock_widget.setAllowedAreas(Qt.AllDockWidgetAreas)

        self.search.returnPressed.connect(self.doSearch)
        self.search.setFixedHeight(50)
        dock_widget.setWidget(self.search)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

    def createNotePreview(self):

        self.tab_bar.addTab(self.noteContent, "note")
        self.web_view.setHtml("")
        page = QWebEnginePage(self.profile, self.web_view)
        self.web_view.setPage(page)
        self.web_view.createWindow = self.addBrowserTab

        tab_content_widget = QWidget()
        vbox = QVBoxLayout()

        tool_bar = QToolBar("Addressbar")

        address_line = QLineEdit()
        address_line.setText("Preview")
        tool_bar.addWidget(address_line)
        vbox.addWidget(tool_bar)

        vbox.addWidget(self.web_view)

        tab_content_widget.setLayout(vbox)
        self.tab_bar.addTab(tab_content_widget, "preview")

        # self.tab_bar.addTab(self.web_view, "preview")
        self.setCentralWidget(self.tab_bar)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        print('in on context menu event')
        print(event)

    def selectionChanged(self):
        print('in selection chagned')

    def addBrowserTab(self, *args):
        webview = QWebEngineView()
        page = QWebEnginePage(self.profile, webview)
        page.createStandardContextMenu()
        webview.setPage(page)
        webview.createWindow = self.addBrowserTab
        webview.setHtml("""
            <h1>Blank Tab</h1>
            <p>
                <a href="https://google.com">google</a>
                <a href="https://www.php.net/manual/en/function.sqlsrv-next-result.php">phplink</a>
            </p>
        """)
        tab_index = self.tab_bar.addTab(webview, 'New tab')
        ##########################
        # menu = webview.page().createStandardContextMenu()
        # hit = webview.page().currentFrame().hitTestContent(event.pos())
        # url = hit.linkUrl()
        # if url.isValid():
        #     self.newTabAction.setData(url)
        #     menu.addAction(self.newTabAction)
        # menu.exec_(event.globalPos())
        ###################
        return webview

    def createNoteList(self):
        dock_widget = QDockWidget()
        dock_widget.setWindowTitle('Notes')
        dock_widget.setAllowedAreas(Qt.AllDockWidgetAreas)

        dock_widget.setWidget(self.list)
        for i, path in enumerate(self.fs.all().keys()):
            self.list.insertItem(i, path)
        self.list.currentRowChanged.connect(self.listview_clicked)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

    def listview_clicked(self):
        item = self.list.currentItem()
        if item is not None and item.text() is not None:  # and os.path.isfile(item.text()):
            self.update_current_note()
            self.current_note_path = item.text()
            self.statusBar().showMessage(self.current_note_path)

            content = self.fs.getNote(self.current_note_path)
            self.noteContent.setPlainText(content)
            self.update_note_markdown_preview(content)

    def update_note_markdown_preview(self, content):
        try:
            markdown_content = markdown.markdown(content, extensions=[GithubFlavoredMarkdownExtension()])
            self.web_view.setHtml(self.htmlDocument.make(markdown_content))
        except Exception as e:
            print(str(e))

    def update_current_note(self):
        if self.current_note_path is not None:  # and read_file_content(self.current_note_path) != self.noteContent.toPlainText():
            self.fs.updateNote(self.current_note_path, self.noteContent.toPlainText())
            # self.fs.updateNote(self.get_current_note_file_name(), self.noteContent.toPlainText())
            # file_put_content(self.current_note_path, self.noteContent.toPlainText())
            self.update_note_markdown_preview(self.noteContent.toPlainText())

    def doSearch(self):
        self.list.clear()
        if self.search.text() == "":
            for i, path in enumerate(self.fs.all().keys()):
                self.list.insertItem(i, path)
        else:
            # res = search(self.search.text())
            self.fs.searchNotes(self.search.text())
            for i, path in enumerate(self.fs.getNotes()):
                self.list.insertItem(i, path)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Notes()
    sys.exit(App.exec())
