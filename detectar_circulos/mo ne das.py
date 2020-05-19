import cv2
import numpy as np
import random

img = cv2.imread('dataset/monedas.png')
src = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# desenfoque
src = cv2.GaussianBlur(src,(5,5),cv2.BORDER_DEFAULT)
cv2.imwrite('output/blur.png',src)
threshold = 90
src = cv2.Canny(src, threshold, threshold*3)
cv2.imwrite('output/canny.png',src)
contornos, jerarquia =  cv2.findContours(src.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print("hay "+str(len(contornos))+" monedas")

a_color = cv2.cvtColor(src, cv2.COLOR_GRAY2RGB)

for i in range(len(contornos)):
  cv2.drawContours(a_color, contornos, i, (random.randint(0,255), random.randint(0,255), random.randint(0,255)), 2)

cv2.imwrite('output/contornos.png',a_color)
