import cv2
import threading
import os
import face_recognition
import pickle
from multiprocessing import Process, Queue
import requests


def sendServer(name):
    body = {
        'accessPoint': 'Allegro Bochalema Principal',
        'name': name
    }

    r = requests.post(url=URL, json=body)
    print(r.text)


def UpdateEncoding():
    global facesEncoding
    global facesNames
    global facesEncoding
    global facesNames

    print('UpdateEncoding')

    for fileStr in os.listdir(facesFolder):
        fileName = fileStr.split(".")[0]

        if not os.path.exists(encodingsFolder + "/" + fileName + ".face"):
            face = face_recognition.load_image_file(
                facesFolder + '/' + fileStr)
            faceEnc = face_recognition.face_encodings(face)[0]

            pickle.dump(faceEnc, open(encodingsFolder +
                                      "/" + fileName + ".face", 'wb'))

        coding = pickle.load(
            open(encodingsFolder + "/" + fileName + ".face", 'rb'))
        facesNames.append(fileName)
        facesEncoding.append(coding)

    print('UpdateEncoding Finish')


def GetCamData(Qframe, QState, QDataReturn):
    cam = cv2.VideoCapture(2)
    cam.set(cv2.CAP_PROP_FOURCC, codeCam)

    name = ""
    top = 0
    right = 0
    bottom = 0
    left = 0

    while(True):
        ret, img = cam.read()

        if(ret):

            if Qframe.qsize() == 0:
                print("Load New Frame")
                Qframe.put(img)

            if QDataReturn.qsize() == 5:
                name = QDataReturn.get()
                top = QDataReturn.get()
                right = QDataReturn.get()
                bottom = QDataReturn.get()
                left = QDataReturn.get()

            cv2.rectangle(img, (left, top),
                          (right, bottom), (0, 0, 255), 2)

            cv2.putText(img, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

            cv2.imshow('WebCam', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cam.release()
                cv2.destroyAllWindows()
                QState.put(True)
                break


def Detect(Qframe, QDataReturn):
    lastName = ""
    count = 0

    while(True):
        if Qframe.qsize() == 1:
            print("Get New Frame")

            frame = Qframe.get()

            name = "Unknown"
            top = 0
            right = 0
            bottom = 0
            left = 0

            if frame is not None:
                smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgbSmallFrame = smallFrame[:, :, ::-1]

                faceLocations = face_recognition.face_locations(rgbSmallFrame)
                faceEncodings = face_recognition.face_encodings(
                    rgbSmallFrame, faceLocations)

                faceNameDetect = []
                for fe in faceEncodings:
                    matches = face_recognition.compare_faces(facesEncoding, fe)

                    if True in matches:
                        firstMatchIndex = matches.index(True)
                        name = facesNames[firstMatchIndex]

                    faceNameDetect.append(name)

                for (top, right, bottom, left), name in zip(faceLocations, faceNameDetect):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                if QDataReturn.qsize() == 0:
                    QDataReturn.put(name)
                    QDataReturn.put(top)
                    QDataReturn.put(right)
                    QDataReturn.put(bottom)
                    QDataReturn.put(left)

                if lastName == name:
                    count = count + 1

                lastName = name

                if count == 5:
                    sendServer(name)
                    count = 0


URL = 'http://localhost:8888/SetCurrent'

codeCam = 1196444237.0

facesFolder = 'known_faces'
encodingsFolder = 'know_encoding'

facesEncoding = []
facesNames = []

start = True
newFrame = True
frame = None

font = cv2.FONT_HERSHEY_COMPLEX

Qframe = Queue()
QState = Queue()
QDataReturn = Queue()

UpdateEncoding()

print('Creando Hilo Camara')
CamThr = Process(name='Camera', target=GetCamData,
                 args=(Qframe, QState, QDataReturn))

print('Creando Hilo Detector')
DecThr = Process(name='Detector', target=Detect,
                 args=(Qframe, QDataReturn))

print('Lanzando Hilo Camara')
CamThr.start()

print('Lanzando Hilo Detector')
DecThr.start()

while(True):
    if QState.qsize() == 1:
        CamThr.terminate()
        DecThr.terminate()
        break
