import tkinter as tk


class Game:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("3D-Minesweeper")
        self._root.geometry("600x400")  # Adjust window size if necessary
        self._images = {}
        self._board = []  # Stores the tiles for all grids
        self.load_images()
        self.create_grids()
        self.draw_tiles()

    def load_images(self):
        """Load and store images for efficient reuse."""
        self._images["flag"] = tk.PhotoImage(file="assets/flag.png").subsample(5, 5)
        self._images["field"] = tk.PhotoImage(file="assets/field.png").subsample(5, 5)

    def create_grids(self):
        """Create 2x3 grid layout for the smaller grids."""
        for grid_row in range(2):
            for grid_col in range(3):
                for row in range(6):
                    self._root.grid_rowconfigure(grid_row * 6 + row, weight=0)
                for col in range(6):
                    self._root.grid_columnconfigure(grid_col * 6 + col, weight=0)

    def draw_tiles(self):
        """Draw 6x6 grids directly on the main window."""
        for grid_row in range(2):
            for grid_col in range(3):
                grid_tiles = []
                for row in range(6):
                    for col in range(6):
                        absolute_row = grid_row * 6 + row
                        absolute_col = grid_col * 6 + col
                        tile = Tile(self, absolute_row, absolute_col)
                        tile.create_button(self._root, absolute_row, absolute_col)
                        grid_tiles.append(tile)
                self._board.append(grid_tiles)

    def run(self):
        self._root.mainloop()

    def get_images(self):
        """Provide image assets to the Tile class."""
        return self._images


class Tile:
    def __init__(self, game, x, y):
        self._game = game
        self._flagged = False
        self._revealed = True
        self._mine = True
        self._adjacent_mines = 0
        self._x = x
        self._y = y
        self._button = None

    def create_button(self, parent, x, y):
        """Create and manage the button for this tile."""
        images = self._game.get_images()
        self._button = tk.Button(parent, image=images["field"], bg="Gray", relief="flat", padx=0, pady=-5)
        self._button.grid(row=x, column=y, padx=1, pady=1)
        self._button.bind("<Button-1>", lambda event: self.reveal())
        self._button.bind("<Button-3>", lambda event: self.toggle_flag())

    def reveal(self):
        """Handle revealing the tile."""
        if self._flagged:
            return False

        self._revealed = True
        self._button.config(
            bg="White",
            image="",
            text=str(self._adjacent_mines) if not self._mine else "*",
            font=("Helvetica", 10, "bold"),  # Adjust font size to balance readability
            fg="blue" if self._adjacent_mines > 0 else "red",  # Add color differentiation

        )

        return True

    def toggle_flag(self):
        if self._revealed:
            return False

        self._flagged = not self._flagged
        images = self._game.get_images()

        if self._flagged:
            self._button.config(image=images["flag"], text="")  # Place image on the button
        else:
            self._button.config(image=images["field"], text="")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
