import os
import re
import pickle
import numpy as np
import cv2
import math
import face_recognition
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
import csv

# region Init Firebase
cred = credentials.Certificate("../ServiceFirebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    'storageBucket': ""
})

bucket = storage.bucket()

listStudentInfo = []


# resize image to increase speed
def resize_image(image, target_width):
    height, width = image.shape[:2]
    scale_factor = target_width / width
    return cv2.resize(image, (int(width * scale_factor), int(height * scale_factor)))


# input : 12345_3 , 12345 || output : 12345, 12345
def getStudentId(imageName):
    match = re.search(r'(\d+)', imageName)

    if match:
        number = match.group(1)
        return number
    else:
        return


# face distance to conf ( accuracy )
def face_distance_to_conf(face_distance):
    Percentage = 1.0 - face_distance
    return Percentage


def recognition_face(input, folder):
    studentIdTmp = 0
    outputFolder = '../Attendance/' + folder + '/'

    # print(len(imgModeList))

    # Load the encoding file
    print("Loading Encode File ...")
    file = open('data preprocessing/FinalEncode.p', 'rb')
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
    img = cv2.imread(input)

    imgS = cv2.resize(img, (0, 0), None, 1, 1)
    imgS = resize_image(imgS, 500)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    print("start")
    # number_of_times_to_upsample = 2 => that the original image will be scaled up twice when looking for faces.
    # Which face detection model to use. "hog" is less accurate but faster on CPUs. "cnn" is a more accurate
    #                   deep-learning model which is GPU/CUDA accelerated (if available). The default is "hog".
    faceCurFrame = face_recognition.face_locations(imgS, number_of_times_to_upsample=2, model="cnn")

    print("start encode")

    # num_jitters = 100 : randomly distort your image 100 times (randomly zoomed, rotated, translated, flipped)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame, num_jitters=100)

    print("check")

    if faceCurFrame:
        i = 0
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            print(i + 1)
            # matches : return array include true and false
            # faceDis : return array include 0 to 1
            # matchIndex : return min(facedis)
            # The smaller the distance, the more accurate the similarity
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.4)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            print("test")
            if matches[matchIndex]:
                print("Known Face Detected")
                conf = face_distance_to_conf(np.min(faceDis))
                imageName = studentIds[matchIndex]
                studentIdTmp = getStudentId(imageName)
                studentInfo = db.reference(f'Students/{studentIdTmp}').get()
                # ex : 0.3 to 30% ,...
                print("Accuracy as a Percentage là {:.0%}".format(conf))
                y1, x2, y2, x1 = faceLoc
                if counter == 0:
                    counter = 1
                    modeType = 1
            if counter != 0:
                if counter == 1:
                    # Get the Data
                    studentInfo = db.reference(f'Students/{studentIdTmp}').get()
                    print(studentInfo)
                    # Get the Image from the storage
                    print(studentIdTmp, imageName, f'Images/{studentIdTmp}/{imageName}')
                    blob = bucket.get_blob(f'Images/{studentIdTmp}/{imageName}' + ".png")
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    # Update data of attendance
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        ref = db.reference(f'Students/{studentIdTmp}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                        if 'attendances_time' in studentInfo:
                            attendances_time = studentInfo['attendances_time']
                        else:
                            attendances_time = []

                        if len(attendances_time) == 7:
                            attendances_time[6] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            attendances_time.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        ref.update({'attendances_time': attendances_time})
                    else:
                        counter = 0
                if modeType != 3:
                    if 10 < counter < 20:
                        modeType = 2
                    counter += 1
                    if counter <= 10:
                        # Create a photo when taking attendance
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

    if len(listStudentInfo) >= 1:
        csv_file_path = "students.csv"
        filenameCsv = os.path.join(outputFolder, csv_file_path)
        with open(filenameCsv, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ["id", "last_attendance_time", "major", "name", "standing", "starting_year",
                          "total_attendance", "attendances_time", "year"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Viết header
            writer.writeheader()

            # Viết dữ liệu
            for student in listStudentInfo:
                writer.writerow(student)
    return listStudentInfo


