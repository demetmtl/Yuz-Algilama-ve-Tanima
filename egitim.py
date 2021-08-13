import cv2
import numpy as np
from PIL import Image
import os,json

yol = 'C:/Users/DEMET/Desktop/Verikoy/'
tani = cv2.face.LBPHFaceRecognizer_create() #LBP yöntemi
detector = cv2.CascadeClassifier('C:/Users/DEMET/PycharmProjects/yuztanima/haarcascade_frontalface_default.xml')

def getImagesAndLabels(yol):
    faceSamples=[]
    ids = []
    labels = []
    klasorler = os.listdir(yol)
    dictionary = {}

    for i, k1 in enumerate(klasorler):
        dictionary[k1] = int(i)

    f = open("ids.json", "w")#id'lerin tutlacağı yer
    a = json.dump(dictionary,f)
    f.close()

    for k1 in klasorler:
        for res in os.listdir(os.path.join(yol,k1)):
            PIL_img = Image.open(os.path.join(yol,k1,res)).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(dictionary[k1])
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)
    return faceSamples, ids

faces,ids = getImagesAndLabels(yol)

tani.train(faces, np.array(ids))
tani.write('trainer.yml')











