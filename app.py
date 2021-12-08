import os

import face_recognition
from flask import Flask, request, flash, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)


def get_image_owner_name(image):
    unknown_image = face_recognition.load_image_file(image)

    try:
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    except IndexError:
        print("Немає жодного лиця на фотографії")
        os.remove(image)
        return None

    list_of_files = [f for f in glob.glob("faces/" + "*.jpg")]

    for file in list_of_files:
        saved_image = face_recognition.load_image_file(file)
        results = face_recognition.compare_faces([face_recognition.face_encodings(saved_image)[0]],
                                                 unknown_face_encoding,
                                                 )
        if results[0]:
            return file.split("/")[1].split(".")[0]

    return "Невідомий"


@app.route('/get-recognition', methods=["GET", "POST"])
def get_recognition():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('Немає файлу')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Не вибрано файлу')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file_path = os.path.join(f"tmp/{filename}")
        file.save(file_path)
        name = get_image_owner_name(file_path)
        os.remove(file_path)
        return name, 200


@app.route('/save-image', methods=["GET", "POST"])
def save_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('Немає файлу')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Не вибрано файлу')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file_path = os.path.join(f"tmp/{filename}")
        file.save(file_path)
        try:
            unknown_image = face_recognition.load_image_file(file_path)
            face_recognition.face_encodings(unknown_image)[0]
            os.replace(file_path, f"faces/{filename}")
        except IndexError:
            os.remove(file_path)
            return "Немає жодного лиця на фотографії", 400
        return "Зображення додано", 201


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
