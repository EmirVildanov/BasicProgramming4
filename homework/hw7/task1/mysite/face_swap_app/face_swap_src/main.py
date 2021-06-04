import os

import cv2

from .face_detection import select_face
from .face_swap import face_swap


def swap_faces(first_image, second_image, path_to_save=None):
    src_points, src_shape, src_face = select_face(first_image)
    dst_points, dst_shape, dst_face = select_face(second_image)

    first_on_second = face_swap(src_face, dst_face, src_points, dst_points, dst_shape, second_image)
    second_on_first = face_swap(dst_face, src_face, dst_points, src_points, src_shape, first_image)
    if path_to_save is not None:
        path = os.path.join(path_to_save, "FirstOnSecond.jpg")
        print(f"Path is {path}")
        cv2.imwrite(os.path.join(path_to_save, "FirstOnSecond.jpg"), first_on_second)
        cv2.imwrite(os.path.join(path_to_save, "SecondOnFirst.jpg"), second_on_first)
    return first_on_second, second_on_first


def swap_and_save_loaded_image():
    src_img = cv2.imread(os.path.join("media", "images", "uploaded_image.jpg"))
    dst_img = cv2.imread(os.path.join("media", "images", "Putin.png"))

    if src_img is None:
        raise RuntimeError("Uploaded image is empty")
    if dst_img is None:
        raise RuntimeError("Dst image is empty")
    swap_faces(src_img, dst_img, os.path.join("media", "images"))
