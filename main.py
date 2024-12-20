import tkinter as tk
import random


class Game:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("3D-Minesweeper")
        self._root.config(bg="#384048")
        self._images = {}
        self._board = [[[None for _ in range(6)] for _ in range(6)] for _ in range(6)]
        self.load_images()
        self.create_grids()
        self.draw_tiles()
        self.initialize_tile_states(20)

        self._root.update_idletasks()
        self._root.geometry(f"{self._root.winfo_reqwidth()}x{self._root.winfo_reqheight()}")
        self._root.resizable(False, False)

    def load_images(self):
        """Load and store images for efficient reuse."""
        self._images["flag"] = tk.PhotoImage(file="assets/flag.png").subsample(3, 3)
        self._images["field"] = tk.PhotoImage(file="assets/field.png").subsample(3, 3)
        self._images["base"] = tk.PhotoImage(file="assets/base.png").subsample(3, 3)
        self._images["mine"] = tk.PhotoImage(file="assets/mine.png").subsample(3, 3)
        for number in range(1, 27):
            self._images[str(number)] = tk.PhotoImage(file=f"assets/numbers/{number}.png").subsample(3, 3)

    def create_grids(self):
        """Create 2x3 grid layout for the smaller grids with spacing."""
        for grid_row in range(2 * 7 + 1):
            self._root.grid_rowconfigure(grid_row, weight=0, minsize=20)

        for grid_col in range(3 * 7 + 1):
            self._root.grid_columnconfigure(grid_col, weight=0, minsize=20)

    def initialize_tile_states(self, mine_count):
        all_tiles = [tile for layer in self._board for row in layer for tile in row]
        mines = random.sample(all_tiles, mine_count)
        for mine_tile in mines:
            mine_tile._mine = True

        for tile in all_tiles:
            if not tile._mine:
                tile._adjacent_mines = sum(
                    1 for neighbor in self.get_neighbors(tile) if neighbor._mine
                )

    def get_neighbors(self, tile, range_size=1):
        """Get neighbors within the specified range in a 6x6x6 grid."""
        neighbors = []
        tile_x, tile_y, tile_z = tile._x, tile._y, tile._z

        for dx in range(-range_size, range_size + 1):
            for dy in range(-range_size, range_size + 1):
                for dz in range(-range_size, range_size + 1):
                    if dx == 0 and dy == 0 and dz == 0:
                        continue

                    neighbor_x = tile_x + dx
                    neighbor_y = tile_y + dy
                    neighbor_z = tile_z + dz

                    if 0 <= neighbor_x < 6 and 0 <= neighbor_y < 6 and 0 <= neighbor_z < 6:
                        neighbors.append(self._board[neighbor_z][neighbor_x][neighbor_y])
        return neighbors

    def draw_tiles(self):
        """Draw tiles as a 2x3 grid layout on the main window while maintaining a 6x6x6 structure."""
        for z in range(6):
            grid_row = z // 3
            grid_col = z % 3
            for x in range(6):
                for y in range(6):
                    absolute_row = grid_row * 7 + x + 1  # Offset by 1 row
                    absolute_col = grid_col * 7 + y + 1  # Offset by 1 column
                    tile = Tile(self, x, y, z)
                    tile.create_button(self._root, absolute_row, absolute_col)
                    self._board[z][x][y] = tile

    def run(self):
        self._root.mainloop()

    def get_images(self):
        """Provide image assets to the Tile class."""
        return self._images


class Tile:
    def __init__(self, game, x, y, z):
        self._game = game
        self._x = x
        self._y = y
        self._z = z
        self._flagged = False
        self._revealed = False
        self._mine = False
        self._adjacent_mines = 0
        self._button = None

    def create_button(self, parent, x, y):
        """Create and manage the button for this tile."""
        images = self._game.get_images()
        self._button = tk.Button(parent, image=images["field"], bg="Gray", relief="flat", padx=0, pady=-5)
        self._button.grid(row=x, column=y, padx=0, pady=0)
        self._button.bind("<Button-1>", lambda event: self.reveal())
        self._button.bind("<Button-3>", lambda event: self.toggle_flag())
        self._button.bind("<Enter>", lambda event: self.highlight())
        self._button.bind("<Leave>", lambda event: self.reset_highlights())

    def reveal(self):
        """Handle revealing the tile."""
        if self._flagged:
            return False

        images = self._game.get_images()

        image_str = str(self._adjacent_mines) if self._adjacent_mines > 0 else "mine" if self._mine else "base"

        self._revealed = True
        self._button.config(
            image=images[image_str],
            font=("Helvetica", 10, "bold"),
            fg="blue" if self._adjacent_mines > 0 else "red",
        )

        return True

    def toggle_flag(self):
        if self._revealed:
            return False

        self._flagged = not self._flagged
        images = self._game.get_images()

        if self._flagged:
            self._button.config(image=images["flag"], text="")
        else:
            self._button.config(image=images["field"], text="")

    def highlight(self):
        """Highlight the neighbors in a 3x3x3 cube."""
        neighbors = self._game.get_neighbors(self, range_size=1)
        for tile in neighbors:
            tile._button.config(bg="yellow")
        self._button.config(bg="red")

    def reset_highlights(self):
        """Reset the neighbors' background color."""
        neighbors = self._game.get_neighbors(self, range_size=1)
        for tile in neighbors:
            tile._button.config(bg="Gray")
        self._button.config(bg="Gray")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
