import os
import pickle

import cvzone
import numpy as np
import cv2
import face_recognition

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

#load the encoding file
print("Loading Encode File")
file = open("EncodeFile.p",'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")



while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgResized = cv2.resize(img, (1280, 950))
    imgBackground[330:330 + 950, 105:105 + 1280] = imgResized
    imgModeResized = cv2.resize(imgModeList[3], (864, 1263))
    imgBackground[91:91 + 1263, 1615:1615 + 864] = imgModeResized

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print("matches", matches)
        # print("faceDis",faceDis)

        matchIndex = np.argmin(faceDis)
        # print("Match Index", matchIndex)

        if matches[matchIndex]:
            # print("Known Face Detected")
            # print(studentIds[matchIndex])
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            bbox =  -190+x1, y1, x2-x1, y2-y1
            imgBackground= cvzone.cornerRect(imgBackground,bbox,rt=0)


    cv2.imshow("Webcam", imgResized)
    cv2.imshow("Face Attendance System", imgBackground)
    cv2.waitKey(1)