import numpy as np
import cv2

if __name__ == "__main__":
    horse = cv2.imread("Horse.png", cv2.IMREAD_COLOR)
    circle = cv2.imread("Circle.png", cv2.IMREAD_COLOR)

    image = cv2.imread("Test.jpg")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clean_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
    laplacian = cv2.Laplacian(clean_image, cv2.CV_64F)
    cv2.imshow("Me", laplacian)
    k = cv2.waitKey(0)
    if k == 27:  # wait for ESC key to exit
        cv2.destroyAllWindows()
    elif k == ord("s"):  # wait for 's' key to save and exit
        cv2.imwrite("Saved_Horse.png", horse)
        cv2.destroyAllWindows()
