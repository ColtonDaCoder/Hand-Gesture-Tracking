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


L = gesture.getGesture("L")#right
HAND = gesture.getGesture("hand")#left
ROCK = gesture.getGesture("rock")#right
OK = gesture.getGesture("ok")#right
FLIP = gesture.getGesture("flip")#right
gesture_list = [L,HAND,ROCK,OK]

def checkGestures(gesture_dict, radii_list):
    tolerance = 0.8
    for key in list(gesture_dict):
        for dict in gesture_dict.get(key):
            index = dict.get('index')
            ideal = dict.get('radius')
            #if not within tolerance for radius pop the gesture
            if not abs(radii_list[index] - ideal) < tolerance:
                gesture_dict.pop(key)
    print(gesture_dict)




# def checkGesture(gesture, radii_list):
#     tolerance = 0.05
#     for cord in gesture:
#         index = cord.get('index')
#         ideal = cord.get('radius')
#         #if not within tolerance for radius pop the gesture
#         if len(radii_list) <= index or not abs(radii_list[index] - ideal) < tolerance:
#             return False
#     return True



def checkGesture(gesture, radii_list):
    tolerance = 0.1
    for index, ideal in enumerate(gesture.cords):
        #if not within tolerance for radius pop the gesture
        if len(radii_list) <= index or not abs(radii_list[index] - ideal) < tolerance:
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
        handle.update(
            results.multi_handedness, 
            results.multi_hand_landmarks, 
            lambda pass_lms: mpDraw.draw_landmarks(img, pass_lms, mpHands.HAND_CONNECTIONS)
        )
        gesture_label = "idle"

        if checkGesture(FLIP, handle.right_hand.radii):
            gesture_label = "flip"


        # if checkGesture(L, handle.right_hand.radii):
        #     gesture_label = "L"

        # if checkGesture(ROCK, handle.right_hand.radii):
            
       # for g in gesture_list:
        #     if checkGesture(g, handle.right_hand.radii):
        #         gesture_label = g.name
        # if Lcounter > 10:
        #     exit()
    else:
        gesture_label = None
    
    img = cv2.flip(img,1)
    cv2.putText(img,str(gesture_label), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    cv2.imshow('Filtered', img)
    cv2.waitKey(1)

 
