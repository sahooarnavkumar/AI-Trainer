import cv2
import mediapipe as mp
import numpy as np
import time
import datetime
import math
from cvzone.PoseModule import PoseDetector as pm

cap = cv2.VideoCapture(0)
detector = pm()
x = datetime.datetime.now()
date = '%d/%m/%Y'
count = 0
dir = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AITrainer/test.jpg")
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img, draw=False)

    # print(lmList)
    p1 = lmList[11]
    p2 = lmList[13]
    p3 = lmList[15]
    # print(p1)
    x1, y1 = p1[1], p1[2]
    x2, y2 = p2[1], p2[2]
    x3, y3 = p3[1], p3[2]
    # print(x1, y1)
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0:
        angle += 360
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
    cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
    cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
    cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
    cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
    cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    per = np.interp(angle, (210, 310), (0, 100))
    bar = np.interp(angle, (220, 310), (650, 100))
    # print(angle, per)
    color = (255, 0, 255)
    # Checking for dumble curls
    if per == 100:
        color = (0, 255, 0)
        if dir == 0:
            count += 0.5
            dir = 1
    if per == 0:
        color = (0, 255, 0)
        if dir == 1:
            count += 0.5
            dir = 0
    # print(count)
    cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
    cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
    cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                color, 4)

    # Draw Curl Count
    cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15,
                (255, 0, 0), 25)
    actualCount = str(int(count))
    # Editing/Saving the File
    with open('Curls_Data.txt', 'w', encoding='utf-8') as data:
        data.write(f'\n{x.strftime(date)},{actualCount}')
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
