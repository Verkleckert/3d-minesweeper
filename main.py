import tkinter as tk

class Game:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("3D-Minesweeper")
        self._root.geometry("900x600")  # Adjusted for a better 2x3 grid layout
        self._images = {}
        self._frames = []
        self._board = []  # Stores the tiles for all frames
        self.load_images()
        self.create_grids()
        self.draw_tiles()

    def load_images(self):
        """Load and store images for efficient reuse."""
        flag_image = tk.PhotoImage(file="assets/flag.png")
        self._images["flag"] = flag_image # Adjust image size to fit larger buttons

    def create_grids(self):
        """Create 2x3 grid layout for the smaller grids."""
        for frame_row in range(2):
            for frame_col in range(3):
                frame = tk.Frame(self._root, bg="black", width=250, height=250)
                frame.grid(row=frame_row, column=frame_col, padx=10, pady=10)
                frame.grid_propagate(False)  # Prevent resizing of frames
                self._frames.append(frame)

    def draw_tiles(self):
        """Draw 6x6 grids inside each frame."""
        for frame in self._frames:
            frame_tiles = []
            for row in range(6):
                for col in range(6):
                    tile = Tile(self, row, col)
                    tile.create_button(frame, row, col)
                    frame_tiles.append(tile)
            self._board.append(frame_tiles)

    def run(self):
        self._root.mainloop()

    def get_images(self):
        """Provide image assets to the Tile class."""
        return self._images


class Tile:
    def __init__(self, game, x, y):
        self._game = game
        self._flagged = False
        self._revealed = False
        self._mine = False
        self._adjacent_mines = 0
        self._x = x
        self._y = y
        self._button = None

    def create_button(self, frame, x, y):
        """Create and manage the button for this tile."""
        self._button = tk.Button(
            frame,
            bg="Gray",
            relief="flat",
            width=3,  # Increased width
            height=2,  # Increased height
        )
        self._button.grid(row=x, column=y, padx=2, pady=2)
        self._button.bind("<Button-1>", lambda event: self.reveal())
        self._button.bind("<Button-3>", lambda event: self.toggle_flag())

    def reveal(self):
        """Handle revealing the tile."""
        if self._flagged:
            return False
        self._revealed = True
        self._button.config(bg="White", text=str(self._adjacent_mines) if not self._mine else "*")
        return True

    def toggle_flag(self):
        if self._revealed:
            return False
        self._flagged = not self._flagged
        images = self._game.get_images()
        if self._flagged:
            self._button.config(image=images["flag"], text="")  # Place image on the button
        else:
            self._button.config(image="", text=" ")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
