# 3D-Minesweeper

A 3D version of the classic Minesweeper game. The game is implemented in Python.

## How to play

The game is played on a 3D grid. The player can click on a cell to reveal it. If the cell contains a mine, the game is over. If the cell does not contain a mine, the number of adjacent cells containing mines is revealed. The player can also flag a cell if they think it contains a mine. The game is won when all non-mine cells are revealed.

### Controls

#### Mouse
- Left click: Reveal cell
- Right click: Flag cell
- Middle click: Reveal all adjacent cells

#### Keyboard
- `R`: Restart game (WIP!)
- `Q`: Quit game (WIP!)
- `0-9`: Set color markers
- `Backspace`: Clear color markers

## How to install

### Requirements
- Python 3.9 or later
- Pip

## How to run
- Clone the repository `git clone https://github.com/Verkleckert/3d-minesweeper.git`
- Run `pip install -r requirements.txt`
- Run `python main.py`
- Enjoy!