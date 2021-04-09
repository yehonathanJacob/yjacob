import os

import cv2 as cv

fase_cascade_path = os.path.join(cv.haarcascades, "haarcascade_frontalface_default.xml")
fase_cascade = cv.CascadeClassifier(fase_cascade_path)

cap = cv.VideoCapture(0)
cap.set(3,800)
cap.set(4,450)
cap.set(10,150)

while True:
    scusses, img = cap.read()
    if scusses:
        faces = fase_cascade.detectMultiScale(img, 1.1, 4)

        for (x, y, w, h) in faces:
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv.imshow("WebCam", img)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break