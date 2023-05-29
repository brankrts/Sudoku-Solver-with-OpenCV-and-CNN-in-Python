import cv2
from sudoku_visualizer import SudokuVisualizer
import argparse

class Main:

    def __init__(self,image_path) -> None:

        self.image_path = image_path
        self.sudoku_visualizer = SudokuVisualizer(image_path)

    def start(self):

        image = self.sudoku_visualizer.solve_board()
        cv2.imshow("Solved Sukodu" , image)

        cv2.waitKey(0)
        


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Cozmesini istediginiz resimler icin sudoku cozucu ornegi")

    parser.add_argument('--path' , type=str , help = 'islenecek resim icin dosya yolu')

    args = parser.parse_args()


    main = Main(args.path)
    main.start()

        









