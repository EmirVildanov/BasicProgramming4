from typing import List, Tuple
import numpy as np
import cv2

from homework.hw7.task1.face_swap_first_step.constants import RED, GREEN
from homework.hw7.task1.face_swap_first_step.face_detector import FaceDetector


def rect_contains_point(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True


def draw_face_point(img, p, color):
    x = int(p[0])
    y = int(p[1])
    cv2.circle(img, (x, y), 2, color, cv2.FILLED, cv2.LINE_AA, 0)


def get_triangle_points(t):
    t = [int(i) for i in t]
    return np.array([[t[0], t[1]], [t[2], t[3]], [t[4], t[5]]])


def draw_delaunay_triangles(img, triangleList, delaunay_color):
    size = img.shape
    r = (0, 0, size[1], size[0])

    for t in triangleList:
        pt1, pt2, pt3 = get_triangle_points(t)

        if rect_contains_point(r, pt1) and rect_contains_point(r, pt2) and rect_contains_point(r, pt3):
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)


def get_triangle_list_from_image_and_points(image, points):
    sub_div = cv2.Subdiv2D((0, 0, image.shape[1], image.shape[0]))
    for point in points:
        sub_div.insert(point)

    return sub_div.getTriangleList()


def get_bound_coordinates(points: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    min_x = int(min([p[0] for p in points]))
    max_x = int(max([p[0] for p in points]))
    min_y = int(min([p[1] for p in points]))
    max_y = int(max([p[1] for p in points]))
    return min_x, max_x, min_y, max_y


if __name__ == "__main__":
    face_detector = FaceDetector()

    first_face = cv2.imread("photos/boy.jpg")
    first_face_template = first_face.copy()
    first_face_gray = cv2.cvtColor(first_face_template, cv2.COLOR_BGR2GRAY)
    first_face_info = [first_face_template, first_face_gray]

    second_face = cv2.imread("photos/girl.jpg")
    second_face_template = second_face.copy()
    second_face_gray = cv2.cvtColor(second_face, cv2.COLOR_BGR2GRAY)
    second_face_info = [second_face_template, second_face_gray]

    faces_images = [first_face_info, second_face_info]
    faces_triples = []
    for index, face in enumerate(faces_images):
        template = face[0]
        gray = face[1]

        faces = face_detector.face_detector.detectMultiScale(gray)
        _, landmarks = face_detector.face_landmark_detector.fit(gray, faces)

        points = []
        for landmark in landmarks:
            for x, y in landmark[0]:
                points.append((x, y))

        # x_min, x_max, y_min, y_max = get_bound_coordinates(points)
        # cropped = template[y_min - 1:y_max + 1, x_min - 1:x_max + 1]
        # resized = cv2.resize(cropped, (500, 500))
        # face[0] = resized.copy()
        # template = face[0]

        # after we resized image, we have to repeat operation

        # gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        # print(gray.shape)
        # faces = face_swapper.face_detector.detectMultiScale(gray)
        # print(faces)
        # _, landmarks = face_swapper.face_landmark_detector.fit(gray, faces)
        #
        # points = []
        # for landmark in landmarks:
        #     for x, y in landmark[0]:
        #         points.append((x, y))

        triangle_list = get_triangle_list_from_image_and_points(template, points)

        # draw_delaunay_triangles(template, triangle_list, WHITE)
        # for p in points:
        #     draw_face_point(template, p, RED)

        faces_triples.append([template, points, triangle_list])

    alfa = 0.5
    morphed_points = []
    for i in range(len(faces_triples[0][1])):
        x_i = faces_triples[0][1][i][0]
        x_j = faces_triples[1][1][i][0]
        y_i = faces_triples[0][1][i][1]
        y_j = faces_triples[1][1][i][1]
        x_m = (1 - alfa) * x_i + alfa * x_j
        y_m = (1 - alfa) * y_i + alfa * y_j
        morphed_points.append((x_m, y_m))

    morphed_image = np.zeros((first_face_template.shape[1], first_face_template.shape[0], 3), np.uint8)
    morphed_triangle_list = get_triangle_list_from_image_and_points(morphed_image, morphed_points)
    draw_delaunay_triangles(second_face_template, morphed_triangle_list, GREEN)
    for p in morphed_points:
        draw_face_point(morphed_image, p, RED)
        draw_face_point(second_face_template, p, GREEN)
    faces_triples.append([morphed_image, morphed_points, morphed_triangle_list])

    first_image_to_morphed_affine_transforms: List[None] = []
    second_image_to_morphed_affine_transforms: List[None] = []

    min_triangles_number = min(len(faces_triples[0][2]), len(faces_triples[1][2]), len(morphed_triangle_list))  # COSTYL

    for i in range(min_triangles_number):
        first_image_triangles_points = get_triangle_points(faces_triples[0][2][i]).astype(np.float32)
        second_image_triangles_points = get_triangle_points(faces_triples[1][2][i]).astype(np.float32)
        morphed_image_triangles_points = get_triangle_points(morphed_triangle_list[i]).astype(np.float32)

        # print("Start")
        # print(first_image_triangles_points)
        # print(morphed_image_triangles_points)
        # print("End")

        first_image_to_morphed_affine_transforms.append(
            cv2.getAffineTransform(first_image_triangles_points, morphed_image_triangles_points)
        )
        first_image_to_morphed_affine_transforms.append(
            cv2.getAffineTransform(second_image_triangles_points, morphed_image_triangles_points)
        )

    for i in range(min_triangles_number):
        x_min, x_max, y_min, y_max = get_bound_coordinates(get_triangle_points(faces_triples[0][2][i]))
        cropped = faces_triples[0][0][y_min:y_max, x_min:x_max]

        # print("Start")
        # print(cropped)
        # print(type(cropped))
        # print(get_bound_coordinates(get_triangle_points(faces_triples[0][2][i])))
        # print("Finish")

        if cropped.size == 0:
            print("CONTINUE")
            continue
        else:
            print("NOT CONTINUE")
            # print(get_bound_coordinates(get_triangle_points(faces_triples[0][2][i])))
            # print(first_face[y_min:y_max, x_min:x_max])
            # print(cropped)
        # result = cv2.warpAffine(cropped, first_image_to_morphed_affine_transforms[i],
        #                         (cropped.shape[1], cropped.shape[0]))
        test = np.array([[-0.98666667, 2.26666667, 0], [-1.70666667, 1.86666667, 0]])
        result = cv2.warpAffine(cropped, test, (cropped.shape[1], cropped.shape[0]))
        print("Affine:")
        print(first_image_to_morphed_affine_transforms[i])
        print("Result:")
        print(result)
        cv2.imshow("Result", result)

        cv2.fillConvexPoly(result, get_triangle_points(faces_triples[0][2][i]), 1)
        faces_triples[0][0][y_min:y_max, x_min:x_max] = result
        # if i == 0:
        #     break

    for index, face_triple in enumerate(faces_triples):
        # template = face_triple[0]
        # points = face_triple[1]
        # x_min, x_max, y_min, y_max = get_bound_coordinates(points)
        # cropped = template[y_min:y_max, x_min:x_max]
        # resized = cv2.resize(cropped, (500, 500))
        # face_triple[0] = resized
        cv2.imshow(f"{index}", face_triple[0])
        if index == 0:
            break

    # morphed_image = cv2.addWeighted(faces_triples[0][0], alfa, faces_triples[1][0], 1 - alfa, 0)
    # cv2.imshow(f"Result", morphed_image)

    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()
    elif k == ord("s"):
        cv2.imwrite("Saved.png", faces_triples[1][0])
        cv2.destroyAllWindows()
