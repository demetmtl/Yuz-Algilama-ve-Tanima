import cv2
import os #işletim sistemi kullanımı için

#from secondwindow import SecondWindow


cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier('C:/Users/DEMET/PycharmProjects/yuztanima/haarcascade_frontalface_default.xml')


def cam_veri(cerceve,user):
    print("girdi")
    #cam = cv2.VideoCapture(0)  # kamera kurulumu
    # opencv ve cascade

    #veriseti bilgileri ve kaydı
    #global user
    #user = input("Kullanıcı adı giriniz: ")
    #user = SecondWindow.get_kullanici()
    """print("/n Kameraya bakın ve bekleyin...")
    os.mkdir('C:/Users/furka/Dataset/'+user)"""

    say = 0  # frame sayısı


    while (True):
        #red, cerceve = cam.read()
        #cerceve=cv2.flip(cerceve, 1)
        gri = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gri, 1.1, 5)
        # Yüz çerçevesi sınırları
        for (x, y, w, h) in faces:
            cv2.rectangle(cerceve, (x, y), (x+w, y+h), (0, 255, 0), 2)
            say += 1
            path ="C:/Users/DEMET/Desktop/Verikoy/"+user+"/" #frame kaydı
            cv2.imwrite(path+str(say) + ".jpg", gri[y:y+h, x:x+w])
            """ cv2.imshow('Data', cerceve)
        k = cv2.waitKey(100) & 0xff
        if k == 27:#esc basılırsa sonlandır
            break"""
        if say >= 50:#frame sayısı 50 ve üstü ise sonlandır
            break
    return cerceve
   # cam.release()
    #cv2.destroyAllWindows()