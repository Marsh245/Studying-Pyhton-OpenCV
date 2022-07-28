# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
import mediapipe as mp
import time

#camera port is 0
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) # camera capturing object

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
 success, img = cap.read()
 imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 results = hands.process(imgRGB)

 print(results.multi_hand_landmarks)
 # previous time
 pTime = 0
 # current time
 cTime = 0

 if results.multi_hand_landmarks:
    for handLMs in results.multi_hand_landmarks:
        # getting information about the hand (x and y )
        for id, lm in enumerate(handLMs.landmark):
             #print(id,lm)
             height, width, c = img.shape
             # position of the center of the hand landmar
             cx, cy = int(lm.x * width), int(lm.y * height)

             print("id:",id, ",CX:", cx,",CY:",cy)
             #drawing a circle in the landmark /0  for the very bottom
             if id == 0:
              cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)



        mpDraw.draw_landmarks(img, handLMs, mpHands.HAND_CONNECTIONS)


 cTime = time.time()
 fps = 1/(cTime-pTime)
 pTime = cTime

 #writing the FPS  on the screen
 cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)



 cv2.imshow("Image", img)
 cv2.waitKey(1)
