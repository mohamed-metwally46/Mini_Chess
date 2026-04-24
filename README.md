# ♟️ 5x5 Mini Chess (Pygame)

A compact chess variant played on a **5×5 board** with randomised back rows, an optional AI opponent, and standard chess rules adapted for the smaller grid.

---

## Features

- **3 game modes** — Player vs Player, Player vs AI (you play White), AI vs Player (you play Black)
- **Randomised back rows** — each game shuffles the king, queen, rook, bishop, and knight into a new order
- **AI opponent** — minimax search with alpha-beta pruning (depth 3)
- **Full legality enforcement** — check detection, legal-move filtering, pawn promotion
- **Draw detection** — insufficient material, threefold repetition, stalemate
- **Captured-piece panel** — displays taken pieces on the right side of the board
- **Check animation** — the king's square flashes when it is in check
- **Forfeit button** — either player can concede mid-game

---

## Project Structure

```
.
├── main.py       # Entry point: Pygame loop, event handling, game state
├── board.py      # All rendering functions (board, pieces, UI overlays)
├── pieces.py     # Movement rules for every piece type
├── utils.py      # Check / checkmate / draw detection, legal-move filtering
├── ai.py         # Minimax + alpha-beta pruning, AI move selection
├── config.py     # Constants: board size, colors, piece values, AI depth
└── img/          # Piece images (wp.png, bp.png, wQ.png, bQ.png, …)
```

---

## Requirements

- Python 3.8+
- [Pygame](https://www.pygame.org/) 2.x

Install dependencies:

```bash
pip install pygame
```

---

## Running the Game

```bash
python main.py
```

---

## How to Play

1. **Select a mode** on the opening screen.
2. **Click a piece** to select it — valid destination squares are highlighted with dots.
3. **Click a highlighted square** to move.
4. **Pawn promotion** happens automatically (promoted to queen).
5. Press **Enter** after the game ends to start a new game.
6. Click **FORFEIT** to concede at any time.

---

## Board & Rules

| Detail | Value |
|---|---|
| Board size | 5 × 5 |
| Starting rows | Back row (randomised) + 5 pawns |
| Pawn promotion | Reaches the far rank → becomes queen |
| Win condition | Capture the enemy king (or opponent forfeits) |
| Draw conditions | Insufficient material · Threefold repetition · Stalemate |

White occupies rows 3–4 (bottom); Black occupies rows 0–1 (top).

---

## AI Details

| Setting | Value |
|---|---|
| Algorithm | Minimax with alpha-beta pruning |
| Search depth | 3 half-moves |
| Evaluation | Material count (pawn=1, knight/bishop=3, rook=5, queen=9, king=1000) |

The AI waits ~1 second before playing its move so the transition feels natural.

---

## Configuration (`config.py`)

| Constant | Default | Description |
|---|---|---|
| `BOARD_SIZE` | `5` | Board dimensions (n × n) |
| `CELL_SIZE` | `100` | Pixels per square |
| `AI_DEPTH` | `3` | Minimax search depth |
| `PIECE_VALUES` | see file | Material values used by the evaluator |

---

## License

MIT — free to use, modify, and distribute.
