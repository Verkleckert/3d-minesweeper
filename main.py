import tkinter as tk


class Game:
    def __init__(self):
        self._board = [[[None for _ in range(6)] for _ in range(6)] for _ in range(6)]
        self._root = tk.Tk()
        self._root.title("3D-Minesweeper")
        self._root.geometry("600x650")
        self._root.grid_columnconfigure(7, minsize=10)
        self._root.grid_columnconfigure(15, minsize=10)
        self._root.grid_rowconfigure(7, minsize=20)
        self._root.grid_rowconfigure(15, minsize=20)

    def draw_buttons(self):
        for x in range(6):
            for y in range(6):
                for z in range(6):
                    self._board[x][y][z] = tk.Button(self._root, text=" ", width=2, height=1)
                    self._board[x][y][z].grid(row=y, column=z + x * 8)
                    self._board[x][y][z].bind("<Button-1>",
                                              lambda event, x_=x, y_=y, z_=z: self._left_click(x_, y_, z_))
                    self._board[x][y][z].bind("<Button-3>",
                                              lambda event, x_=x, y_=y, z_=z: self._right_click(x_, y_, z_))
                    self._board[x][y][z].bind("<Enter>",
                                              lambda event, x_=x, y_=y, z_=z: self._button_hover(x_, y_, z_))
                    self._board[x][y][z].bind("<Leave>",
                                              lambda event, x_=x, y_=y, z_=z: self._button_unhover(x_, y_, z_))

    def run(self):
        self._root.mainloop()

    @staticmethod
    def _left_click(x, y, z):
        print("Left click")

    @staticmethod
    def _right_click(x, y, z):
        print("Right click")

    def _button_hover(self, x, y, z):
        for h in range(-1, 2):
            if 0 <= x + h < 6:
                for i in range(-1, 2):
                    if 0 <= y + i < 6:
                        if 0 <= z - 1 < 6:
                            self._board[x + h][y + i][z - 1].config(bg="yellow")
                        self._board[x + h][y + i][z].config(bg="yellow")
                        if 0 <= z + 1 < 6:
                            self._board[x + h][y + i][z + 1].config(bg="yellow")

    def _button_unhover(self, x, y, z):
        for h in range(-1, 2):
            if 0 <= x + h < 6:
                for i in range(-1, 2):
                    if 0 <= y + i < 6:
                        if 0 <= z - 1 < 6:
                            self._board[x + h][y + i][z - 1].config(bg="SystemButtonFace")
                        self._board[x + h][y + i][z].config(bg="SystemButtonFace")
                        if 0 <= z + 1 < 6:
                            self._board[x + h][y + i][z + 1].config(bg="SystemButtonFace")


class Tile:
    def __init__(self):
        self._flagged = False
        self._revealed = False
        self._mine = False
        self._adjacent_mines = 0


def main():
    game = Game()
    game.draw_buttons()
    game.run()


if __name__ == "__main__":
    main()
