import glob
import os

import face_recognition


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
