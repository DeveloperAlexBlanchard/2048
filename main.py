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

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    # # Creates the GUI
    
    def GUI(self):
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

        # # Score Header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5, y=45, anchor="center")
        tk.Label(
            score_frame,
            text="Score: ",
            font=color.SCORE_LABEL_FONT
        ).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=color.SCORE_FONT)
        self.score_label.grid(row=1)

    # # Sets up the Game for the Player
    
    def begin_game(self):
        # # Create Matrix of Zeroes
        self.matrix = [[0] * 4 for _ in range(4)]

        # # Fill 2 random cells with 2's
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


    # # Matrix Manipulation Functions

    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for r in range(4):
            fill_position = 0
            for c in range(4):
                if self.matrix[r][c] != 0:
                    new_matrix[r][fill_position] = self.matrix[r][c]
                    fill_position += 1
        self.matrix = new_matrix


    def combine(self):
        for r in range(4):
            for c in range(3):
                if self.matrix[r][c] != 0 and self.matrix[r][c] == self.matrix[r][c + 1]:
                    self.matrix[r][c] *= 2
                    self.matrix[r][c + 1] = 0
                    self.score += self.matrix[r][c]


    def reverse(self):
        new_matrix = []
        for r in range(4):
            new_matrix.append([])
            for c in range(4):
                new_matrix[r].append(self.matrix[r][3 - c])
        self.matrix = new_matrix


    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for r in range(4):
            for c in range(4):
                new_matrix[r][c] = self.matrix[r][c]
        self.matrix[r][c] = new_matrix


    # # Add a new tile (2 or 4) randomly to an empty cell

    def add_tile(self):
        row = random.randint(0, 3)
        column = random.randint(0, 3)
        while (self.matrix[row][column] != 0):
            row = random.randint(0, 3)
            column = random.randint(0, 3)
        self.matrix[row][column] = random.choice([2, 4])


    # # Update GUI to match the matrix

    def update_GUI(self):
        for r in range(4):
            for c in range(4):
                cell_value = self.matrix[r][c]
                if cell_value == 0:
                    self.cells[r][c]["frame"].configure(bg=color.EMPTY_CELL_COLOR)
                    self.cells[r][c]["number"].configure(bg=color.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[r][c]["frame"].configure(bg=color.COLORS[cell_value])
                    self.cells[r][c]["number"].configure(
                        bg=color.COLORS[cell_value],
                        fg=color.NUM_COLORS[cell_value],
                        font=color.NUM_FONTS[cell_value],
                        text=str(cell_value)
                    )
        self.score_label.configure(text=self.score)
        self.update_idletasks()


    # # Keyboard Controls

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_tile()
        self.update_GUI()
        self.game_over()


    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_tile()
        self.update_GUI()
        self.game_over()


    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_tile()
        self.update_GUI()
        self.game_over()


    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_tile()
        self.update_GUI()
        self.game_over()

    # # Check if any moves are possible

    def can_move_horizontal(self):
        for r in range(4):
            for c in range(4):
                if self.matrix[r][c] == self.matrix[r][c + 1]:
                    return True
        return False


    def can_move_vertical(self):
        for r in range(3):
            for c in range(4):
                if self.matrix[r][c] == self.matrix[r + 1][c]:
                    return True
        return False

    # # Check if game is over (Win/Lose)

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_screen = tk.Frame(self.main_grid, borderwidth=2)
            game_over_screen.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_screen,
                text="You Win!",
                bg=color.WINNER_BG,
                fg=color.GAME_OVER_FONT_COLOR,
                font=color.GAME_OVER_FONT
            ).pack()
        elif not any(0 in row for row in self.matrix) and not self.can_move_horizontal() and not self.can_move_vertical():
            game_over_screen = tk.Frame(self.main_grid, borderwidth=2)
            game_over_screen.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_screen,
                text="Game Over!",
                bg=color.LOSER_BG,
                fg=color.GAME_OVER_FONT_COLOR,
                font=color.GAME_OVER_FONT
            ).pack()

def main():
    Game()

if __name__ == "__main__":
    main()
