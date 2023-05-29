


class SudokuSolver:



    def __init__(self):
        pass


    def solve(self,board):

        empty_coords = self.find_empty(board)

        if not empty_coords: return True

        row , col = empty_coords

        for i in range(1,10):

            if self.is_valid(board , i , (row , col)):

                board[row][col] = i

                if self.solve(board): return True

                board[row][col] = 0

        return False

    
    def is_valid(self, board , num , pos):

        for i in range(len(board[0])):

            if board[pos[0]][i] ==num and pos[1] != i : return False

        for i in range(len(board)):

            if board[i][pos[1]] == num and pos[0] !=i : return False

        box_x = pos[1] // 3
        box_y = pos[0] // 3 

        for i in range(box_y*3 , box_y*3 +3):

            for j in range(box_x * 3 , box_x *3  + 3):

                if board[i][j] == num and (i, j ) != pos: return False

        return True

    def find_empty(self,board):
        
        for i in range(len(board)):

            for j in range(len(board[0])):

                if board[i][j] ==0: return (i,j)

        return None

