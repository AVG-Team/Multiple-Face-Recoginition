import cv2
from module import recognition_face
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime
from PIL import Image
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'Uploads Tmp'
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
        name = datetime.now().strftime("%Y%m%d%H%M") + "_" + file.filename
        filename = os.path.join(app.config['UPLOAD_FOLDER'], name)
        file.save(filename)

        listStudentInfo = recognition_face(filename)

        if not listStudentInfo:
            return jsonify({'error': 'No face detected'})

        time = (datetime.now().strftime("%Y%m%d%H%M"))
        print(time)
        return jsonify({'message': 'File uploaded successfully', 'data': listStudentInfo, 'folder': time})

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

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)

            try:
                img = Image.open(image_path)
                img.verify()
                image_list.append(filename)
            except Exception as e:
                print(f"Tệp {filename} bị lỗi: {str(e)}")

    return render_template('attendances.html', images=image_list, folder=folder_name)


@app.route('/image/<folder>/<filename>')
def get_image(folder, filename):
    folder_path = os.path.join('../Attendance', folder)
    return send_from_directory(folder_path, filename)


if __name__ == '__main__':
    app.run(debug=True)
