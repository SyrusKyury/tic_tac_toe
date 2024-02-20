# Tic Tac Toe
A simple tic-tac-toe game coded in Python which implements a simple AI you can play against.

## How to play
Run the command:
`python3 tic_tac_toe.py`

## Heuristic
The file `ai.py` generates training data, associating every possible game state with a certain score. Scores can be:
- **0** if it's a tie
- **1** if X wins
- **-1** if O wins
- **>0** if X has a higher chance of winning in that game state
- **<0** if O has a higher chance of winning in that game state

If the CPU plays as X, it will choose the move with the highest score; conversely, if the CPU plays as O. The CPU avoids moves that could lead the opponent to win.
Training data is then used to feed `tic_tac_toe.py`.
