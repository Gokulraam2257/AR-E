import cv2 as cv
from cv2 import aruco
from random import randint
import numpy as np
marker = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

MARKER_SIZE = 400 #pixeles

'''id = randint(20 ,50)
print(id)
marker_img = aruco.generateImageMarker(marker,id,MARKER_SIZE)
cv.imwrite(f"./Marker-{id}.png" ,marker_img)
cv.imshow("Test", marker_img)
cv.waitKey(0)
cv.destroyAllWindows()'''
for id in range(20):
	marker_img = aruco.generateImageMarker(marker,id,MARKER_SIZE)
	cv.imwrite(f"./Markers/Marker-{id}.png" ,marker_img)
cv.destroyAllWindows()
	

	