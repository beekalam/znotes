import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QPlainTextEdit, QLineEdit, \
    QHBoxLayout, QAction, QMainWindow
from PyQt5.QtWidgets import QTabWidget
import sys

from utils import build_file_list, search, read_file_content, file_put_content
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension


class Notes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 QListWidget"
        self.InitializeUI()
        self.show()

    def InitializeUI(self):
        pass


App = QApplication(sys.argv)
window = Notes()
sys.exit(App.exec())
