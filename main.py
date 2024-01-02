import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import firebase_admin
from firebase_admin import credentials

# region Init Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recoginiton-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recoginiton.appspot.com"
})

bucket = storage.bucket()

listStudentInfo = []

# endregion
def recognition_face(input):
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
    print("Encode File Loaded")

    # Init
    modeType = 0
    counter = 0
    imageName = -1
    imgStudent = []

    # input
    img = cv2.imread('Test/multiple.png')

    imgS = cv2.resize(img, (0, 0), None, 1, 1)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgShow = cv2.resize(img, (635, 480))
    imgBackground[160:160 + 480, 55:55 + 635] = imgShow
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                print("Known Face Detected")
                imageName = studentIds[matchIndex]
                studentInfo = db.reference(f'Students/{imageName}').get()
                print(studentInfo)
                print(studentInfo)
                y1, x2, y2, x1 = faceLoc
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    counter = 1
                    modeType = 1
            if counter != 0:
                if counter == 1:
                    # Get the Data
                    studentInfo = db.reference(f'Students/{imageName}').get()
                    # Get the Image from the storage
                    blob = bucket.get_blob(f'Images/{imageName}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    # Update data of attendance
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{imageName}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        counter = 0
                if modeType != 3:
                    if 10 < counter < 20:
                        modeType = 2
                    counter += 1
                    if counter <= 10:
                        # Create a photo when taking attendance
                        outputFolder = './Attendance/' + datetime.now().strftime("%Y%m%d%H") + '/'
                        os.makedirs(outputFolder, exist_ok=True)
                        cv2.imwrite(outputFolder + str(studentInfo['id']) + '.png', imgStudent)

                        listStudentInfo.append(studentInfo)
                        # reset step
                        counter = 0
                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
    else:
        print("1123")
        modeType = 0
        counter = 0
    return listStudentInfo
