# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from secondwindow import SecondWindow

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mainwindow()
    def mainwindow(self):
        #Anasayfa yapısı
        self.second_window=QtWidgets.QStackedWidget()
        self.setStyleSheet("background: white;")
        self.setWindowTitle("ANASAYFA")
        self.setWindowIcon(QtGui.QIcon('kamera.ico'))
        self.setMinimumSize(600,450)
        self.setMaximumSize(600,450)
        
        #logo 1
        self.logo=QtWidgets.QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap('anasayfa.ico'))
        self.logo.setScaledContents(True)
        self.logo.resize(100,100)
        self.logo.move(195,50)

        # logo 2
        self.logo = QtWidgets.QLabel(self)
        self.logo.setPixmap(QtGui.QPixmap('anasayfa2.ico'))
        self.logo.setScaledContents(True)
        self.logo.resize(100, 100)
        self.logo.move(305, 50)
        
        #başlık
        self.baslik=QtWidgets.QLabel(self)
        self.baslik.setText("YÜZ TANIMA SİSTEMİ")
        self.baslik.setFont(QtGui.QFont("MS Shell Dlg 2", 12,QtGui.QFont.Bold))
        self.baslik.setAlignment(QtCore.Qt.AlignCenter)
        self.baslik.resize(375,95)
        self.baslik.move(100,170)
        
        #Programa geçiş butonu
        self.prog_gecis_buton=QtWidgets.QPushButton(self)
        self.prog_gecis_buton.setText(" YÜZ TANIMLAMAYA \nBAŞLA")
        self.prog_gecis_buton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:0.864, x2:1, y2:0, stop:0.0965909 rgba(85, 85, 255, 255), stop:1 rgba(227, 156, 156, 255));")
        self.prog_gecis_buton.setFont(QtGui.QFont("MS Shell Dlg 2", 8,QtGui.QFont.Bold))
        self.prog_gecis_buton.resize(125,35)
        self.prog_gecis_buton.move(225,275)

        self.prog_gecis_buton.clicked.connect(self.openWindow)
        
    def openWindow(self):
        self.hide()
        self.second=SecondWindow()
        self.second.show()
        
def main():
    app=QtWidgets.QApplication(sys.argv)
    main=MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
