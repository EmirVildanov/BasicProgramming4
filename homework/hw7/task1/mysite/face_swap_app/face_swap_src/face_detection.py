import os

import cv2
import urllib.request as urlreq
import numpy as np


# For more detailed information about face and landmarks detection look here:
# https://medium.com/analytics-vidhya/facial-landmarks-and-face-detection-in-python-with-opencv-73979391f30e


class FaceDetector:
    def __init__(self):
        haarcascade_url = (
            "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt2.xml"
        )
        haarcascade = "haarcascade_frontalface_alt2.xml"

        if haarcascade in os.listdir(os.curdir):
            print("Face detector file exists")
        else:
            urlreq.urlretrieve(haarcascade_url, haarcascade)
            print("Face detector file downloaded")
        self.face_detector = cv2.CascadeClassifier(haarcascade)

        LBFmodel_url = "https://github.com/kurnianggoro/GSOC2017/raw/master/data/lbfmodel.yaml"
        LBFmodel = "lbfmodel.yaml"
        if LBFmodel in os.listdir(os.curdir):
            print("Landmark detector file exists")
        else:
            urlreq.urlretrieve(LBFmodel_url, LBFmodel)
            print("Landmark detector file downloaded")

        self.face_landmark_detector = cv2.face.createFacemarkLBF()
        self.face_landmark_detector.loadModel(LBFmodel)


def select_face(image, r=10):
    face_detector = FaceDetector()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_detector.face_detector.detectMultiScale(gray)
    if len(faces) == 0:
        raise RuntimeError("There is no face on photo. Please try to upload another image")
    if len(faces) > 1:
        raise RuntimeError("There are more than one face on photo. Please try to upload another image")
    _, landmarks = face_detector.face_landmark_detector.fit(gray, faces)

    points = []
    for landmark in landmarks:
        for x, y in landmark[0]:
            points.append((int(x), int(y)))

    im_w, im_h = image.shape[:2]
    left, top = np.min(points, 0)
    right, bottom = np.max(points, 0)

    x, y = int(max(0, left - r)), int(max(0, top - r))
    w, h = int(min(right + r, im_h) - x), int(min(bottom + r, im_w) - y)

    return points - np.asarray([[x, y]]), (x, y, w, h), image[y : y + h, x : x + w]
