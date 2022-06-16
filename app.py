from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import PyQt5.sip
import sys
sys.path.insert(1, 'D:/UNI STUFF/Fourth year comp/sem 2/GGP/VAROMATIC-APP/lib/offside_modules')
sys.path.insert(1, 'D:/UNI STUFF/Fourth year comp/sem 2/GGP/VAROMATIC-APP/lib/Goal_Line_modules')
from GoalLineProcess import GoalLineProcess
from Main import * 

import numpy as np
class MainWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        layout = QVBoxLayout(self)
       
        def activate():
            print(self.Qcombo.currentText())
            if self.Qcombo.currentText() == 'Camera 1':
                if self.Qcombo2.currentText() == 'YOLO':
                    return mainProcess(True,'new2')
                else:
                    return mainProcess(False,'new2')
            else:
               return GoalLineProcess()
        self.Qcombo = QComboBox(self)
        self.Qcombo.addItem("Camera 1")
        self.Qcombo.addItem("Camera 2")
        self.Qcombo.setFixedSize(100,50)
        self.Qcombo.move(750,50)

        self.Qcombo2 = QComboBox(self)
        self.Qcombo2.addItem("IP")
        self.Qcombo2.addItem("YOLO")
        self.Qcombo2.setFixedSize(100,50)
        self.Qcombo2.move(50,50)
        
        self.pushButton = QPushButton("Activate",self)
        self.pushButton.setFixedSize(100,100)
        self.pushButton.move(400,500)

        label = QLabel(self)
        pixmap = QPixmap('assets/logobg.jpg')
        label.setPixmap(pixmap)
        label.setFixedHeight(500)
        label.setFixedWidth(500)
        label.move(235,0)
        self.pushButton.clicked.connect(activate)
        lay = QHBoxLayout(self)
        lay.addWidget(self.pushButton)
        lay.addWidget(self.pushButton)

stylesheet = """
    MainWindow {
        background-image: url("D:/UNI STUFF/Fourth year comp/sem 2/GGP/VAROMATIC-APP/assets/football2.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)     # <---
    window = MainWindow()
    window.resize(900,700)
    window.show()
    sys.exit(app.exec_())
