# Face Detection
import os

import cv2

CASCADES_TUPLE = [
    (haarcascade_file_name.replace('haarcascade_', '').replace('.xml', ''),
     cv2.CascadeClassifier(os.path.join(cv2.haarcascades, haarcascade_file_name)))
    for haarcascade_file_name in os.listdir(cv2.haarcascades)
    if 'haarcascade_' in haarcascade_file_name
]
cap = cv2.VideoCapture(0)
# frameWidth = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# frameHeight = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# cap.set(10, 150)

for selected_cascades in CASCADES_TUPLE:
    print(selected_cascades)

    while cap.isOpened():
        success, img = cap.read()
        if success:
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            cascade_name, cascade_detector = selected_cascades
            detections = cascade_detector.detectMultiScale(imgGray, 1.1, 4)
            for (x, y, w, h) in detections:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img, cascade_name,
                            (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 0, 0), 2)

            cv2.imshow("Result", img)
            k = cv2.waitKey(33)
            if k in [27, ord('q')]:
                exit(1)
            elif k == ord('n'):
                break
