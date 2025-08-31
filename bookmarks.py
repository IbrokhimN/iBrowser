from PyQt5.QtWidgets import QMenu, QAction, QStyle
from PyQt5.QtCore import QUrl

def create_bookmarks_menu(parent):
    bookmarks_menu = QMenu(parent)
    bookmarks_menu.setTitle("Bookmarks")
    
    # Add some default bookmarks
    bookmarks = {
        "DuckDuckGo": "https://duckduckgo.com",
        "YouTube": "https://youtube.com",
        "GitHub": "https://github.com",
        "Reddit": "https://reddit.com"
    }
    
    for name, url in bookmarks.items():
        action = QAction(name, parent)
        action.triggered.connect(lambda checked, url=url: parent.current_webview().setUrl(QUrl(url)))
        bookmarks_menu.addAction(action)
    
    bookmarks_btn = QAction(parent.style().standardIcon(QStyle.SP_DirLinkIcon), "Bookmarks", parent)
    bookmarks_btn.setMenu(bookmarks_menu)
    return bookmarks_btn
