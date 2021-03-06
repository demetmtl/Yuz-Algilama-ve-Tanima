import cv2
import json

tani = cv2.face.LBPHFaceRecognizer_create()
tani.read('trainer.yml') #eğitim dosyası okunur
cascadePath = 'C:/Users/DEMET/Desktop/Face-Recognition-with-Deep-Based-Computer-Vision-master/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX #yüz sahibi ismi yazı fontu
id = 0

dictionary = {} #okunan id'ler buraya atanır
names = []
dosya = open('ids.json','r')
dictionary = json.load(dosya)
cam = cv2.VideoCapture(0)

#ret, cerceve =cam.read()
#cerceve = cv2.flip(cerceve,1)

def cam_tani(cerceve):

    for key, value in dictionary.items():
        names.append(key)

    while True:

        gri = cv2.cvtColor(cerceve, cv2.COLOR_BGR2GRAY)
    #görüntüde yüzü çerçeve ile yakalama
        faces = faceCascade.detectMultiScale(gri,scaleFactor=1.5,minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(cerceve, (x, y), (x + w, y + h), (255, 0, 0), 2)
            id ,oran = tani.predict(gri[y:y+h, x:x+w])
            print(id, ' ', oran)

            if (oran > 70):
                id = names [id]
            else:
                id = 'Bilinmiyor'
            cv2.putText(cerceve, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.waitKey(20)
            return cerceve
"""       cv2.imshow('Kamera', cerceve)
        k = cv2.waitKey(10) & 0xff
        if k == 27: # cv2.waitKey(1) & 0xFF == ord('q'):  # klavyeden q'ya bastığımızda çıkıyor.
            break
    cam.release()
    cv2.destroyAllWindows()"""

















