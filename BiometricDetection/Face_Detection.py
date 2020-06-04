import face_recognition
import cv2
import numpy as np
import matplotlib.pyplot as plt

video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
video_capture.set(cv2.CAP_PROP_FPS, 5)

print(video_capture.get(cv2.CAP_PROP_FPS))

face1 = face_recognition.load_image_file("known_faces/Breyner_Albarracin.jpg")
face1_encoding = face_recognition.face_encodings(face1)[0]

face2 = face_recognition.load_image_file("known_faces/Victor_Romero.jpeg")
face2_encoding = face_recognition.face_encodings(face2)[0]

faceA1 = face_recognition.load_image_file("known_faces/Persona1.jpg")
faceA1_encoding = face_recognition.face_encodings(faceA1)[0]
faceA2 = face_recognition.load_image_file("known_faces/Persona2.jpg")
faceA2_encoding = face_recognition.face_encodings(faceA2)[0]
faceA3 = face_recognition.load_image_file("known_faces/Persona3.jpg")
faceA3_encoding = face_recognition.face_encodings(faceA3)[0]
faceA4 = face_recognition.load_image_file("known_faces/Persona4.jpg")
faceA4_encoding = face_recognition.face_encodings(faceA4)[0]
faceA5 = face_recognition.load_image_file("known_faces/Persona5.jpg")
faceA5_encoding = face_recognition.face_encodings(faceA5)[0]
faceA6 = face_recognition.load_image_file("known_faces/Persona6.jpg")
faceA6_encoding = face_recognition.face_encodings(faceA6)[0]

known_face_encodings = [
    face1_encoding,
    face2_encoding,
    faceA1_encoding,
    faceA2_encoding,
    faceA3_encoding,
    faceA4_encoding,
    faceA5_encoding,
    faceA6_encoding
]

known_face_names = [
    "Breyner_Albarracin",
    "Victor_Romero",
    "Persona1",
    "Persona2",
    "Persona3",
    "Persona4",
    "Persona5",
    "Persona6"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

font = cv2.FONT_HERSHEY_COMPLEX

while True:
    ret, frame = video_capture.read()

    if (frame is None):
        print("start cam...")
    else:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                face_distances = face_recognition.face_distance(
                    known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)
            print(name)

        cv2.imshow('Cam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_capture.release()
cv2.destroyAllWindows()
