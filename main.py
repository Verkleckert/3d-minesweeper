import tkinter as tk
import random


class Game:
    GRID_SIZE = 6
    MINE_COUNT = 35
    COLOR_MAP = {
        0: "lightgray",
        1: "blue",
        2: "green",
        3: "red",
        4: "purple",
        5: "orange",
        6: "cyan",
        7: "pink",
        8: "brown",
        9: "yellow",
    }

    def __init__(self):
        self.root_window = tk.Tk()
        self.root_window.title("3D-Minesweeper")
        self.root_window.config(bg="#384048")

        self._images = {}
        self._board = [[[None for _ in range(Game.GRID_SIZE)] for _ in range(Game.GRID_SIZE)] for _ in
                       range(Game.GRID_SIZE)]
        self.over = False
        self.reset_window = None
        self.hovered_tile = None

        self.grid_frame = tk.Frame(self.root_window, bg="#384048")
        self.grid_frame.pack(side="top", pady=10)

        self.load_images()
        self.setup_grid_layout()
        self.initialize_board()

        self.root_window.update_idletasks()
        self.root_window.geometry(f"{self.root_window.winfo_reqwidth()}x{self.root_window.winfo_reqheight()}")
        self.root_window.resizable(False, False)
        self.root_window.bind_all("<KeyPress>", self.process_key_input)

    def load_images(self):
        self._images = {
            "flag": tk.PhotoImage(file="assets/flag.png").subsample(3, 3),
            "field": tk.PhotoImage(file="assets/field.png").subsample(3, 3),
            "base": tk.PhotoImage(file="assets/base.png").subsample(3, 3),
            "mine": tk.PhotoImage(file="assets/mine.png").subsample(3, 3),
        }
        for number in range(1, 27):
            self._images[str(number)] = tk.PhotoImage(file=f"assets/numbers/{number}.png").subsample(3, 3)

    def setup_grid_layout(self):
        for row in range(2 * Game.GRID_SIZE // 3 * (Game.GRID_SIZE + 1) - 1):  # Adjust rows to remove extra space
            self.grid_frame.grid_rowconfigure(row, weight=0, minsize=3 if row % (Game.GRID_SIZE + 1) == 0 else 20)
        for col in range(3 * Game.GRID_SIZE // 3 * (Game.GRID_SIZE + 1) - 1):  # Adjust columns to remove extra space
            self.grid_frame.grid_columnconfigure(col, weight=0, minsize=3 if col % (Game.GRID_SIZE + 1) == 0 else 20)

    def initialize_board(self):
        for z in range(Game.GRID_SIZE):
            grid_row = z // 3
            grid_col = z % 3
            for x in range(Game.GRID_SIZE):
                for y in range(Game.GRID_SIZE):
                    absolute_row = grid_row * (Game.GRID_SIZE + 1) + x + 1
                    absolute_col = grid_col * (Game.GRID_SIZE + 1) + y + 1
                    tile = Tile(self, x, y, z)
                    tile.create_button(self.grid_frame, absolute_row, absolute_col)
                    self._board[z][x][y] = tile
        self.set_mine_states()

    def set_mine_states(self):
        all_tiles = [tile for layer in self._board for row in layer for tile in row]
        mines = random.sample(all_tiles, Game.MINE_COUNT)
        for mine_tile in mines:
            mine_tile._mine = True

        for tile in all_tiles:
            if not tile._mine:
                tile._adjacent_mines = sum(1 for neighbor in self.find_adjacent_tiles(tile) if neighbor._mine)

    def find_adjacent_tiles(self, tile, range_size=1):
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

                    if 0 <= neighbor_x < Game.GRID_SIZE and 0 <= neighbor_y < Game.GRID_SIZE and 0 <= neighbor_z < Game.GRID_SIZE:
                        neighbors.append(self._board[neighbor_z][neighbor_x][neighbor_y])
        return neighbors

    def process_key_input(self, event):
        if self.hovered_tile:
            key = event.keysym
            if key.isdigit():
                number = int(key)
                color = Game.COLOR_MAP.get(number, "gray")
                self.hovered_tile._button.config(bg=color)
                self.hovered_tile.marker_color = color
            elif key == "BackSpace":
                self.hovered_tile._button.config(bg="Gray")
                self.hovered_tile.marker_color = None

    def reset_game(self):
        self.over = False
        if self.reset_window:
            self.reset_window.destroy()
        for layer in self._board:
            for row in layer:
                for tile in row:
                    tile.reset()
        self.set_mine_states()

    def end_game(self):
        self.over = True
        self.show_reset_window()

    def show_reset_window(self):
        self.reset_window = tk.Toplevel(self.root_window)
        self.reset_window.title("Game Over")
        self.reset_window.geometry("200x100")
        self.reset_window.resizable(False, False)
        tk.Label(self.reset_window, text="Game Over!", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.reset_window, text="Reset", command=self.reset_game, bg="red", fg="white").pack(pady=10)

    def run(self):
        self.root_window.mainloop()


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
        self.marker_color = None

    def create_button(self, parent, row, col):
        images = self._game._images
        self._button = tk.Button(parent, image=images["field"], bg="Gray", relief="flat", padx=0, pady=-5)
        self._button.grid(row=row, column=col, padx=0, pady=0)
        self._button.bind("<Button-1>", lambda event: self.reveal())
        self._button.bind("<Button-2>", lambda event: self.reveal_adjacent_highlighted())
        self._button.bind("<Button-3>", lambda event: self.toggle_flag())
        self._button.bind("<Enter>", lambda event: self.highlight())
        self._button.bind("<Leave>", lambda event: self.reset_highlights())

    def reveal(self):
        if self._flagged or self._game.over or self._revealed:
            return

        images = self._game._images
        if self._mine:
            self._button.config(image=images["mine"])
            self._game.end_game()
        else:
            image_str = str(self._adjacent_mines) if self._adjacent_mines > 0 else "base"
            self._button.config(image=images[image_str])
        self._revealed = True

    def reveal_adjacent_highlighted(self):
        if self._game.over or self._revealed:
            return
        if self._mine:
            self.reveal()
        elif self._adjacent_mines == 0:
            self.flood_fill()
        else:
            self.reveal()

    def flood_fill(self):
        stack = [self]
        while stack:
            current_tile = stack.pop()
            if current_tile._revealed or current_tile._flagged or current_tile._mine:
                continue
            current_tile.reveal()
            if current_tile._adjacent_mines == 0:
                neighbors = self._game.find_adjacent_tiles(current_tile)
                stack.extend(neighbors)

    def toggle_flag(self):
        if self._revealed or self._game.over:
            return
        self._flagged = not self._flagged
        images = self._game._images
        self._button.config(image=images["flag"] if self._flagged else images["field"])

    def highlight(self):
        if self._game.over:
            return
        for tile in self._game.find_adjacent_tiles(self):
            if tile.marker_color is None:
                tile._button.config(bg="yellow")
        if self.marker_color is None:
            self._button.config(bg="red")
        self._game.hovered_tile = self

    def reset_highlights(self):
        if self._game.over:
            return
        for tile in self._game.find_adjacent_tiles(self):
            if tile.marker_color is None:
                tile._button.config(bg="Gray")
        if self.marker_color is None:
            self._button.config(bg="Gray")

    def reset(self):
        self._flagged = False
        self._revealed = False
        self._mine = False
        self.marker_color = None
        self._button.config(image=self._game._images["field"], text="", bg="Gray")


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
