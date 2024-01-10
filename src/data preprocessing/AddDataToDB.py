import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

cred = credentials.Certificate("../../ServiceFirebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
})
# DB : Students / IdStudents :
ref = db.reference('Students')

with open('data_train.json', 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)
    data = json_data.get('data', {})

for key, value in data.items():
    ref.child(key).set(value)
