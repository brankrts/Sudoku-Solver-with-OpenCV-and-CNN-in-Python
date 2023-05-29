import cv2
import numpy as np

from keras.models import load_model

class ImageProcessor:

    def __init__(self, image) -> None:
        self.image = image
        self.contour_area_threshold  = 50

    def image_preprocess(self):

        image_gray = cv2.cvtColor(self.image ,cv2.COLOR_BGR2GRAY ) 
        image_blur = cv2.GaussianBlur(image_gray , (5,5) , 1)
        image_threshold = cv2.adaptiveThreshold(image_blur,255,1,1,11,2)

        return image_threshold
    
    # verilen resim icerisinde en buyuk alana sahip olan dikdortgensel bolgenin hesabi gerceklestirilmektedir.
    def image_biggest_contour(self,contour):

        biggest_area_coords = np.array([])
        max_area = 0
        
        for i in contour:

            area = cv2.contourArea(i)

            if area > self.contour_area_threshold:
                peri = cv2.arcLength(i , True)
                approx = cv2.approxPolyDP(i , 0.02 * peri , True)
                if area > max_area and len(approx) == 4:
                    biggest_area_coords = approx
                    max_area = area
            
        return biggest_area_coords , max_area 
    

    # belirtilen alani ifade eden 4 farkli noktanin cv2 organizasyonu icin yeniden siralandirilmasi islemi gerceklestirilmektedir.

    def reorder_max_contour_area_points(self, max_contour_area):

        max_contour_area = max_contour_area.reshape((4,2))
        new_max_contour_area = np.zeros((4,1,2),dtype = np.int32)
        add = max_contour_area.sum(1)
        new_max_contour_area[0] = max_contour_area[np.argmin(add)]
        new_max_contour_area[3] = max_contour_area[np.argmax(add)]
        
        differance = np.diff(max_contour_area, axis =1)
        new_max_contour_area[1] = max_contour_area[np.argmin(differance)]
        new_max_contour_area[2] = max_contour_area[np.argmax(differance)]


        return new_max_contour_area
    
    def image_warp_perspective(self,image, points1, points2 , width , height):

        matrix = cv2.getPerspectiveTransform(points1 , points2)
        perspectived_image = cv2.warpPerspective(image,matrix, (width , height))

        return  perspectived_image

    def split_image(self, image):

        rows = np.vsplit(image,9)

        boxes = []

        for r in rows:
            cols = np.hsplit(r,9)
            for box in cols:
                boxes.append(box)

        return boxes

















