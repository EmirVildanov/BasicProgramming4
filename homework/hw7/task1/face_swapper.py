import cv2

face_detector_file_name = "models/haar_cascade_classifier.xml"
LBF_model_file_name = "models/lbfmodel.yaml"


class FaceSwapper:
    def __init__(self):
        self.face_detector = cv2.CascadeClassifier(face_detector_file_name)
        self.face_landmark_detector = cv2.face.createFacemarkLBF()
        self.face_landmark_detector.loadModel(LBF_model_file_name)
