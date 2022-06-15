from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# def window():
#     app = QApplication(sys.argv)
#     win = QMainWindow()
#     win.setGeometry(200,200,300,300)
#     win.setWindowTitle('Varomatic APP')

#     win.show()
#     sys.exit(app.exec_())

# window()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.pushButton1 = QPushButton("Button 1", self.centralwidget)
        self.pushButton2 = QPushButton("Button 2", self.centralwidget)

        lay = QHBoxLayout(self.centralwidget)
        lay.addWidget(self.pushButton1)
        lay.addWidget(self.pushButton2)


stylesheet = """
    MainWindow {
        background-image: url("D:/UNI STUFF\/fourth year/sem 2/GGP/VAROMATIC-APP/assets/logo.jpg"); 
        background-repeat: no-repeat; 
        background-position: top;
    }
"""

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)     # <---
    window = MainWindow()
    window.resize(640, 640)
    window.show()
    sys.exit(app.exec_())