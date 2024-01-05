import json
from unidecode import unidecode

# Đọc file JSON
with open('data_train.json', 'r') as json_file:
    data = json.load(json_file)

# Đọc file văn bản
with open('train_ai.txt', 'r', encoding='utf-8') as txt_file:
    lines = txt_file.readlines()

# Duyệt qua từng dòng trong file văn bản
for line in lines:
    parts = line.split()
    if len(parts) >= 2:
        student_id = parts[0]
        student_name = ' '.join(parts[1:])
        data["data"][student_id] = {
            "id": student_id,
            "name": unidecode(student_name),
            "major": "IT",
            "starting_year": 2021,
            "total_attendance": 0,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        }

print(data)

json_data = json.dumps(data, ensure_ascii=False)

# Ghi lại file JSON
with open('data_train_update.json', 'w') as json_file:
    json.dump(data, json_file, indent=2)
