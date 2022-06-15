from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap

import sys
# from lib.offside_modules.Main import *

class MainWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        layout = QVBoxLayout(self)

        self.Qcombo = QComboBox(self)
        self.Qcombo.addItem("Camera 1")
        self.Qcombo.addItem("Camera 2")
        # self.cb.currentIndexChanged.connect(self.selectionchange)
        
        self.pushButton = QPushButton("Activate",self)
        self.pushButton.setFixedWidth(200)
        self.pushButton.setFixedHeight(50)
        self.pushButton.move(500,800)
        
        label = QLabel(self)
        pixmap = QPixmap('assets/logo.jpg')
        label.setPixmap(pixmap)
        # self.setCentralWidget(label)
        label.setFixedHeight(500)
        label.setFixedWidth(500)
        label.move(500,0)
        # self.pushButton.clicked.connect(mainProcess())
        lay = QHBoxLayout(self)
        lay.addWidget(self.pushButton)
        lay.addWidget(self.pushButton)


stylesheet = """
    MainWindow {
        background-color: green;
        background-image: url("D:/UNI STUFF\/fourth year/sem 2/GGP/VAROMATIC-APP/assets"); 
        background-repeat: no-repeat; 
        background-position: top;
    }
"""

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)     # <---
    window = MainWindow()
    window.resize(1280, 960)
    window.show()
    sys.exit(app.exec_())