from tkinter import *  # Tk, Label, Button, Menu, Text, Entry
from tkinter import ttk
# from tkinter import LEFT, RIGHT, W, RAISED, GROOVE, RIDGE
import time
import numpy as np

from sudoku_solver import Sudoku


class SudokuGUI:
    def __init__(self):
        self.root = Tk()
        self.sudoku_grid = Sudoku(np.zeros((9, 9)).astype(int))
        self.root.title("Sudoku")
        self.init_grid()
        self.init_buttons()
        self.root.mainloop()

    def init_grid(self):
        self.entries = []
        for n in range(9 ** 2):
            self.entries.append(Entry(self.root, width=3, fg="black"))
            self.entries[n].config({"background": "white"})
            r = n // 9 + (n // 9) // 3
            c = int(n % 9) + (int(n % 9) // 3)
            self.entries[n].grid(row=r, column=c)

    def init_buttons(self):
        self.example_button = ttk.Button(self.root, text="Example", command=self.input_example)
        self.example_button.grid(row=1, column=14)

        self.generate_button = ttk.Button(self.root, text="Generate", command=self.generate)
        self.generate_button.grid(row=3, column=14)

        self.generate_slider = Scale(self.root, from_=0, to=10, orient=HORIZONTAL)
        self.generate_slider.grid(row=4, column=14)

        self.difficulty_label = ttk.Label(self.root, text="Difficulty")
        self.difficulty_label.grid(row=5, column=14)

        self.solve_button = ttk.Button(self.root, text="Solve", command=self.start_solve)
        self.solve_button.grid(row=6, column=14)

        self.check_button = ttk.Button(self.root, text="Check", command=self.check)
        self.check_button.grid(row=7, column=14)

        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_entries)
        self.clear_button.grid(row=9, column=14)

        self.quit_button = ttk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=10, column=14)

    def input_example(self):
        self.clear_entries()
        my_board = np.array([
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
        self.sudoku_grid.board = my_board
        for i in range(9):
            for j in range(9):
                if my_board[i][j] == 0:
                    continue
                self.entries[i * 9 + j].insert(END, my_board[i][j])

    def clear_entries(self):
        """Clears the entries in the GUI"""
        for i in range(9 ** 2):
            self.entries[i].delete(0, END)
            self.entries[i].config({"background": "white"})
            self.root.update()

    def generate(self):
        self.sudoku_grid.board = np.zeros((9, 9)).astype(int)
        self.clear_entries()
        self.get_gui_board()
        difficulty = self.generate_slider.get()
        # Solve then strip back
        rand_first_row = np.random.permutation(range(1, 10))
        for i in range(9):
            self.sudoku_grid.board[0, i] = rand_first_row[i]
            self.entries[i].insert(END, rand_first_row[i])
        self.solve()

        to_remove = 35 + 2 * difficulty
        rand_positions = np.random.randint(81, size=(1, to_remove))
        for pos in rand_positions[0]:
            self.entries[pos].delete(0, END)
        self.get_gui_board()
        for i in range(9 ** 2):
            self.entries[i].config({"background": "white"})
        self.root.update()

    def check(self):
        """Checks if complete and valid solution"""
        # TODO: refactor...
        valid = True
        self.get_gui_board()
        transpose_board = [[], [], [], [], [], [], [], [], []]

        boxes_as_rows = [[], [], [], [], [], [], [], [], []]
        for r in range(9):
            i_box = r // 3
            j_box = r % 3
            for i in range(i_box * 3, i_box * 3 + 3):
                for j in range(j_box * 3, j_box * 3 + 3):
                    boxes_as_rows[r].append(self.sudoku_grid.board[i, j])
            for c in range(9):
                transpose_board[r].append(self.sudoku_grid.board[c, r])
                self.entries[r * 9 + c].config({"background": "white"})

        for c in range(9):  # check rows
            row = self.sudoku_grid.board[c, :]
            col = transpose_board[c][:]
            if len(row) != len(np.unique(row)):
                for i in range(9):
                    self.entries[c * 9 + i].config({"background": "red"})
                valid = False
            if len(col) != len(np.unique(col)):
                for i in range(9):
                    self.entries[i * 9 + c].config({"background": "red"})
                valid = False
            if len(boxes_as_rows) != len(np.unique(boxes_as_rows)):
                i_box = c // 3
                j_box = c % 3
                for i in range(i_box * 3, i_box * 3 + 3):
                    for j in range(j_box * 3, j_box * 3 + 3):
                        self.entries[i * 9 + j].config({"background": "red"})
                valid = False
        if valid:
            for i in range(9 ** 2):
                self.entries[i].config({"background": "green"})
        return valid

    def get_gui_board(self):
        """Gets entries in GUI and returns a matrix of board entries"""
        elements = [e.get() for e in self.entries]
        for i in range(9):
            for j in range(9):
                if elements[i * 9 + j] == '':
                    self.sudoku_grid.board[i, j] = 0
                else:
                    self.sudoku_grid.board[i, j] = int(elements[i * 9 + j])

    def start_solve(self):
        print("Solving")
        start_time = time.time()
        self.get_gui_board()
        print(repr(self.sudoku_grid))
        self.solve()
        print("--- %s seconds ---" % (time.time() - start_time))

    def solve(self):
        next_pos = self.sudoku_grid.next_empty()
        if not next_pos:  # finished
            print("Finished:")
            # self.print_board()
            print(repr(self.sudoku_grid))
            return True
        for number in range(1, 10):  # try values
            if self.sudoku_grid.is_valid(number, next_pos):
                self.sudoku_grid.board[next_pos[0], next_pos[1]] = number
                self.place_value(number, next_pos)
                self.entries[next_pos[0] * 9 + next_pos[1]].config({"background": "green"})
                self.root.update()
                if self.solve():
                    return True
            self.sudoku_grid.board[next_pos[0], next_pos[1]] = 0
            self.place_value(0, next_pos)
            self.entries[next_pos[0] * 9 + next_pos[1]].config({"background": "red"})
            self.root.update()
        return False

    def place_value(self, num, pos):
        self.entries[pos[0] * 9 + pos[1]].delete(0, END)
        self.entries[pos[0] * 9 + pos[1]].insert(END, num)
        self.entries[pos[0] * 9 + pos[1]].config({"background": "green"})


def main():
    app = SudokuGUI()

    print("--------------------------")


if __name__ == '__main__':
    main()
