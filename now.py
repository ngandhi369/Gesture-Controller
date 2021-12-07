import time
import tkinter.font as font
from time import sleep
from tkinter import *

import threading

import math
import cv2
import cvzone
import dlib
import mediapipe as mp
import imutils
import numpy as np
import pyautogui
import pyttsx3
import os
from cvzone.HandTrackingModule import HandDetector
from gtts import gTTS
from imutils import face_utils
from pynput.keyboard import Controller, Key
from scipy.spatial import distance as dist

from zmq.eventloop.zmqstream import ZMQStream


language = 'en'

gui = Tk(className='Gesture Keyboard')
gui.geometry("1920x1080")

myFont = font.Font(size=30)


# def task_1():
#     os.system('python gk.py')
#     #os.system('cmd /k "python gk.py"')
#
# def task_2():
#     os.system('cmd /k "python demo2.py"')


# ////////////////////////////////////////////////////////////

class handDetectorclass():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 4, (255, 0, 255), cv2.FILLED)

        return lmList

# ////////////////////////////////////////////////////////////

def mouse_gesture():
    engine = pyttsx3.init()  # text to speech
    keyboard = Controller()  # keyboard controller

    # ######################### capture video
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    cap.set(10, 100)

    # ######################### screen size
    wScr, hScr = pyautogui.size()
    detector = handDetectorclass(maxHands=1)
    pTime = 0

    # ####################### Frame Reduction
    frameR = 100
    smoothening = 7
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    # ######################## output
    engine.say("hy there, how can i help ? ")
    engine.runAndWait()

    print("[INFO] print q to quit...")

    while True:
        success, img = cap.read()
        #   ======================================== find landmark
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img)
        #   ========================================= find position
        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            x3, y3 = lmList[4][1:]  # for thumb
            #  ======================================= Cheack finger
            tipIds = [4, 8, 12, 16, 20]
            fingers = []

            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # ======== cheack Fingers are up
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # print(fingers)
            # ============================================ frame redution
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                          (255, 0, 255), 2)
            # ===================================== all function =================================================

            #   ====================================== Volumn controller

            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                cx3, cy3 = (x1 + x3) // 2, (y1 + y3) // 2
                r, t = 9, 2
                if True:
                    cv2.line(img, (x3, y3), (x1, y1), (255, 0, 255), t)
                    cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x3, y3), r, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (cx3, cy3), r, (0, 0, 255), cv2.FILLED)
                    length = math.hypot(x3 - x1, y3 - y1)

                    if length < 100:
                        cv2.circle(img, (cx3, cy3), 10, (0, 255, 0), cv2.FILLED)
                        keyboard.press(Key.media_volume_up)
                        keyboard.release(Key.media_volume_up)
                        time.sleep(0.1)
                    if length > 100:
                        cv2.circle(img, (cx3, cy3), 10, (0, 0, 0), cv2.FILLED)
                        keyboard.press(Key.media_volume_down)
                        keyboard.release(Key.media_volume_down)
                        time.sleep(0.1)
            # 5.  ====================================== Mouses  is  moving
            if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0:
                # 6. ===================================Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                # 7. ===================================Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                # 8. ===================================== Move Mouse
                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY
                # 9. ===================================== Click  Mouse
            if fingers[1] == 1 and fingers[2] == 1:
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                r, t = 9, 2
                if True:
                    cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
                    cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
                    length = math.hypot(x2 - x1, y2 - y1)
                    if length < 40:
                        cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
                        pyautogui.rightClick()
            # 10. ===================================== scroll   Mouse

            if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                pyautogui.scroll(-1.5)
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                pyautogui.scroll(2)
            # 11. ===================================== doubleclick   Mouse
            if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                pyautogui.doubleClick()

        # ===================================== all function =================================================

        # ######################### Framerate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
        # ######################### Framerate

        cv2.imshow('Ans', img)
        Nkey = cv2.waitKey(1)

        if Nkey == ord("q"):
            return

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)



# EYE-GESTURE

# import the necessary packages


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


def eye_main():
    position1 = 960
    position2 = 540

    video_capture = cv2.VideoCapture(0)
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # detect face
    font = cv2.FONT_HERSHEY_SIMPLEX

    EYE_AR_THRESH = 0.2
    EYE_AR_CONSEC_FRAMES = 1.0

    # initialize the frame counters and the total number of blinks

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # start the video stream thread
    print("[INFO] starting video stream thread...")
    print("[INFO] print q to quit...")

    ret, frame = video_capture.read()
    time.sleep(1.0)
    COUNTER = 0
    TOTAL = 0

    COUNTER1 = 0
    TOTAL1 = 0

    s = 0
    p = 0

    # mlr.linear_regression_model()
    # loop over frames from the video stream
    while True:

        ret, frame = video_capture.read()
        rows, cols, _ = frame.shape
        frame = imutils.resize(frame, width=1200)
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        ##############################################
        rects = detector(gray, 0)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=7,
            minSize=(20, 20),  # size of face  (move far the size of face decreases)
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        ##############################################

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            # average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 2)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 2)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 6)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]

                # pyautogui.moveTo(x_medium-100,y_medium-100, duration = 0)
                pyautogui.moveTo(x + 20, y - 80, duration=0)

            # check to see if the eye aspect ratio is below the blink
            # threshold, and if so, increment the blink frame counter
            start = 0
            stop = 0

            if ear < EYE_AR_THRESH:
                COUNTER += 1
                p = p + 1

                start = time.time()
                if p == 1:
                    start1 = start

            else:
                if COUNTER >= EYE_AR_CONSEC_FRAMES:
                    TOTAL += 1
                    stop = time.time()
                    total_time = round(abs(stop - start1), 2)
                    print("time delay of blink = ", total_time)

                    # if total_time >= 0.6:
                    #     pyautogui.click(x + 20, y - 80)

                    new_x, new_y = pyautogui.position()
                    positionStr = 'X: ' + str(new_x).rjust(4) + ' Y: ' + str(new_y).rjust(4)

                    print(positionStr, end='')
                    print('\b' * len(positionStr), end='', flush=True)

                    pyautogui.click(new_x, new_y)

                    p = 0
                    total_time = 0

                COUNTER = 0

            # draw the total number of blinks on the frame along with
            # the computed eye aspect ratio for the frame

            cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # show the frame
        cv2.imshow("Eye Gesture", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    video_capture.release()
    cv2.destroyAllWindows()


# if __name__ == '__main__':
#     main()

# ////////////////////////////////////////////////////////////

# HAND-GESTURE


def txt2speech(mytext):
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("voice.mp3")

    # try:
    #     playsound("voice.mp3")
    #     print("Yes, it works")
    #     sleep(2.0)
    # except:
    #      print("Final Voice Not playing ")
    # os.remove('voice.mp3')

    converter = pyttsx3.init()
    converter.setProperty('rate', 100)
    converter.setProperty('volume', 1)
    converter.say(mytext)
    converter.runAndWait()


def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                      (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    # print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


class MyButton():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


def hand_main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.8)
    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<-"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "_"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
    finalText = ""

    keyboard = Controller()

    buttonList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(MyButton([100 * j + 50, 100 * i + 50], key))

    print("[INFO] print 's' to quit...")

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bboxInfo = detector.findPosition(img)
        img = drawAll(img, buttonList)

        # PRESS 's' TO STOP
        if cv2.waitKey(5) == ord('s'):
            txt2speech(finalText)
            break

        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    # print(l)

                    ## when clicked
                    if l < 30:
                        if button.text == "<-":
                            if len(finalText):
                                keyboard.press(Key.backspace)
                                finalText = finalText.strip(finalText[-1])
                                cv2.rectangle(img, button.pos, (x + w, y + h),
                                              (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, button.text, (x + 20, y + 65),
                                            cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                        elif button.text == "_":
                            keyboard.press(Key.space)
                            finalText = finalText.ljust(len(finalText) + 1)
                            cv2.rectangle(img, button.pos, (x + w, y + h),
                                          (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 65),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
                        else:
                            keyboard.press(button.text)
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 65),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            finalText += button.text

                        # FOR Pronounce particular character
                        converter = pyttsx3.init()
                        converter.setProperty('rate', 150)
                        converter.setProperty('volume', 1)
                        if button.text == '<-':
                            converter.say('backspace')
                        elif button.text == '_':
                            converter.say('space')
                        else:
                            converter.say(button.text)
                        converter.runAndWait()

                        sleep(1.0)

        cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (60, 430),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        cv2.imshow("Hand Gesture", img)
        cv2.waitKey(1)

# 4th module - Eye Keyboard
#
def call_MWCam():
    os.system("python MWCam.py")
def call_MWBoard():
    os.system("python MWBoard.py")

def eye_board():
    t1 = threading.Thread(target=call_MWBoard)
    t2 = threading.Thread(target=call_MWCam)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print("Done")

# Create button
button1 = Button(gui, bg='#0052cc', fg='#ffffff', text="Hand Keyboard", command=hand_main)
button2 = Button(gui, bg='#0052cc', fg='#ffffff', text="Eye Mouse", command=eye_main)
button3 = Button(gui, bg='#0052cc', fg='#ffffff', text="Hand Mouse", command=mouse_gesture)
button4 = Button(gui, bg='#0052cc', fg='#ffffff', text="Eye Keyboard", command=eye_board)

# Apply font to the button label
button1['font'] = myFont
button2['font'] = myFont
button3['font'] = myFont
button4['font'] = myFont

# Add Elements to gui window
Label(text="\n Select One of the options to Start... \n", font=("Arial", 30)).pack()
button1.pack()
Label(text="\n", font=("Arial", 25)).pack()
button2.pack()
Label(text="\n", font=("Arial", 25)).pack()
button3.pack()
Label(text="\n", font=("Arial", 25)).pack()
button4.pack()

gui.mainloop()
