import time


class Sudoku:
    def __init__(self, board):
        self.board = board

    def print_board(self):
        for i in range(9):
            if i % 3 == 0:
                print("___________________")
            for j in range(9):
                if j % 3 == 0:
                    print("|", end="")  # ,
                else:
                    print(' ', end="")  # ,
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(self.board[i][j], end="")  # ,
        print("___________________")

    def solve(self):
        next_pos = self.next_empty()
        if not next_pos:  # finished
            print("Finished:")
            self.print_board()
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
        iBox = pos[0] // 3  # integer division
        jBox = pos[1] // 3
        for i in range(iBox * 3, iBox * 3 + 3):
            for j in range(jBox * 3, jBox * 3 + 3):
                if self.board[i][j] == num and [i, j] != pos:
                    return False
        return True


def main():
    input_board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    sudoku_board = Sudoku(input_board)
    sudoku_board.print_board()
    sudoku_board.solve()
    print("--------------------------")


if __name__ == '__main__':
    main()
