from ursina import *
import cv2 as cv
from PIL import Image as im
from cv2 import aruco
from direct.actor.Actor import Actor
import numpy as np


app = Ursina()
window.size=(800,800)
v=Entity(model="quad",position=(0,0,10),scale=15,color=color.white)
cap = cv.VideoCapture(0)
ent=Entity(scale=2,collider="mesh",enabled = False)
actor = Actor('./kelvin.glb')
actor.setPos(0,-0.05,0)
#actor.setHpr(actor,0,90,180)
actor.reparent_to(ent)
imsize = (800,600)

cv_file = cv.FileStorage('calibration_chessboard.yaml', cv.FILE_STORAGE_READ) 
mtx = cv_file.getNode('K').mat()
dst = cv_file.getNode('D').mat()
cv_file.release()
world_points = np.array([[0.,0.,0.],
    							[2.5,0.,0.],
    							[2.5,0.,0.],
    							[0.,2.5,0.]], dtype=np.float32)

def estimatePoseSingleMarkers(corners, marker_size, mtx, ortion):

    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []
    for c in corners:
        nada, R, t = cv.solvePnP(marker_points, c, mtx, ortion, False, cv.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash         

def update():    
    ret, frame = cap.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    ent.enabled = False
    marker = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    param_marker = aruco.DetectorParameters()
    MARKER_SIZE = 400 #pixeles
    detector = aruco.ArucoDetector(marker,param_marker)
    frame.flags.writeable = True

    
    
    if not ret:
        quit()
        
    gray =  cv.cvtColor(frame,cv.COLOR_BGR2GRAY) #frame, cv.COLOR_BGR2RGB
    corners, ids, rejected = detector.detectMarkers(gray)
    if corners:
        ent.enabled = True 
        #print(ids)
        tot = range(0,ids.size)
        for id,cor,i in zip(ids,corners,tot) :
           
            cv.polylines(frame,[cor.astype(np.int32)],True,(0,255,255),4,cv.LINE_AA)
            cor = cor.reshape(4,2)
            cor = cor.astype(int)
            top_right = cor[0].ravel()
            
    
            rvecs, tvecs, markerPoints = estimatePoseSingleMarkers(corners, 0.05, mtx, dst)
            
            cv.putText(frame , f"id:{id[0]} dist:{tvecs[i][0]}", top_right , cv.FONT_HERSHEY_PLAIN,1.3,(0,255,0),2,cv.LINE_AA)
            #image_augmantation(frame,img_vid,cor)
            
            #print(rvec,tvec,markerPoints)
            for rvec, tvec in zip(rvecs, tvecs):
                
                # Convert the rotation vector to a rotation matrix
                rotation_matrix, _ = cv.Rodrigues(rvec)

                
                
          
                cv.drawFrameAxes(frame, mtx, dst, rvec, tvec,0.5) 
                ent.position = (-tvec[0],tvec[1],-tvec[2])
    frame=cv.flip(frame, 1)
    data = im.fromarray(frame)
    data= data.convert("RGBA")
    av=Texture(data)
    v.texture=av
    
def input(key):
    if key=='q':
        application.quit()

EditorCamera()
app.run()