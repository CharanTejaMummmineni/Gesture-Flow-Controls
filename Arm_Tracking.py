import cv2
import mediapipe as mp
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.SerialModule import SerialObject
import math
import time
import string

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
detection = HandDetector(detectionCon=0.5, maxHands=1)
arm = cv2.VideoCapture(0)
arduino = SerialObject()
str1 =""
count =0

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

while True:
    success, img = arm.read()
    req, img = detection.findHands(img)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)


    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        right_shoulder = [landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_elbow = [landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mpPose.PoseLandmark.RIGHT_ELBOW.value].y]
        right_wrist = [landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mpPose.PoseLandmark.RIGHT_WRIST.value].y]
        #right_hip = [landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mpPose.PoseLandmark.RIGHT_HIP.value].y]
        left_shoulder = [landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value].y]
        #right_thumb = [landmarks[mpPose.PoseLandmark.RIGHT_THUMB.value].x,landmarks[mpPose.PoseLandmark.RIGHT_THUMB.value].y]
        k1 = 0
        k2 = 0
        k3 = 0
        k4 = 0
        k5 = 0
        #K6 = 0
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            if id in (24, 16, 14, 12, 11):
                cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)
            if id == 14:
                k1 = (cx, cy)
            if id == 16:
                k2 = (cx, cy)
            if id == 12:
                k3 = (cx, cy)
            #if id == 24:
                #k4 = (cx, cy)
            if id == 11:
                k5 = (cx, cy)
            #if id == 22:
                #k6 = (cx, cy)
        cv2.line(img, k1, k2, (255, 0, 0), 2)
        cv2.line(img, k1, k3, (255, 0, 0), 2)
        #cv2.line(img, k3, k4, (255, 0, 0), 2)
        cv2.line(img, k3, k5, (255, 0, 0), 2)
        #cv2.line(img, k2, k6, (255, 0, 0), 2)
        angle1 = int(calculate_angle(right_shoulder, right_elbow, right_wrist))
        angle3 = int(calculate_angle(right_elbow,right_shoulder, left_shoulder))
        #angle4 = int(calculate_angle(right_elbow, right_wrist, right_thumb))
        #angle2 = int(calculate_angle(right_shoulder, right_elbow, right_hip))

    if req:
        tracking = req[0]
        lmlist = tracking["lmList"]
        bbox = tracking["bbox"]
        centerPoint = tracking['center']
        handType = tracking["type"]
        if lmlist:
            fingers = detection.fingersUp(tracking)
            fingers.extend([angle1, angle3])
            fingers[0] = "%04d" % fingers[0]
            fingers[1] = "%04d" % fingers[1]
            fingers[2] = "%04d" % fingers[2]
            fingers[3] = "%04d" % fingers[3]
            fingers[4] = "%04d" % fingers[4]
            fingers[5] = "%04d" % fingers[5]
            fingers[6] = "%04d" % fingers[6]
            #print(type(fingers[0]))
            print(fingers)
            arduino.sendData(fingers)

    #smallerframe = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
        break