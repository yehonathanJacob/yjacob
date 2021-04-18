import cv2 as cv

cap = cv.VideoCapture(0)
cap.set(3,800)
cap.set(4,450)
cap.set(10,150)

def draw_contours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv.contourArea(cnt)
        print(area)
        cv.drawContours(img, cnt, -1, (255,0,0), 3)

while True:
    scusses, img = cap.read()
    if scusses:
        draw_contours(img)

        cv.imshow("WebCam", img)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break