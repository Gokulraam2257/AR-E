import cv2 as cv
from cv2 import aruco
from random import randint
import numpy as np

from ursina import *

from PIL import Image as im

from direct.actor.Actor import Actor



app = Ursina()
window.size=(800,800)
v=Entity(model="quad",position=(0,0,10),scale=15,color=color.white)
cap = cv.VideoCapture(0)
ent=Entity(position=(0,0,-1),scale=25,collider="mesh")

actor = Actor('./stegosaurs_SStenops.glb')
actor.setPos(0,90,0)
#actor.setHpr(actor,0,90,180)

actor.reparent_to(ent)
actor.loop(actor.get_anim_names()[0])
imsize = (800,600)
mtx= cv2.getDefaultNewCameraMatrix(np.diag([800, 800, 1]), imsize, True)

def update():
	ret , frame = cap.read()
	marker = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
	param_marker = aruco.DetectorParameters()
	MARKER_SIZE = 400 #pixeles
	detector = aruco.ArucoDetector(marker,param_marker)
	frame.flags.writeable = True

	
	
	if not ret:
		quit()
		
	gray =  cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #frame, cv2.COLOR_BGR2RGB
	corners, ids, rejected = detector.detectMarkers(gray)
	if corners:
		#print(ids)
		for i,cor in zip(ids,corners) :
			detct = True
			cv.polylines(frame,[cor.astype(np.int32)],True,(0,255,255),4,cv.LINE_AA)
			cor = cor.reshape(4,2)
			cor = cor.astype(int)
			top_right = cor[0].ravel()
				
			ent.world_position=(0,0,1)
			cv.putText(frame , f"id:{i[0]}", top_right , cv.FONT_HERSHEY_PLAIN,1.3,(0,255,0),2,cv.LINE_AA)
				#image_augmantation(frame,img_vid,cor)
				#rvec, tvec, markerPoints = estimatePoseSingleMarkers(cor, 1, K,None)
				#print(rvec,tvec,markerPoints)
	cv.imshow(f"frame",frame)
	key = cv.waitKey(1)
	if key == ord('q'):
		quit()
	
	frame=cv.flip(frame, 1)
	data = im.fromarray(frame)
	#print(data)
	data= data.convert("RGBA")
	av=Texture(data)
	v.texture=av
	#ent.texture('./models/20430_cat_diff_v1.jpg')
def input(keys):
	if keys == ord('q'):
		quit()

EditorCamera()
app.run()