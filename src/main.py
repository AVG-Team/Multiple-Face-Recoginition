import csv

import cv2
from firebase_admin import db

import firebase_admin
from firebase_admin import credentials

from module import recognition_face
from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import os
from datetime import datetime
from PIL import Image
import re

app = Flask(__name__)

UPLOAD_FOLDER = '../Uploads Tmp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        try:
            name = datetime.now().strftime("%Y%m%d%H%M") + "_" + file.filename
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], name)
            file.save(filename)

            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            listStudentInfo = recognition_face(filename, timestamp)

            if not listStudentInfo:
                return jsonify({'error': 'No face detected'})

            return jsonify({'message': 'File uploaded successfully', 'data': listStudentInfo, 'folder': timestamp})
        except Exception as e:
            return jsonify({print(f"An unexpected error occurred: {e}")})

    return jsonify({'error': 'Invalid file type'})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400


@app.route('/attendances')
def attendances():
    folder_name = request.args.get('q', '')

    if not re.match("^[a-zA-Z0-9_-]+$", folder_name):
        return render_template('400.html'), 400

    folder_path = os.path.join('../Attendance', folder_name)

    if not os.path.exists(folder_path):
        return render_template('404.html'), 404

    image_list = []
    info_list = {}

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)

            try:
                img = Image.open(image_path)
                img.verify()
                image_list.append(filename)
            except Exception as e:
                print(f"Tệp {filename} bị lỗi: {str(e)}")
    csv_file_path =folder_path + "/students.csv"
    # Mở file CSV
    with open(csv_file_path, 'r', newline='') as file:
        # Đọc dữ liệu từ file CSV
        csv_reader = csv.DictReader(file)
        # Lặp qua từng dòng và hiển thị thông tin
        for row in csv_reader:
            info_list[row['id']] = row['name']

        print(info_list,info_list['2180607368'])
    return render_template('attendances.html', images=image_list, folder=folder_name, info=info_list)

def file_exists(file_path):
    return os.path.exists(file_path) and os.path.isfile(file_path)


@app.route("/attendance/export", methods=['POST'])
def export_attendance():
    if request.method != 'POST':
        print(1)
        return render_template('400.html'), 400

    folder_name = request.form.get('q', '')
    print(folder_name)
    if not re.match("^[a-zA-Z0-9_-]+$", folder_name):
        print(2)
        return render_template('400.html'), 400

    folder_path = os.path.join('../Attendance', folder_name)

    if not os.path.exists(folder_path):
        print(3)
        return render_template('404.html'), 404

    image_path = os.path.join(folder_path, "students.csv")

    if file_exists(image_path):
        print(4)
        return send_file(image_path, as_attachment=True, download_name= datetime.now().strftime("%Y%m%d%H%M%S") + '.csv')
    return "File not found."


@app.route('/image/<folder>/<filename>')
def get_image(folder, filename):
    folder_path = os.path.join('../Attendance', folder)
    return send_from_directory(folder_path, filename)


@app.route('/img/<filename>')
def get_img(filename):
    folder_path = os.path.join('../img')
    return send_from_directory(folder_path, filename)


if __name__ == '__main__':
    app.run(debug=True)
