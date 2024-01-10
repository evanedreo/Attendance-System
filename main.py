import os

import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 950)   # Height

imgBackground = cv2.imread('Resources/background.png')

# importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

print(len(imgModeList))


while True:
    success, img = cap.read()

    imgResized = cv2.resize(img, (1280, 950))
    imgBackground[330:330 + 950, 105:105 + 1280] = imgResized
    imgModeResized = cv2.resize(imgModeList[0], (864, 1263))
    imgBackground[91:91 + 1263, 1615:1615 + 864] = imgModeResized

    cv2.imshow("Webcam", imgResized)
    cv2.imshow("Face Attendance System", imgBackground)
    cv2.waitKey(1)