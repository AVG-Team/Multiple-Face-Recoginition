import cv2
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("../../serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recoginiton-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recoginiton.appspot.com"
})

folderPath = "../../Images/three_year"

folderUpload = "three_year_upload"
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    folderPathName = os.path.join(f'{folderPath}/{path}')
    files = os.listdir(folderPathName)
    for file in files:
        filename = os.path.join(folderPathName, file)
        filenameUpload = os.path.join(f'{folderUpload}/{path}/{file}')
        print(filenameUpload)
        bucket = storage.bucket()
        blob = bucket.blob(filenameUpload)
        blob.upload_from_filename(filename)

print("success")

