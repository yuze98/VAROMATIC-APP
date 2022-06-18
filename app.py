from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import QtCore
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
                    return mainProcess(True,'new2',self.Qcombo3.currentText())
                else:
                    return mainProcess(False,'new2',self.Qcombo3.currentText())
            else:
               return GoalLineProcess('rec')
        
        self.label_name = QLabel('CAMERA', self)
        self.label_name.setStyleSheet("""QLabel{
        color: white;
        font: 14pt;
        text-align:center;
        }""")
        self.label_name.setFixedSize(100,20)
        self.label_name.move(760,25)

        self.Qcombo = QComboBox(self)
        self.Qcombo.addItem("Camera 1")
        self.Qcombo.addItem("Camera 2")
        self.Qcombo.setFixedSize(100,50)
        self.Qcombo.move(750,50)

        self.label_name = QLabel('TECHNIQUE', self)
        self.label_name.setStyleSheet("""QLabel{
        color: white;
        font: 14pt;
        text-align:center;
        }""")
        self.label_name.setFixedSize(100,20)
        self.label_name.move(50,25)

        self.Qcombo2 = QComboBox(self)
        self.Qcombo2.addItem("Image Processing")
        self.Qcombo2.addItem("YOLO")
        self.Qcombo2.setFixedSize(120,50)
        self.Qcombo2.move(50,50)

        self.label_name = QLabel('ATTACK DIRECTION', self)
        self.label_name.setStyleSheet("""QLabel{
        color: white;
        font: 14pt;
        text-align:center;
        }""")
        self.label_name.setFixedSize(200,20)
        self.label_name.move(50,125)

        self.Qcombo3 = QComboBox(self)
        self.Qcombo3.addItem("right")
        self.Qcombo3.addItem("left")
        self.Qcombo3.setFixedSize(120,50)
        self.Qcombo3.move(50,150)
        
        self.pushButton = QPushButton("Activate",self)
        self.pushButton.setFixedSize(200,50)
        self.pushButton.move(350,500)   
        self.pushButton.clicked.connect(activate)
        self.pushButton.setIcon(QIcon('assets/logobg.jpg'))
        self.pushButton.setIconSize(QtCore.QSize(64, 64))
        self.pushButton.setStyleSheet("""QPushButton{
        font: 14pt;
        text-align:center;
        background-image:url("D:/UNI STUFF/Fourth year comp/sem 2/GGP/VAROMATIC-APP/assets/grass.jpg");
        }""")

        label = QLabel(self)
        pixmap = QPixmap('assets/logobg.jpg')
        label.setPixmap(pixmap)
        label.setFixedHeight(500)
        label.setFixedWidth(500)
        label.move(235,0)
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
    window.setWindowTitle("VAROMATIC")
    window.resize(900,700)
    window.show()
    sys.exit(app.exec_())
