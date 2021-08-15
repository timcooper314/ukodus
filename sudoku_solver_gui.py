# Sudoku solver gui - use python3
from tkinter import *  # Tk, Label, Button, Menu, Text, Entry
# from tkinter import LEFT, RIGHT, W, RAISED, GROOVE, RIDGE
import time
import numpy as np


class SudokuGUI:
    def __init__(self):  # , master):
        # self.master = master
        self.root = Tk()
        self.board = [[], [], [], [], [], [], [], [], []]
        self.root.title("Sudoku")
        self.entries = []
        for n in range(9 ** 2):
            self.entries.append(Entry(self.root, width=3, fg="black"))
            self.entries[n].config({"background": "white"})
            r = n // 9 + (n // 9) // 3
            c = int(n % 9) + (int(n % 9) // 3)
            self.entries[n].grid(row=r, column=c)

        self.example_button = Button(self.root, text="Example", command=self.input_example)
        self.example_button.grid(row=1, column=14)

        self.generate_button = Button(self.root, text="Generate", command=self.generate)
        self.generate_button.grid(row=3, column=14)

        self.generate_slider = Scale(self.root, from_=0, to=10, orient=HORIZONTAL)
        self.generate_slider.grid(row=4, column=14)

        self.difficulty_label = Label(self.root, text="Difficulty")
        self.difficulty_label.grid(row=5, column=14)

        self.solve_button = Button(self.root, text="Solve", command=self.start_solve)
        self.solve_button.grid(row=6, column=14)

        self.check_button = Button(self.root, text="Check", command=self.check)
        self.check_button.grid(row=7, column=14)

        self.clear_button = Button(self.root, text="Clear", command=self.clear_entries)
        self.clear_button.grid(row=9, column=14)

        self.quit_button = Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=10, column=14)
        self.root.mainloop()

    def input_example(self):
        my_board = [
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
        for i in range(9):
            for j in range(9):
                if my_board[i][j] == 0:
                    continue
                self.entries[i * 9 + j].insert(END, my_board[i][j])
                # self.entries[i*9+j].config({"background":"blue"})

    def clear_entries(self):
        """Clears the entries in the GUI"""
        for i in range(9 ** 2):
            self.entries[i].delete(0, END)
            self.entries[i].config({"background": "white"})
            # root.update()

    def generate(self):
        self.clear_entries()
        self.get_board()
        difficulty = self.generate_slider.get()
        # Solve then strip back
        first_row = np.random.permutation(range(1, 10))
        for i in range(9):
            self.board[0][i] = first_row[i]
            self.entries[i].insert(END, first_row[i])
        self.solve()

        to_remove = 35 + 2 * difficulty
        rand_positions = np.random.randint(81, size=(1, to_remove))
        for j in range(to_remove):
            pos = rand_positions[0][j]
            self.entries[pos].delete(0, END)
        self.get_board()
        for i in range(9 ** 2):
            self.entries[i].config({"background": "white"})

        # By insertion
        # for i in range(17+20-2*difficulty):
        #     new_num = randint(1,9)
        #     x = randint(0,8)
        #     y = randint(0,8)
        #     if self.is_valid(new_num,[x,y]) and self.board[x][y]==0:
        #         self.board[x][y]=new_num
        #         self.entries[x*9+y].insert(END,new_num)
        #     else:
        #         i-=1

    def check(self):
        """Checks if complete and valid solution"""
        # change colour font for valid/not valid
        valid = 1
        self.get_board()
        transpose_board = [[], [], [], [], [], [], [], [], []]

        boxes_as_rows = [[], [], [], [], [], [], [], [], []]
        for r in range(9):
            iBox = r // 3
            jBox = r % 3
            for i in range(iBox * 3, iBox * 3 + 3):
                for j in range(jBox * 3, jBox * 3 + 3):
                    boxes_as_rows[r].append(self.board[i][j])

            for c in range(9):
                transpose_board[r].append(self.board[c][r])
                self.entries[r * 9 + c].config({"background": "white"})

        for c in range(9):  # check rows
            row = self.board[c][:]
            col = transpose_board[c][:]
            rows_duplicates = any(row.count(e) > 1 for e in row)
            cols_duplicates = any(col.count(e) > 1 for e in row)
            box_duplicates = any(boxes_as_rows.count(e) > 1 for e in row)
            # if rows_duplicates==True or cols_duplicates==True or box_duplicates==True:
            #     for i in range(9**2):
            #         self.entries[i].config({"background":"red"})
            #     return(0)
            if rows_duplicates == True:
                for i in range(9):
                    self.entries[c * 9 + i].config({"background": "red"})
                valid = 0
            if cols_duplicates == True:
                for i in range(9):
                    self.entries[i * 9 + c].config({"background": "red"})
                valid = 0
            if box_duplicates == True:
                iBox = c // 3
                jBox = c % 3
                for i in range(iBox * 3, iBox * 3 + 3):
                    for j in range(jBox * 3, jBox * 3 + 3):
                        self.entries[i * 9 + j].config({"background": "red"})
                valid = 0
        if valid:
            for i in range(9 ** 2):
                self.entries[i].config({"background": "green"})
        return (valid)

    def get_board(self):
        """Gets entries in GUI and returns a matrix of board entries"""
        self.board = [[], [], [], [], [], [], [], [], []]
        elements = [e.get() for e in self.entries]
        for i in range(9):
            for j in range(9):
                if elements[i * 9 + j] == '':
                    self.board[i].append(0)
                else:
                    self.board[i].append(int(elements[i * 9 + j]))
        return (self.board)

    def start_solve(self):
        print("Solving")
        start_time = time.time()
        self.board = self.get_board()
        self.print_board()
        self.solve()
        print("--- %s seconds ---" % (time.time() - start_time))

    def solve(self):
        nextPos = self.next_empty()
        if nextPos == 0:  # finished
            print("Finished:")
            self.print_board()
            return (1)
        for number in range(1, 10):  # try values
            # check if valid with number
            valid = self.is_valid(number, nextPos)
            if valid:
                self.board[nextPos[0]][nextPos[1]] = number
                self.place_value(number, nextPos)
                self.entries[nextPos[0] * 9 + nextPos[1]].config({"background": "green"})
                # root.update()
                if self.solve():
                    return (1)
            self.board[nextPos[0]][nextPos[1]] = 0
            self.place_value(0, nextPos)
            self.entries[nextPos[0] * 9 + nextPos[1]].config({"background": "red"})
            self.root.update()
        return (0)

    def print_board(self, ):
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

    def next_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return ([i, j])
        return (0)

    def is_valid(self, num, pos):
        """"Checks validity of board with new number num in position pos"""
        # check row:
        for c in range(9):
            if self.board[pos[0]][c] == num and c != pos[1]:  # invalid
                return (0)
        # check column:
        for r in range(9):
            if self.board[r][pos[1]] == num and r != pos[0]:  # invalid
                return (0)
        # check box:
        iBox = pos[0] // 3  # integer division
        jBox = pos[1] // 3
        for i in range(iBox * 3, iBox * 3 + 3):
            for j in range(jBox * 3, jBox * 3 + 3):
                if self.board[i][j] == num and [i, j] != pos:
                    return (0)
        return (1)

    def place_value(self, num, pos):
        self.entries[pos[0] * 9 + pos[1]].delete(0, END)
        self.entries[pos[0] * 9 + pos[1]].insert(END, num)
        # self.entries[pos[0] *9 +pos[1]].config({"background":"green"})
        # root.update()


def main():
    # root = Tk()
    # myGUI = SudokuGUI(root)
    # root.mainloop()
    app = SudokuGUI()

    print("--------------------------")


if __name__ == '__main__':
    main()
