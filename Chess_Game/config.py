# config.py
# All game-wide constants and configuration values

# --- Screen ---
WIDTH = 700
HEIGHT = 600
FPS = 60

# --- Board ---
BOARD_SIZE = 5        # 5x5 board
CELL_SIZE = 100       # pixels per square

# --- Turn step values ---
# 0 = white's turn, no selection
# 1 = white's turn, piece selected
# 2 = black's turn, no selection
# 3 = black's turn, piece selected

# --- Initial piece layouts ---
WHITE_PIECES_INIT = [
    'rook', 'knight', 'queen', 'king', 'bishop',
    'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
]
WHITE_LOCATIONS_INIT = [
    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)
]
BLACK_PIECES_INIT = [
    'rook', 'knight', 'queen', 'king', 'bishop',
    'pawn', 'pawn', 'pawn', 'pawn', 'pawn'
]
BLACK_LOCATIONS_INIT = [
    (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1)
]

# --- Piece ordering used for image index lookups ---
PIECE_LIST = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# --- AI piece values ---
PIECE_VALUES = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 1000
}

# --- AI search depth ---
AI_DEPTH = 3
