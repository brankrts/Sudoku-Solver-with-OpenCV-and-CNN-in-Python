from sudoku_algo  import SudokuSolver
from image_processor import ImageProcessor 
from predictor import Predictor
import numpy as np
import cv2



class SudokuVisualizer:


    def __init__(self,image_path) -> None:
         
        self.image = cv2.imread(image_path) 
        self.predictor = Predictor('Resources/model.h5')
        self.solver = SudokuSolver()
        self.image_height = 450
        self.image_width = 450
        self.image = cv2.resize(self.image , (self.image_width , self.image_height))
        self.image_processor = ImageProcessor(self.image)
        self.image_blank = np.zeros((self.image_height , self.image_width,3),np.uint8 )
        self.image_contour = self.image.copy()
        self.image_big_contour = self.image.copy()
        self.image_threshold = self.image_processor.image_preprocess() 

    def find_contour(self):

        contours , hierarchy = cv2.findContours(self.image_threshold , cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)

        self.image_contour = cv2.drawContours(self.image_contour , contours , -1 , (0 ,255,0) , 3)

        return contours

    def find_biggest_contour_area(self):

        biggest_area_coords , max_area =  self.image_processor.image_biggest_contour(self.find_contour())
        return biggest_area_coords

    def flatting_predicted_number_position(self,image,position_array ,sudoku_board):

        flat_list = []

        for sublist in sudoku_board:

            for item in sublist:

                flat_list.append(item)

        solved_numbers = flat_list * position_array

        image = self.display_number_on_image(image , solved_numbers)

        return image

    def draw_grid(self,image):

        secW = int(image.shape[1]/9)
        secH = int(image.shape[0]/9)

        for i in range (0,9):

            pt1 = (0,secH*i)
            pt2 = (image.shape[1],secH*i)
            pt3 = (secW * i, 0)
            pt4 = (secW*i,image.shape[0])
            cv2.line(image, pt1, pt2, (255, 255, 0),2)
            cv2.line(image, pt3, pt4, (255, 255, 0),2)

        return image




    def display_number_on_image(self,image , numbers ,color = (0,255,0)):

        secW = int(image.shape[1]/9)
        secH = int(image.shape[0]/9)
        for x in range (0,9):
            for y in range (0,9):
                if numbers[(y*9)+x] != 0 :
                     cv2.putText(image, str(numbers[(y*9)+x]),
                                   (x*secW+int(secW/2)-10, int((y+0.8)*secH)), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                2, color, 2, cv2.LINE_AA)
        return image

    def solve_board(self):

        if self.find_biggest_contour_area().size ==0: return
        
        reordered_biggest_area_coords = self.image_processor.reorder_max_contour_area_points(self.find_biggest_contour_area())
        self.image_big_contour = cv2.drawContours(self.image_big_contour , reordered_biggest_area_coords , -1 , (0,0,255),25)

        source_points = np.float32(reordered_biggest_area_coords)
        target_points = np.float32([[0, 0], [self.image_width, 0], [0, self.image_height], [self.image_width, self.image_height]]) 

        image_warp_colored = self.image_processor.image_warp_perspective(
                self.image, source_points,target_points , self.image_width, self.image_height
                )
        image_warp_colored = cv2.cvtColor(image_warp_colored, cv2.COLOR_BGR2GRAY)

        image_detected_digits = self.image_blank.copy()

        image_solved_digits = self.image_blank.copy()

        splited_boxes = self.image_processor.split_image(image_warp_colored)

        predicted_numbers = self.predictor.get_predicton(splited_boxes)

        image_detected_digits = self.display_number_on_image(image_detected_digits , predicted_numbers)

        predicted_numbers = np.asarray(predicted_numbers)

        position_array = np.where(predicted_numbers > 0 , 0 ,1)

        sudoku_board = np.array_split(predicted_numbers , 9)

        try:
            self.solver.solve(sudoku_board)
        
        except Exception as e:

            raise e

        image_solved_digits = self.flatting_predicted_number_position(image_solved_digits,position_array,sudoku_board)
        
        image_inv_warp_colored = self.image.copy()

        source_points , target_points = target_points , source_points


        image_inv_warp_colored = self.image_processor.image_warp_perspective(image_solved_digits , source_points ,target_points , self.image_width , self.image_height)

        inv_perspective = cv2.addWeighted(image_inv_warp_colored , 1 , self.image , 0.5 ,1)

        return inv_perspective




