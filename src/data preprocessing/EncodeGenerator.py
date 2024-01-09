import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("../../service.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    'storageBucket': ""
})


# Input : 123_1223.png => output = 123_1223
def extract_first_number(identifier):
    numbers = [int(num) for num in identifier.split('_') if num.isdigit()]
    if numbers:
        return numbers[0]
    else:
        return ''.join(char for char in identifier if char.isdigit())


# studentIds get name from folderPath
folderPath = '../../Images/processed'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    folderPathName = os.path.join(folderPath, path)
    files = os.listdir(folderPathName)
    for file in files:
        imgList.append(cv2.imread(os.path.join(folderPathName, file)))
        fileName = os.path.splitext(file)[0]
        studentIds.append(fileName)
        print(fileName)


# Encode image and encodeList get image encode from folderPath
def findEncodings(imagesList):
    flag = 0
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        flag += 1
# num_jitters = 100 : randomly distort your image 100 times (randomly zoomed, rotated, translated, flipped)
        face_encodings = face_recognition.face_encodings(img, num_jitters=100)
        print(flag)
        if face_encodings:
            encodeList.append(face_encodings[0])
    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
# Encode List Known With Ids
encodeListKnownWithIds = [encodeListKnown, studentIds]

print("Encoding Complete", len(studentIds), len(encodeListKnown))
print(studentIds)
print(encodeListKnown)
print(encodeListKnownWithIds)

file = open("FinalEncode.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")
