import mediapipe as mp
import cv2
import time
import os
import math
import json
import gesture
from handler import handler
import pyautogui as pag
import actions


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
PEACE = gesture.getGesture("peace")
SAVE = gesture.getGesture("save")
gesture_list = [FLIP,L,HAND,ROCK,OK,PEACE,SAVE]

def checkGestures(gestures, radii_list):
    tolerance = 0.1
    gesture_dict = {g.name: g.cords for g in gestures} 
    #check every radius with respective index from radii_list
    for index, radius in enumerate(radii_list):
        temp = []
        #check every gesture with the current radius
        for name, cords in gesture_dict.items(): 
            #if the length of cords is long enough
            if len(cords) > index:
                #if cords[index] is not -1 and it is not within tolerance, pop the gesture 
                if not cords[index] == -1 and abs(radius - cords[index]) > tolerance:
                    temp.append(name)
        #if name is in temp then pop is from the dictionary
        for name in temp:
            gesture_dict.pop(name)
    return returnGesture(list(gesture_dict.keys()))

def checkGesture(gesture, radii_list):
    tolerance = 0.15
    for index, ideal in enumerate(gesture.cords):
        print(index)
        #if not within tolerance for radius pop the gesture
        if len(radii_list) <= index or abs(radii_list[index] - ideal) > tolerance:
            return False
    return True

def returnGesture(gesture): 
    return gesture[0] if len(gesture) == 1 else "idle"

def saveGesture(name, radii_list):
    new_gesture = gesture.newGesture(name, radii_list)
    new_gesture.toJson()

Handcounter = 0
Lcounter = 0
gesture_label = None

prevX = 0
prevT = 0.0001
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        #update hand radii and draw landmarks
        handle.update(results.multi_handedness, results.multi_hand_landmarks, lambda pass_lms: mpDraw.draw_landmarks(img, pass_lms, mpHands.HAND_CONNECTIONS))
        gesture_label = "idle1"

        #get left and right gestures
        left_gesture = checkGestures(gesture_list, handle.left_hand.radii)        
        right_gesture = checkGestures(gesture_list, handle.right_hand.radii)

        if left_gesture == "save":
            x = 10 * handle.left_hand.temp[0][0]
            actions.volume(False, int(x))

        if right_gesture == "save":
            x = 10 - 10*handle.right_hand.temp[0][0]
            actions.volume(True, int(x))


        
        #if len(handle.right_hand.temp) > 0:
        #    x = handle.right_hand.temp[0][0] 
        #    t = time.time()
        #    speed = (x-prevX) / (t-prevT)
        #    if speed > 1.5: 
        #        #pag.hotkey('ctrl', 'right')                
        #        #actions.volume(True)
        #        time.sleep(0.5)
        #    if speed < -1.5:
        #        #pag.hotkey('ctrl', 'left')
        #        actions.volume(False)
        #        time.sleep(0.5)
        #    prevX = x
        #    prevT = t

        #if left_gesture == "save":
        #    pag.hotkey('ctrl', 'left')
        #    time.sleep(0.5)
        #if right_gesture == "save":
        #    pag.hotkey('ctrl', 'right')
        #    time.sleep(0.5)
    else:
        left_gesture = "None"
        right_gesture = "None"
    
    img = cv2.flip(img,1)
    output = str(left_gesture) + " " + str(right_gesture)
    cv2.putText(img,str(output), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
    #cv2.imshow('Filtered', img)
    #cv2.waitKey(1)

 
