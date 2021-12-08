# Resize and Crop
import cv2
import numpy as np

img = cv2.imread("Resources/lambo.png")
print(img.shape)

imgResize = cv2.resize(img, (1000, 500))
print(imgResize.shape)

imgCropped = img[0:200, 200:500]

cv2.imshow("Image", img)
cv2.imshow("Image Resize",imgResize)
cv2.imshow("Image Cropped", imgCropped)
cv2.setWindowProperty('Image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty('Image Resize', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty('Image Cropped', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cv2.waitKey(0)

cv2.destroyAllWindows()


