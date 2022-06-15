from turtle import onclick
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui

import sys
sys.path.insert(1, 'D:/UNI STUFF/Fourth year comp/sem 2/GGP/VAROMATIC-APP/lib/offside_modules')
from Main import * 
import numpy as np
class MainWindow(QMainWindow):
    def __init__(self):
        QWidget.__init__(self)
        layout = QVBoxLayout(self)
        def sadFunction():
            print('saaad')
        def activate():
            print(self.Qcombo.currentText())
            if self.Qcombo.currentText() == 'Camera 1':
                return mainProcess(self)
            else:
               return sadFunction()
        self.Qcombo = QComboBox(self)
        self.Qcombo.addItem("Camera 1")
        self.Qcombo.addItem("Camera 2")
        self.Qcombo.setFixedSize(100,50)
        self.Qcombo.move(750,50)
        # self.Qcombo.currentIndexChanged.connect(selectionchange)
        
        self.pushButton = QPushButton("Activate",self)
        self.pushButton.setFixedSize(100,100)
        self.pushButton.move(400,500)

        label = QLabel(self)
        pixmap = QPixmap('assets/logo.jpg')
        label.setPixmap(pixmap)
        label.setFixedHeight(500)
        label.setFixedWidth(500)
        label.move(250,0)
        self.pushButton.clicked.connect(activate)
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
    window.resize(900,700)
    window.show()
    sys.exit(app.exec_())
# class App(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Qt live label demo")
#         self.disply_width = 640
#         self.display_height = 480
#         # create the label that holds the image
#         self.image_label = QLabel(self)
#         self.image_label.resize(self.disply_width, self.display_height)
#         # create a text label
#         self.textLabel = QLabel('Webcam')

#         # create a vertical box layout and add the two labels
#         vbox = QVBoxLayout()
#         vbox.addWidget(self.image_label)
#         vbox.addWidget(self.textLabel)
#         # set the vbox layout as the widgets layout
#         self.setLayout(vbox)

#         # create the video capture thread
#         self.thread = OffsideDetection()
#         # connect its signal to the update_image slot
#         self.thread.change_pixmap_signal.connect(self.update_image)
#         # start the thread
#         self.thread.start()



#     @pyqtSlot(np.ndarray)
#     def update_image(self, cv_img):
#         """Updates the image_label with a new opencv image"""
#         qt_img = self.convert_cv_qt(cv_img)
#         self.image_label.setPixmap(qt_img)
    
#     def convert_cv_qt(self, cv_img):
#         """Convert from an opencv image to QPixmap"""
#         rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
#         h, w, ch = rgb_image.shape
#         bytes_per_line = ch * w
#         convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
#         p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
#         return QPixmap.fromImage(p)
    
# if __name__=="__main__":
#     app = QApplication(sys.argv)
#     a = App()
#     a.show()
#     sys.exit(app.exec_())