# -*- coding: utf-8 -*-
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
from PyQt5.QtCore import QTimer, pyqtSignal, QThread, pyqtSlot, Qt
from sonuc import cam_tani
from veri import cam_veri
import os, json
import numpy as np
from PIL import Image

class VeriThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.release()
        while True:
            faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            ret, frame = cap.read()

            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                faces = faceCascade.detectMultiScale(
                    rgbImage,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class SonucThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):

        cam = cv2.VideoCapture(0)

        tani = cv2.face.LBPHFaceRecognizer_create()
        tani.read('trainer.yml')  # eğitim dosyası okunur
        cascadePath = 'haarcascade_frontalface_default.xml'
        faceCascade = cv2.CascadeClassifier(cascadePath)
        font = cv2.FONT_HERSHEY_SIMPLEX  # yüz sahibi ismi yazı fontu

        dictionary = {}  # okunan id'ler buraya atanır
        names = []
        dosya = open('ids.json', 'r')
        dictionary = json.load(dosya)

        for key, value in dictionary.items():
            names.append(key)

        while True:
            ret, cerceve = cam.read()
            if ret:
                cerceve_rekli = cv2.cvtColor(cerceve, cv2.COLOR_BGR2RGB)
                gri = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)
                # görüntüde yüzü çerçeve ile yakalama
                faces = faceCascade.detectMultiScale(gri, scaleFactor=1.1, minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(cerceve_rekli, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    id, oran = tani.predict(gri[y:y + h, x:x + w])
                    print(id, ' ', oran)

                    if (oran < 70):
                        id = names[id]
                    else:
                        id = 'Bilinmiyor'
                    cv2.putText(cerceve_rekli, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

                    h, w, ch = cerceve_rekli.shape
                    bytesPerLine = ch * w
                    convertToQtFormat = QImage(cerceve_rekli.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)


class SecondWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.secondwindow()
        self.timer = QTimer()
        # self.timer.timeout.connect(self.kamera_ac)
        self.timer2 = QTimer()
        # self.timer2.timeout.connect(self.kullanici_kayit)
        self.thveri = VeriThread(self)
        self.thveri.changePixmap.connect(self.setImageVeri)
        self.thveri.start()

    @pyqtSlot(QImage)
    def setImageVeri(self, image):
        self.orjinal_resim_img.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setImageSonuc(self, image):
        self.kamera_yeri.setPixmap(QPixmap.fromImage(image))

    def secondwindow(self):
        self.thveri = VeriThread(self)
        self.thveri.changePixmap.connect(self.setImageVeri)

        self.thsonuc = SonucThread(self)
        self.thsonuc.changePixmap.connect(self.setImageSonuc)


        self.resim = ''
        self.setStyleSheet("background: #efecf7;")
        self.setWindowTitle("YÜZ TANIMA SİSTEMİ")
        self.setWindowIcon(QtGui.QIcon('kamera.ico'))
        self.setMinimumSize(600, 450)
        self.setMaximumSize(600, 450)

        # Tab oluşturma
        self.table = QtWidgets.QTabWidget(self)
        self.table.setStyleSheet("border: 0px solid black;border-radius: 0px;background: #efecf7;")
        self.table.move(0, 0)
        self.table.resize(600, 405)
        self.table.setTabShape(QtWidgets.QTabWidget.TabShape(QtWidgets.QTabWidget.Triangular))

        # Anasayfaya Dön butonu
        self.anasyafaya_don_btn = QtWidgets.QPushButton(self)
        self.anasyafaya_don_btn.move(170, 410)
        self.anasyafaya_don_btn.resize(241, 30)
        self.anasyafaya_don_btn.setText("ANASAYFAYA DÖN")
        self.anasyafaya_don_btn.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0.864, x2:1, y2:0, stop:0.0965909 rgba(85, 85, 255, 255), stop:1 rgba(227, 156, 156, 255));")
        self.anasyafaya_don_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 7, QtGui.QFont.Bold))
        self.anasyafaya_don_btn.clicked.connect(self.anasayfa_clicked)

        # Veri Çekme tabı oluşturuldu.
        self.resimtab = QtWidgets.QWidget()
        self.resimtab.setStyleSheet("border: 0px solid black;border-radius: 10px;background: #efecf7;")

        # logo 3
        self.resimtab_logo = QtWidgets.QLabel(self.resimtab)
        self.resimtab_logo.setPixmap(QtGui.QPixmap('kul_ekle.ico'))
        self.resimtab_logo.setScaledContents(True)
        self.resimtab_logo.resize(50, 50)
        self.resimtab_logo.move(35, 20)

        # Orjinal Resim başlığı
        self.orjinal_resim_text = QtWidgets.QLabel(self.resimtab)
        self.orjinal_resim_text.setText("Kamera")
        self.orjinal_resim_text.setStyleSheet(
            "background-color:#461eb7;color:#ffffff;border-radius:20px;border-style: solid;")
        self.orjinal_resim_text.move(145, 85)
        self.orjinal_resim_text.resize(85, 25)
        self.orjinal_resim_text.setFont(QtGui.QFont("MS Shell Dlg 2", 6, QtGui.QFont.Bold))
        self.orjinal_resim_text.setAlignment(QtCore.Qt.AlignCenter)

        # Resmin gözükeceği yer
        self.orjinal_resim_img = QtWidgets.QLabel(self.resimtab)
        self.orjinal_resim_img.setStyleSheet("border: 5px solid black;border-radius: 10px;background: white;")
        self.orjinal_resim_img.move(85, 115)
        self.orjinal_resim_img.setScaledContents(True)
        self.orjinal_resim_img.resize(200, 200)

        self.label = QtWidgets.QLabel(self.resimtab)
        self.label.setObjectName("label")
        self.label.move(95, 30)
        self.label.resize(245, 25)
        self.label.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0.864, x2:1, y2:0, stop:0.0965909 rgba(85, 85, 255, 255), stop:1 rgba(227, 156, 156, 255));")
        self.label.setText(" Veri Almayı Başlatmak İçin Kullanıcı Adı Giriniz: ")
        self.label.setFont(QtGui.QFont("MS Shell Dlg 2", 7, QtGui.QFont.Bold))

        self.lineEdit = QtWidgets.QLineEdit(self.resimtab)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.move(350, 30)
        self.lineEdit.resize(125, 25)
        self.lineEdit.setEnabled(True)
        self.lineEdit.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0.864, x2:1, y2:0, stop:0.0965909 rgba(85, 85, 255, 255), stop:1 rgba(227, 156, 156, 255));")

        self.lineEdit.returnPressed.connect(self.thveri.start)

        # Alınan Frame Başlığı
        self.alinan_frame_text = QtWidgets.QLabel(self.resimtab)
        self.alinan_frame_text.setText("Alınan Frame")
        self.alinan_frame_text.setStyleSheet(
            "background-color:#461eb7;color:#ffffff;border-radius:20px;border-style: solid;")
        self.alinan_frame_text.move(330, 85)
        self.alinan_frame_text.resize(130, 25)
        self.alinan_frame_text.setFont(QtGui.QFont("MS Shell Dlg 2", 6, QtGui.QFont.Bold))
        self.alinan_frame_text.setAlignment(QtCore.Qt.AlignCenter)

        # Alınan Frame in gözükeceği yer
        self.alinan_frame_yeri = QtWidgets.QLabel(self.resimtab)
        self.alinan_frame_yeri.setStyleSheet("border: 5px solid black;border-radius: 10px;background: white;")
        self.alinan_frame_yeri.move(295, 115)
        self.alinan_frame_yeri.setScaledContents(True)
        self.alinan_frame_yeri.resize(200, 200)

        # Kullanıcıyı kaydet butonu
        self.kullaniciyi_kaydet_btn = QtWidgets.QPushButton(self.resimtab)
        self.kullaniciyi_kaydet_btn.setText("Kullanıcıyı Kaydet")
        self.kullaniciyi_kaydet_btn.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0.864, x2:1, y2:0, stop:0.0965909 rgba(85, 85, 255, 255), stop:1 rgba(227, 156, 156, 255));")
        self.kullaniciyi_kaydet_btn.move(225, 325)
        self.kullaniciyi_kaydet_btn.resize(145, 25)
        self.kullaniciyi_kaydet_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 7, QtGui.QFont.Bold))
        self.kullaniciyi_kaydet_btn.clicked.connect(self.veri_egit)

        # Kamera tabı oluşturuldu.
        self.cameratab = QtWidgets.QWidget()
        self.cameratab.setStyleSheet("border: 0px solid black;border-radius: 10px;background: #efecf7; ")

        # Yuz Tanıma başlığı
        self.yuz_tanima_text = QtWidgets.QLabel(self.cameratab)
        self.yuz_tanima_text.setText("YÜZ TANIMA KAMERASI")
        self.yuz_tanima_text.setStyleSheet(
            "background-color:#461eb7;color:#ffffff;border-radius:20px;border-style: solid;")
        self.yuz_tanima_text.move(215, 35)
        self.yuz_tanima_text.resize(150, 32)
        self.yuz_tanima_text.setFont(QtGui.QFont("MS Shell Dlg 2", 7, QtGui.QFont.Bold))
        self.yuz_tanima_text.setAlignment(QtCore.Qt.AlignCenter)

        # Kameranın Gözükeceği yer
        self.kamera_yeri = QtWidgets.QLabel(self.cameratab)
        self.kamera_yeri.setStyleSheet("border: 5px solid black;border-radius: 10px;background: white;")
        self.kamera_yeri.move(115, 75)
        self.kamera_yeri.setScaledContents(True)
        self.kamera_yeri.resize(350, 250)

        # Kamera Çalıştırma butonu
        self.kamerayi_calistir = QtWidgets.QPushButton(self.cameratab)
        self.kamerayi_calistir.setText("ÇALIŞTIR")
        self.kamerayi_calistir.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0.864, x2:1, y2:0, stop:0.0965909 rgba(85, 85, 255, 255), stop:1 rgba(227, 156, 156, 255));")
        self.kamerayi_calistir.move(190, 330)
        self.kamerayi_calistir.resize(90, 25)
        self.kamerayi_calistir.setFont(QtGui.QFont("MS Shell Dlg 2", 7, QtGui.QFont.Bold))
        self.kamerayi_calistir.clicked.connect(self.thsonuc.start)

        # Kamerayı Durdur butonu
        self.kamerayi_durdur_btn = QtWidgets.QPushButton(self.cameratab)
        self.kamerayi_durdur_btn.setText("DURDUR")
        self.kamerayi_durdur_btn.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:1, y1:0.864, x2:1, y2:0, stop:0.0965909 rgba(85, 85, 255, 255), stop:1 rgba(227, 156, 156, 255));")
        self.kamerayi_durdur_btn.move(290, 330)
        self.kamerayi_durdur_btn.resize(90, 25)
        self.kamerayi_durdur_btn.setFont(QtGui.QFont("MS Shell Dlg 2", 7, QtGui.QFont.Bold))
        self.kamerayi_durdur_btn.clicked.connect(self.thsonuc.terminate)

        self.table.addTab(self.resimtab, "Yeni Yüz Tanıtma")
        self.table.addTab(self.cameratab, "Kamera ile Yüz Tanımlama")

    """def cam_veri(self):
        cam = cv2.VideoCapture(0)  # kamera kurulumu
        # opencv ve cascade
        face_detector = cv2.CascadeClassifier('C:/Users/DEMET/PycharmProjects/yuztanima/haarcascade_frontalface_default.xml')

        # veriseti bilgileri ve kaydı
        global user
        # user = input("Kullanıcı adı giriniz: ")
        user = self.get_kullanici()

        print("/n Kameraya bakın ve bekleyin...")
        os.mkdir('C:/Users/DEMET/Dataset/'+user)

        say = 0  # frame sayısı

        while (True):
            red, cerceve = cam.read()
            cerceve = cv2.flip(cerceve, 1)

            height, width, channel = cerceve.shape
            step = channel * width
            qImg = QImage(cerceve.data, width, height, step, QImage.Format_RGB888)
            self.orjinal_goruntu_img.setPixmap(QtGui.QPixmap.fromImage(qImg))

            gri = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gri, 1.5, 5)
            # Yüz çerçevesi sınırları
            for (x, y, w, h) in faces:
                cv2.rectangle(cerceve, (x, y), (x + w, y + h), (255, 0, 0), 2)
                say += 1
                path = "C:/Users/DEMET/Dataset/" + user + "/"  # frame kaydı
                cv2.imwrite(path + str(say) + ".jpg", gri[y:y + h, x:x + w])
                cv2.imshow('Data', cerceve)
            k = cv2.waitKey(100) & 0xff
            if k == 27:  # esc basılırsa sonlandır
                break
            elif say >= 50:  # frame sayısı 50 ve üstü ise sonlandır
                break

        cam.release()
        cv2.destroyAllWindows()"""

    def veri_egit(self):
        self.yol = 'C:/Users/DEMET/Desktop/Verikoy/'
        self.tani = cv2.face.LBPHFaceRecognizer_create()  # LBP yöntemi
        self.detector = cv2.CascadeClassifier('C:/Users/DEMET/PycharmProjects/yuztanima/haarcascade_frontalface_default.xml')

        def getImagesAndLabels(yol):
            faceSamples = []
            ids = []
            labels = []
            klasorler = os.listdir(yol)
            dictionary = {}

            for i, k1 in enumerate(klasorler):
                dictionary[k1] = int(i)

            f = open("ids.json", "w")  # id'lerin tutlacağı yer
            a = json.dump(dictionary, f)
            f.close()

            for k1 in klasorler:
                for res in os.listdir(os.path.join(yol, k1)):
                    PIL_img = Image.open(os.path.join(yol, k1, res)).convert('L')
                    img_numpy = np.array(PIL_img, 'uint8')
                    id = int(dictionary[k1])
                    faces = self.detector.detectMultiScale(img_numpy)
                    for (x, y, w, h) in faces:
                        faceSamples.append(img_numpy[y:y + h, x:x + w])
                        ids.append(id)
            return faceSamples, ids

        faces, ids = getImagesAndLabels(self.yol)

        self.tani.train(faces, np.array(ids))
        self.tani.write('trainer.yml')

    def kamera_ac(self):

        ret, image = self.cap.read()
        image = cam_tani(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width, channel = image.shape
        step = channel * width
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        self.kamera_yeri.setPixmap(QtGui.QPixmap.fromImage(qImg))

    def kullanici_kayit(self):

        self.kullanici = self.lineEdit.text()
        print("alinan yazi = ", self.kullanici)

        # print("/n Kameraya bakın ve bekleyin...")
        say = 0  # frame sayısı
        os.mkdir('C:/Users/DEMET/Desktop/Verikoy/' + self.kullanici)

        ret, image2 = self.cap2.read()
        cam_veri(image2, self.kullanici)
        height, width, channel = image2.shape
        step = channel * width
        qImg = QImage(image2.data, width, height, step, QImage.Format_RGB888)
        self.orjinal_resim_img.setPixmap(QtGui.QPixmap.fromImage(qImg))

    def get_kullanici(self):
        return self.kullanici

    def yuz_bul(self):
        """img=cv2.imread(str(self.resim))
        yuz=detect(img)
        cv2.imwrite('output/output.jpg',yuz)
        self.bulunan_resimdeki_yuzler_img.setPixmap(QtGui.QPixmap('output/output.jpg'))"""

    def zaman_kontrol(self):
        print(self.timer.isActive())
        if not self.timer.isActive():
            print("devam")
            self.cap = cv2.VideoCapture(0)
            self.timer.start(200)

        else:
            self.timer.stop()
            self.cap.release()

    def zaman_kontrol2(self):
        print(self.timer2.isActive())
        if not self.timer2.isActive():
            print("devam")
            self.cap2 = cv2.VideoCapture(0)
            self.timer2.start(200)

        else:
            self.timer2.stop()
            self.cap2.release()

    def anasayfa_clicked(self):
        from mainwindow import MainWindow
        self.hide()
        self.mainwin = MainWindow()
        self.thveri.terminate()
        self.thsonuc.terminate()
        self.mainwin = MainWindow()
        self.mainwin.show()