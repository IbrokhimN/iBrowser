import sys
from PyQt5.QtWidgets import QApplication
from browser import Browser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("IbraVim Browser 🐱")
    app.setApplicationVersion("1.0")
    
    # Импортируем и применяем стиль
    from styles.dark_style import DarkStyle
    dark_style = DarkStyle()
    app.setStyle(dark_style.style)
    app.setPalette(dark_style.palette)
    
    window = Browser()
    sys.exit(app.exec_())
