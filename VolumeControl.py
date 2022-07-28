import cv2
import time
import numpy
import mediapipe as mp
import  math

import numpy as np

import HandtackingModule2 as htm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

Camwidth, HightCam = 640,480
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


cap = cv2.VideoCapture(0)
cap.set(3,Camwidth)
cap.set(4,HightCam)
previous_Time = 0
detector = htm.handDetector(detectionCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)
minimum_Vol = volRange[0]
maximum_vol = volRange[1]
vol=0
volBar=400  # zero is at 400
volPer= 0

while True:
    success, img=cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img,draw=False)
    if len(lmlist) != 0:
      #  print(lmlist[4], lmlist[8])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]

        # getting center of the line..// is floor division (dividing and rounding the number
        CX,CY = (x1+x2)//2, (y1+y2)//2



        cv2.circle(img, (x1, y1), 10,(255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10,(255, 0, 255), cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(CX, CY),10,(255,0,255),cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #Hand range 50 -300
        # volume range -65 - 0
        # converting hand range to  volume range :
        vol = np.interp(length,[50,300],[minimum_Vol,maximum_vol])
        #converting Volume bar to the image
        volBar =np.interp(length,[50,300],[400,150])
        #Volume percentage converter
        volPer = np.interp(length,[50,300],[0,100]) #from 50-300 to 0 -100
        volume.SetMasterVolumeLevel(vol, None)


        if length<50:
            cv2.circle(img, (CX, CY), 15, (0, 255, 0), cv2.FILLED)


    cv2.rectangle(img,(50,150), (85,400),(255,0,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    ################################################################

###############################################################################


    current_Time = time.time()
    fps= 1/(current_Time-previous_Time)
    previous_Time=current_Time


     #cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,scale,(Color),thickness)
    cv2.putText(img,f'FPS: {int(fps)}',(40,70),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)

    cv2.imshow("img",img)
    cv2.waitKey(1)
