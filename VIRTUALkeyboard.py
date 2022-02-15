# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 10:41:28 2021

@author: amalo
"""
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from cvzone import cornerRect
from pynput.keyboard import Controller 

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)


def drawAll(ListButtons,img):
    for button in ListButtons : 
        x,y = button.pos
        h,w = button.size
        cornerRect(img,(x,y,w,h),20,rt=0,colorC=(62,10,259)) # to draw the corner borders it is a function of cvzone 
        cv2.rectangle(img,button.pos,(x+w,y+h),(141,90,252),cv2.FILLED) #bgr
        cv2.putText(img,button.text,(x+15,y + 45),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
    return img

keyboard = Controller()



detector = HandDetector(detectionCon = 0.8,maxHands = 2)  # by default the confidance is 0.5 

class Button():
    def __init__(self,pos,text,size = [60,80]):
        self.pos = pos
        self.text = text
        self.size = size
    
    
        
        
        
keys = [["1","2","3","4","5","6","7","8","9","0"],
        ["A","Z","E","R","T","Y","U","I","O","P"],
        ["Q","S","D","F","G","H","J","K","L","M"],
        ["W","X","C","V","B","N",",",";",":","!"]
        ]     
ButtonList = []

for i in range(4):
    for j,key in enumerate(keys[i]):
        ButtonList.append(Button([100*j+100,80*i+300],key))  
ButtonList.append(Button([100,80*4+300]," ",(60,980)))         
finalText = ""        
        
while True:
    
    ret,frame = cap.read()
    frame = cv2.resize(frame, (1200,720)) #to resize the frame
    #detects the hand in the frame and locate the key points and draws the landmark
    hands,frame = detector.findHands(frame) 
    img  = drawAll(ButtonList, frame)
    if hands: #here we check if the hand is detected or not
        hand1 = hands[0]
        lmList1 = hand1["lmList"]
        bbox1 = hand1["bbox"]
        
        if len(hands) == 2: #checks if the other hand is used
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
        
        for button in ButtonList:
            x,y = button.pos
            h,w = button.size
            
            x1,y1 = lmList1[8] #get landmark number 8 coordinates
            
            if x<x1<x+w and y<y1<y+h: #check if your finger is in the range of the button if it is then change the color of the button
                cv2.rectangle(frame,button.pos,(x+w,y+h),(199,174,254),cv2.FILLED)
                cv2.putText(frame,button.text,(x+15,y + 45),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
                lenght,info= detector.findDistance(lmList1[8],lmList1[12])
                if lenght < 30 : #check the distance between the landmark 8 and the landmark 12 using the findDistance function , if it is less then 30 then write on the finale text
                    
                    #keyboard.press(button.text) #then open notepad and try typing with your virtual keyboard 
                    cv2.rectangle(frame,button.pos,(x+w,y+h),(62,10,259),cv2.FILLED)
                    cv2.putText(frame,button.text,(x+15,y + 45),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
                    finalText += button.text
                    sleep(1)
                    
    cv2.rectangle(frame,(50,50),(1100,120),(199,174,254),cv2.FILLED)
    cv2.putText(frame,finalText,(60,100),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
    # to find the landmarks
     
    cv2.imshow("frame",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()