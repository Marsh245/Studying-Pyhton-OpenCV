# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
import mediapipe as mp
import time

#camera port is 0
class handDetector():
    # the class takes the parameters of the Hand the func hand
     def __init__(self, mode=False,modelComplexity=1, MaxHands = 2,detectionCon=0.5, trackCon=0.5):
         self.mode= mode #variable of the object we gonna call,  initiated
         self.MaxHands = MaxHands

         self.modeComplexity=modelComplexity
         self.detectionCon = detectionCon
         self.trackCon = trackCon

         self.mpHands = mp.solutions.hands
         self.hands = self.mpHands.Hands(self.mode, self.MaxHands,self.detectionCon, self.trackCon)
         self.mpDraw = mp.solutions.drawing_utils


     def findHands(self,img,draw=True):
         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
         results = self.hands.process(imgRGB)

         #print(results.multi_hand_landmarks)

         if results.multi_hand_landmarks:
            for handLMs in results.multi_hand_landmarks:
                # getting information about the hand (x and y )
                if draw:
                  self.mpDraw.draw_landmarks(img, handLMs, self.mpHands.HAND_CONNECTIONS)

         return img

                #for id, lm in enumerate(handLMs.landmark):
                    # print(id,lm)
                    #height, width, c = img.shape
                    # position of the center of the hand landmar
                    #cx, cy = int(lm.x * width), int(lm.y * height)

                    #print("id:", id, ",CX:", cx, ",CY:", cy)
                    # drawing a circle in the landmark /0  for the very bottom
                    # if id == 0:
                    #cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)




def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # camera capturing object
    detector = handDetector() #callig the func
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()