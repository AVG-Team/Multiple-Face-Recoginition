import cv2
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recoginiton-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recoginiton.appspot.com"
})

folderPath = "Images"
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    print(path)
    print(os.path.splitext(path)[0])

    filename = os.path.join(f'{folderPath}/{path}')
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
print(studentIds)