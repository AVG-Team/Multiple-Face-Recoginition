import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recoginiton-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recoginiton.appspot.com"
})

bucket = storage.bucket()

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds,encodeListKnown)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

img = cv2.imread('multiple.png')
imgS = cv2.resize(img, (0, 0), None, 1, 1)
imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
print(imgS)
faceCurFrame = face_recognition.face_locations(imgS)
encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

print("faceCurFrame")
print(faceCurFrame)

print("encode")
print(encodeCurFrame)
# imgBackground[162:162 + 480, 55:55 + 640] = img
# imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]


for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
    print("matches", matches)
    print("faceDis", faceDis)

    matchIndex = np.argmin(faceDis)
    print("Match Index", matchIndex)

    if matches[matchIndex]:
        print("Known Face Detected")
        print(studentIds[matchIndex])
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
        # imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
        id = studentIds[matchIndex]
        print(id)
modeType = 0
counter = 0
# cv2.imshow("Webcam", img)
# cv2.imshow("Face Attendance", imgBackground)
cv2.waitKey(1)
