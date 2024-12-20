import tkinter as tk


class Game:
    def __init__(self):
        self._board = [
            [[[None, Tile()] for _ in range(6)] for _ in range(6)] for _ in range(6)
        ]
        self._root = tk.Tk()
        self._root.title("3D-Minesweeper")
        self._root.geometry("600x650")
        self._root.grid_columnconfigure(7, minsize=10)
        self._root.grid_columnconfigure(15, minsize=10)
        self._root.grid_rowconfigure(7, minsize=20)
        self._root.grid_rowconfigure(15, minsize=20)
        self.draw_buttons()

    def draw_buttons(self):
        for x in range(6):
            for y in range(6):
                for z in range(6):
                    button = tk.Button(
                        self._root, text=" ", width=2, height=1, bg="Gray"
                    )
                    button.grid(row=y, column=z + x * 8)
                    button.bind(
                        "<Button-1>",
                        lambda event, x_=x, y_=y, z_=z: self._left_click(x_, y_, z_),
                    )
                    button.bind(
                        "<Button-3>",
                        lambda event, x_=x, y_=y, z_=z: self._right_click(x_, y_, z_),
                    )
                    button.bind(
                        "<Enter>",
                        lambda event, x_=x, y_=y, z_=z: self._button_hover(x_, y_, z_),
                    )
                    button.bind(
                        "<Leave>",
                        lambda event, x_=x, y_=y, z_=z: self._button_unhover(
                            x_, y_, z_
                        ),
                    )

                    self._board[x][y][z][0] = button  # type: ignore

    def run(self):
        self._root.mainloop()

    def _left_click(self, x, y, z):
        self._board[x][y][z][1]._revealed = not self._board[x][y][z][1]._revealed
        print(f"Left click ({x}|{y}|{z}) {self._board[x][y][z][1]._revealed} ")

    def _right_click(self, x, y, z):
        print(f"Right click ({x}|{y}|{z}) ")

    def _button_hover(self, x, y, z):
        for h in range(-1, 2):
            if 0 <= x + h < 6:
                for i in range(-1, 2):
                    if 0 <= y + i < 6:
                        if 0 <= z - 1 < 6:
                            self._board[x + h][y + i][z - 1][0].config(bg="yellow")
                        self._board[x + h][y + i][z][0].config(bg="yellow")
                        if 0 <= z + 1 < 6:
                            self._board[x + h][y + i][z + 1][0].config(bg="yellow")

    def _button_unhover(self, x, y, z):
        for h in range(-1, 2):
            if 0 <= x + h < 6:
                for i in range(-1, 2):
                    if 0 <= y + i < 6:
                        if 0 <= z - 1 < 6:
                            self._board[x + h][y + i][z - 1][0].config(bg="Gray")
                        self._board[x + h][y + i][z][0].config(bg="Gray")
                        if 0 <= z + 1 < 6:
                            self._board[x + h][y + i][z + 1][0].config(bg="Gray")


class Tile:
    def __init__(self):
        self._flagged = False
        self._revealed = False
        self._mine = False
        self._adjacent_mines = 0


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
