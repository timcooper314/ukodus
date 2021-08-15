import time
import numpy as np


class Sudoku:
    def __init__(self, board):
        self.board = board

    def __repr__(self):
        m = ""
        for i in range(9):
            if i % 3 == 0:
                m += "_______________________________\n"
            for j in range(9):
                if j % 3 == 0:
                    m += " | "
                else:
                    m += "  "
                if j == 8:
                    m += f"{str(self.board[i][j])}\n"
                else:
                    m += str(self.board[i][j])
        m += "_______________________________\n"
        return m

    def solve(self):
        next_pos = self.next_empty()
        if not next_pos:  # finished
            print("Finished:")
            print(repr(self))
            return True
        for number in range(1, 10):  # try values
            # check if valid with number
            if self.is_valid(number, next_pos):
                self.board[next_pos[0]][next_pos[1]] = number
                if self.solve():
                    return True
            self.board[next_pos[0]][next_pos[1]] = 0
        return False

    def next_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return [i, j]
        return False

    def is_valid(self, num, pos):
        """"Checks validity of board with new number num in position pos"""
        # check row:
        for c in range(9):
            if self.board[pos[0]][c] == num and c != pos[1]:  # invalid
                return False
        # check column:
        for r in range(9):
            if self.board[r][pos[1]] == num and r != pos[0]:  # invalid
                return False
        # check box:
        i_box = pos[0] // 3  # integer division
        j_box = pos[1] // 3
        for i in range(i_box * 3, i_box * 3 + 3):
            for j in range(j_box * 3, j_box * 3 + 3):
                if self.board[i][j] == num and [i, j] != pos:
                    return False
        return True


def main():
    input_board = np.array([
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ])
    sudoku_board = Sudoku(input_board)
    print(repr(sudoku_board))
    sudoku_board.solve()
    print("--------------------------")


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
