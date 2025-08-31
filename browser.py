import os
from PyQt5.QtWidgets import (
    QMainWindow, QToolBar, QLineEdit, QAction, QTabWidget, QWidget, 
    QVBoxLayout, QMessageBox, QStyle
)
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from tab import BrowserTab

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IbraVim Browser")
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.SP_ComputerIcon)))
        self.setMinimumSize(1024, 768)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.setMovable(True)
        layout.addWidget(self.tabs)
        
        self.create_navigation_toolbar()
        self.add_new_tab(self.get_home_url(), "Home")
        self.showMaximized()

    def get_home_url(self):
        """Get URL for home page"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        home_file = os.path.join(current_dir, 'resources', 'home.html')
        
        if os.path.exists(home_file):
            return QUrl.fromLocalFile(home_file)
        else:
            return QUrl("https://duckduckgo.com")

    def create_navigation_toolbar(self):
        navtb = QToolBar("Navigation")
        navtb.setMovable(False)
        navtb.setIconSize(QSize(24, 24))
        self.addToolBar(navtb)
        
        # New tab button
        new_tab_btn = QAction(self.style().standardIcon(QStyle.SP_FileIcon), "New Tab", self)
        new_tab_btn.setShortcut(QKeySequence.AddTab)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        navtb.addAction(new_tab_btn)
        navtb.addSeparator()
        
        # Navigation buttons
        back_btn = QAction(self.style().standardIcon(QStyle.SP_ArrowBack), "Back", self)
        back_btn.setShortcut(QKeySequence.Back)
        back_btn.triggered.connect(lambda: self.current_webview().back())
        navtb.addAction(back_btn)
        
        forward_btn = QAction(self.style().standardIcon(QStyle.SP_ArrowForward), "Forward", self)
        forward_btn.setShortcut(QKeySequence.Forward)
        forward_btn.triggered.connect(lambda: self.current_webview().forward())
        navtb.addAction(forward_btn)
        
        reload_btn = QAction(self.style().standardIcon(QStyle.SP_BrowserReload), "Reload", self)
        reload_btn.setShortcut(QKeySequence.Refresh)
        reload_btn.triggered.connect(lambda: self.current_webview().reload())
        navtb.addAction(reload_btn)
        
        home_btn = QAction(self.style().standardIcon(QStyle.SP_DirHomeIcon), "Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)
        navtb.addSeparator()
        
        # Address bar
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        
        # Go button
        search_btn = QAction(self.style().standardIcon(QStyle.SP_CommandLink), "Go", self)
        search_btn.triggered.connect(self.navigate_to_url)
        navtb.addAction(search_btn)
        navtb.addSeparator()
        
        # Bookmarks
        from bookmarks import create_bookmarks_menu
        bookmarks_btn = create_bookmarks_menu(self)
        navtb.addAction(bookmarks_btn)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = self.get_home_url()
        
        browser = BrowserTab(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        
        browser.webview.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.webview.loadFinished.connect(lambda _, i=i, browser=browser: 
            self.tabs.setTabText(i, browser.webview.page().title()[:15] + "..."))
        
        self.urlbar.setFocus()

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        if i >= 0:
            qurl = self.current_webview().url()
            self.update_urlbar(qurl, self.current_webview())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            self.close()
        else:
            self.tabs.removeTab(i)

    def navigate_home(self):
        self.current_webview().setUrl(self.get_home_url())

    def navigate_to_url(self):
        url_text = self.urlbar.text()
        
        if not (url_text.startswith('http://') or url_text.startswith('https://') or 
                '.' in url_text and ' ' not in url_text):
            url_text = 'https://duckduckgo.com/?q=' + url_text.replace(' ', '+')
        else:
            if not url_text.startswith('http'):
                url_text = 'https://' + url_text
                
        self.current_webview().setUrl(QUrl(url_text))

    def update_urlbar(self, q, browser=None):
        if browser != self.current_webview():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def current_webview(self):
        return self.tabs.currentWidget().webview

    def closeEvent(self, event):
        if self.tabs.count() > 1:
            reply = QMessageBox.question(self, 'Confirm Close', 
                                        'Are you sure you want to close the browser?',
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                event.ignore()
                return
        event.accept()
