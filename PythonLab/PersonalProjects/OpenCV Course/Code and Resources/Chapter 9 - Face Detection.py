# Face Detection
import os

import cv2

cascade_path = os.path.join(cv2.haarcascades, "haarcascade_frontalface_default.xml")
faceCascade = cv2.CascadeClassifier(cascade_path)
img = cv2.imread('Resources/lena.png')
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv2.imshow("Result", img)
cv2.waitKey(0)
