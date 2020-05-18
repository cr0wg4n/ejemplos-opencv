import cv2
import numpy as np

img = cv2.imread('dataset/prueba_1.jpg')
src = cv2.medianBlur(img, 5)
src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(src, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=50, param2=30, minRadius=0, maxRadius=0)

# Redondeando unidades
circles = np.uint16(np.around(circles))

# circles => [posición en X, posición en Y, tamaño]
for i in circles[0,:]:
    # dibujando bordes
    cv2.circle(img, (i[0], i[1]), i[2], (0,255,0), 2) 
    # dibujando contornos 
    cv2.circle(img, (i[0], i[1]), 2, (0,0,255), 3)

cv2.imshow('Imagenes detectadas', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
