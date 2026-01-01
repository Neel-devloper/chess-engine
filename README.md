# Chess Engine V1

A simple chess game with an AI opponent built using Python, Pygame, and the `chess` library.

## Features

- Play chess against an AI opponent
- Graphical user interface with customizable themes (10 themes available)
- Highlight legal moves
- Timer for each player
- AI uses minimax algorithm with alpha-beta pruning
- Adjustable AI difficulty by changing search depth

## Requirements

- Python 3.x
- Pygame
- python-chess library

## Installation

1. Clone or download the repository.
2. Install the required dependencies:

   ```bash
   pip install pygame python-chess
   ```

3. Ensure the chess piece images are in the same directory as `main.py`. The images should be named as follows:
   - `white pawn.png`
   - `white rook.png`
   - `white knight.png`
   - `white bishop.png`
   - `white queen.png`
   - `white king.png`
   - `black pawn.png`
   - `black rook.png`
   - `black knight.png`
   - `black bishop.png`
   - `black queen.png`
   - `black king.png`

## Usage

Run the game by executing:

```bash
python Chess\ engine/main.py
```

### Controls

- Click on a piece to select it, then click on a destination square to move.
- Press keys 0-9 to change the board theme.
- Close the window to quit.

### AI Configuration

The AI's intelligence can be adjusted by modifying the `DEPTH` variable in `chess_engine.py`. Higher depth means stronger AI but slower moves.

## Project Structure

- `Chess engine/chess_engine.py`: Contains the AI logic using minimax with alpha-beta pruning.
- `Chess engine/main.py`: Handles the game loop, UI, and user input.
- `Chess engine/README.md`: Additional documentation.

## License

This project is open-source. Feel free to use and modify it.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
