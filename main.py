import tkinter as tk
import colorscheme as color
import random


class Game(tk.Frame):
    def __int__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("Alex's 2048")

        self.main_grid = tk.Frame(
            self, bg=color.GRID_COLOR, bd=3, width=600, height=600
        )
        self.main_grid.grid(pady=(100,0))
        self.GUI()
        self.begin_game()

        self.mainloop()


    def GUI(self):
        # Create Grid
        self.cells = []
        for r in range(4):
            row = []
            for c in range(4):
                cell_frame = tk.Frame(
                    self.main_grid,
                    bg=color.EMPTY_CELL_COLOR,
                    width=150,
                    height=150
                )
                cell_frame.grid(row=r, column=c, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=color.EMPTY_CELL_COLOR)
                cell_number.grid(row=r, column=c)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # Create Score Header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(
            score_frame,
            text="Score: ",
            font=color.SCORE_LABEL_FONT
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=color.SCORE_FONT)
        self.score_label.grid(row=1)


    def begin_game(self):
        # Create Matrix of Zeroes
        self.matrix = [[0] * 4 for _ in range(4)]

        # fill 2 random cells with 2's
        row = random.randint(0, 3)
        column = random.randint(0, 3)
        self.matrix[row][column] = 2
        self.cells[row][column]["frame"].configure(bg=color.COLORS[2])
        self.cells[row][column]["number"].configure(
            bg=color.COLORS[2],
            fg=color.NUM_COLORS[2],
            font=color.NUM_FONTS[2],
            text="2"
        )
        while(self.matrix[row][column] != 0):
            row = random.randint(0, 3)
            column = random.randint(0, 3)
        self.matrix[row][column] = 2
        self.cells[row][column]["frame"].configure(bg=color.COLORS[2])
        self.cells[row][column]["number"].configure(
            bg=color.COLORS[2],
            fg=color.NUM_COLORS[2],
            font=color.NUM_FONTS[2],
            text="2"
        )

        self.score = 0


    # Matrix Manipulation Functions

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for r in range(4):
            fill_position = 0
            for c in range(4):
                if self.matrix[r][c] != 0:
                    new_matrix[r][fill_position] = self.matrix[r][c]
                    fill_position += 1
        self.matrix = new_matrix
