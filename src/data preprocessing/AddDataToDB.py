import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("../../serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recoginiton-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "321654":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "2180607":
        {
            "name": "Nguyen Mai Bao Huy",
            "id": "2180607",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "G",
            "year": 5,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "2180608":
        {
            "name": "Nguyen Hung",
            "id": "2180608",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "G",
            "year": 5,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "2144422":
        {
            "id": "2144422",
            "name": "Nguyen Hoang",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "G",
            "year": 5,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "3216543":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "123":
        {
            "name": "Hoang Chau",
            "id":"2180605",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "343":
        {
            "name": "GIA BAO",
            "id": "2180604",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "3432":
        {
            "name": "Bao Uyen",
            "id": "2180603",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "G",
            "year": 5,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "3532":
        {
            "name": "Nguyen Khai",
            "id": "2180602",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "G",
            "year": 5,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "5353":
        {
            "name": "ThanhQuang",
            "id": "2180601",
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 8,
            "standing": "G",
            "year": 5,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
}

for key, value in data.items():
    ref.child(key).set(value)