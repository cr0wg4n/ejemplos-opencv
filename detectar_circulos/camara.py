import cv2
import numpy as np
import time

def filtro_fail(img):
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  _, mask = cv2.threshold(gray,50,255,cv2.THRESH_BINARY)
  circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=50, param2=30, minRadius=0, maxRadius=0)
  for i in circles[0,:]:
    cv2.circle(mask, (i[0], i[1]), i[2], (0,255,0), 2) 
    # cv2.circle(mask, (i[0], i[1]), 2, (0,0,255), 3)      
  return mask

video = cv2.VideoCapture(0)
## Parámetros Importantes
# 10 Brillo
# 11 Contraste
# 12 Saturación
# https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
# https://www.it-swarm.dev/es/python/configuracion-de-los-parametros-de-la-camara-en-opencvpython/1068172896/
video.set(3,1280)  # Ancho
video.set(4,1024)  # Alto 
video.set(15, 0.1) # Exposicion

while True:
  ret, img = video.read()
  img = filtro_fail(img)
  cv2.imshow("demo camarin", img)
  key = cv2.waitKey(10) # 10 microsegundos de delay
  # key => ASCII 
  # https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/ASCII-Table-wide.svg/1200px-ASCII-Table-wide.svg.png
  # 27 es escape segun la tabla
  if key == 27: 
    break 

cv2.destroyAllWindows()
cv2.VideoCapture(0).release()