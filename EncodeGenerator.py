import pickle
import cv2
import face_recognition
import os
import firebase_admin
from firebase_admin import storage
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendance-d5748-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendance-d5748.appspot.com'
})

# importing the people images
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = os.path.join(folderPath,path)
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(studentIds)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)[0]
        encodeList.append(encodes)

    return encodeList

print("Encoding Started")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Completed")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")