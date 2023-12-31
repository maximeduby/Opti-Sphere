import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication


from ui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication()
    app.setWindowIcon(QIcon("resources/icons/app-icon.png"))  # set window icon
    app.setStyleSheet(open("resources/stylesheet.css").read())  # set window UI stylesheet
    window = MainWindow()
    sys.exit(app.exec())
