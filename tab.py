from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStyle
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os

class BrowserTab(QWidget):
    def __init__(self, url=None):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.create_navigation_bar()
        
        self.webview = QWebEngineView()
        
        # If URL is not provided, use home page
        if url is None:
            url = self.get_home_url()
        elif isinstance(url, str):
            url = QUrl(url)
        
        self.webview.setUrl(url)
        self.layout.addWidget(self.webview)
        
        self.connect_buttons()
        self.webview.setZoomFactor(1.0)
        
    def get_home_url(self):
        """Get URL for home page"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        home_file = os.path.join(current_dir, 'resources', 'home.html')
        
        if os.path.exists(home_file):
            return QUrl.fromLocalFile(home_file)
        else:
            return QUrl("https://duckduckgo.com")
        
    def create_navigation_bar(self):
        self.nav_bar = QHBoxLayout()
        self.nav_bar.setContentsMargins(5, 2, 5, 2)
        
        self.back_btn = QPushButton()
        self.back_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
        self.back_btn.setFixedSize(30, 30)
        self.back_btn.setToolTip("Back")
        
        self.forward_btn = QPushButton()
        self.forward_btn.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        self.forward_btn.setFixedSize(30, 30)
        self.forward_btn.setToolTip("Forward")
        
        self.reload_btn = QPushButton()
        self.reload_btn.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.reload_btn.setFixedSize(30, 30)
        self.reload_btn.setToolTip("Reload")
        
        self.home_btn = QPushButton()
        self.home_btn.setIcon(self.style().standardIcon(QStyle.SP_DirHomeIcon))
        self.home_btn.setFixedSize(30, 30)
        self.home_btn.setToolTip("Home")
        
        self.nav_bar.addWidget(self.back_btn)
        self.nav_bar.addWidget(self.forward_btn)
        self.nav_bar.addWidget(self.reload_btn)
        self.nav_bar.addWidget(self.home_btn)
        self.nav_bar.addStretch()
        self.layout.addLayout(self.nav_bar)

    def connect_buttons(self):
        self.back_btn.clicked.connect(self.webview.back)
        self.forward_btn.clicked.connect(self.webview.forward)
        self.reload_btn.clicked.connect(self.webview.reload)
        self.home_btn.clicked.connect(self.navigate_home)

    def navigate_home(self):
        self.webview.setUrl(self.get_home_url())
