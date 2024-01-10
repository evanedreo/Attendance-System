import os
import pickle
import cvzone
import numpy as np
import cv2
import face_recognition
import firebase_admin
from firebase_admin import storage
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendance-d5748-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendance-d5748.appspot.com'
})

bucket = storage.bucket()


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

modeType = 3
counter = 0
id = -1
imgStudent =[]


while True:
    success, img = cap.read()

    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgResized = cv2.resize(img, (1280, 950))
    imgBackground[330:330 + 950, 105:105 + 1280] = imgResized
    imgModeResized = cv2.resize(imgModeList[modeType], (864, 1263))
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
            id = studentIds[matchIndex]

            if counter == 0:
                counter = 1
                modeType = 1

    if counter != 0:
        if counter == 1:
            #Get the Data
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)

            #Get the Image from the storage
            blob = bucket.get_blob(f'Images/{id}.jpg')
            array = np.frombuffer(blob.download_as_string(),np.uint8)
            imgStudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

        cv2.putText(imgBackground,str(studentInfo['total_attendance']),(1750,252),
                    cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2)
        cv2.putText(imgBackground, str(studentInfo['major']), (2015, 1105),
                    cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 2)
        cv2.putText(imgBackground, str(id), (2015,990),
                    cv2.FONT_HERSHEY_COMPLEX, 0.9, (255,255,255), 2)
        cv2.putText(imgBackground, str(studentInfo['standing']), (1820, 1260),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        cv2.putText(imgBackground, str(studentInfo['year']), (2050, 1260),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
        cv2.putText(imgBackground, str(studentInfo['starting_year']), (2250, 1260),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)

        (w,h),_=cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
        offset =(864-w)//2
        cv2.putText(imgBackground, str(studentInfo['name']), (1510+offset, 888),
                    cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)


        imgStudentResized = cv2.resize(imgStudent, (452, 444))
        imgBackground[352:352 + 444, 1826:1826 + 452] = imgStudentResized
        counter +=1


    cv2.imshow("Webcam", imgResized)
    cv2.imshow("Face Attendance System", imgBackground)
    cv2.waitKey(1)