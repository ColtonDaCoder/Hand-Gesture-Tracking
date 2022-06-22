import cv2
import mediapipe as mp
import time
import os
import math
import json
import gesture
from handler import handler


cap = cv2.VideoCapture(0)

handle = handler()
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

"example comment"
L = gesture.getGesture("L")#right
HAND = gesture.getGesture("hand")#left
ROCK = gesture.getGesture("rock")#right
OK = gesture.getGesture("ok")#right
FLIP = gesture.getGesture("flip")#right
gesture_list = [FLIP, L,HAND,ROCK,OK]

def checkGestures(gestures, radii_list):
    tolerance = 0.1
    gesture_dict = {g.name: g.cords for g in gestures} 
    for index, radius in enumerate(radii_list):
        temp = []
        for name, cords in gesture_dict.items():    
            #if not within tolerance for radius pop the gesture
            if len(cords) <= index or abs(radius - cords[index]) > tolerance:
                temp.append(name)
        for name in temp:
            gesture_dict.pop(name)
    return list(gesture_dict.keys())

def checkGesture(gesture, radii_list):
    tolerance = 0.1
    for index, ideal in enumerate(gesture.cords):
        print(index)
        #if not within tolerance for radius pop the gesture
        if len(radii_list) <= index or abs(radii_list[index] - ideal) > tolerance:
            return False
    return True


Handcounter = 0
Lcounter = 0
gesture_label = None

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        handle.update(results.multi_handedness, results.multi_hand_landmarks, lambda pass_lms: mpDraw.draw_landmarks(img, pass_lms, mpHands.HAND_CONNECTIONS))
        gesture_label = "idle"

        gestures_list = checkGestures(gesture_list, handle.right_hand.radii)
        for g in gestures_list:
            gesture_label = g
    else:
        gesture_label = None
    
    img = cv2.flip(img,1)
    cv2.putText(img,str(gesture_label), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow('Filtered', img)
    cv2.waitKey(1)

 
