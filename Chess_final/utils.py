# utils.py
# Utility functions: check detection, legal move filtering, checkmate/draw detection.
# All functions receive board state explicitly — no globals used.

from config import BOARD_SIZE
from pieces import check_options

MAX_INDEX = BOARD_SIZE - 1


# ---------------------------------------------------------------------------
# Sliding attack helper
# ---------------------------------------------------------------------------

def _sliding_attacks(pos, directions, friends, enemies):
    """
    Return all squares reachable by a sliding piece from pos in the given
    directions, stopping at the first occupied square (inclusive).
    """
    attacks = []
    for dx, dy in directions:
        chain = 1
        while True:
            nx, ny = pos[0] + chain * dx, pos[1] + chain * dy
            if not (0 <= nx <= MAX_INDEX and 0 <= ny <= MAX_INDEX):
                break
            target = (nx, ny)
            attacks.append(target)
            if target in friends or target in enemies:
                break
            chain += 1
    return attacks


# ---------------------------------------------------------------------------
# Check detection
# ---------------------------------------------------------------------------

def is_in_check(color, w_pieces, w_locations, b_pieces, b_locations):
    """
    Return True if the king of `color` is currently under attack.
    Operates entirely on the passed-in board state.
    """
    if color == 'white':
        if 'king' not in w_pieces:
            return False
        king_pos = w_locations[w_pieces.index('king')]
        for i in range(len(b_pieces)):
            piece = b_pieces[i]
            pos   = b_locations[i]
            if piece == 'pawn':
                # Black pawns attack diagonally downward (y increases)
                attacks = [(pos[0] + 1, pos[1] + 1), (pos[0] - 1, pos[1] + 1)]
            elif piece == 'knight':
                attacks = [(pos[0] + a, pos[1] + b) for a, b in
                           [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]]
            elif piece == 'king':
                attacks = [(pos[0] + a, pos[1] + b) for a, b in
                           [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
            elif piece == 'rook':
                attacks = _sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0)],
                                           w_locations, b_locations)
            elif piece == 'bishop':
                attacks = _sliding_attacks(pos, [(1,1),(1,-1),(-1,1),(-1,-1)],
                                           w_locations, b_locations)
            elif piece == 'queen':
                attacks = _sliding_attacks(
                    pos, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)],
                    w_locations, b_locations)
            else:
                attacks = []
            if king_pos in attacks:
                return True
        return False

    else:  # color == 'black'
        if 'king' not in b_pieces:
            return False
        king_pos = b_locations[b_pieces.index('king')]
        for i in range(len(w_pieces)):
            piece = w_pieces[i]
            pos   = w_locations[i]
            if piece == 'pawn':
                # White pawns attack diagonally upward (y decreases)
                attacks = [(pos[0] + 1, pos[1] - 1), (pos[0] - 1, pos[1] - 1)]
            elif piece == 'knight':
                attacks = [(pos[0] + a, pos[1] + b) for a, b in
                           [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]]
            elif piece == 'king':
                attacks = [(pos[0] + a, pos[1] + b) for a, b in
                           [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
            elif piece == 'rook':
                attacks = _sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0)],
                                           b_locations, w_locations)
            elif piece == 'bishop':
                attacks = _sliding_attacks(pos, [(1,1),(1,-1),(-1,1),(-1,-1)],
                                           b_locations, w_locations)
            elif piece == 'queen':
                attacks = _sliding_attacks(
                    pos, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)],
                    b_locations, w_locations)
            else:
                attacks = []
            if king_pos in attacks:
                return True
        return False


# ---------------------------------------------------------------------------
# Legal move filtering
# ---------------------------------------------------------------------------

def filter_legal_moves(piece_index, color, moves, w_pieces, w_locations, b_pieces, b_locations):
    """
    From a list of candidate moves for one piece, keep only those that do
    not leave the moving side's own king in check.
    Works with explicit board state so it can be used both in-game and by the AI.
    """
    legal = []
    for move in moves:
        new_w_pieces = w_pieces[:]
        new_w_locs   = w_locations[:]
        new_b_pieces = b_pieces[:]
        new_b_locs   = b_locations[:]

        if color == 'white':
            new_w_locs[piece_index] = move
            if move in new_b_locs:
                idx = new_b_locs.index(move)
                new_b_locs.pop(idx)
                new_b_pieces.pop(idx)
        else:
            new_b_locs[piece_index] = move
            if move in new_w_locs:
                idx = new_w_locs.index(move)
                new_w_locs.pop(idx)
                new_w_pieces.pop(idx)

        if not is_in_check(color, new_w_pieces, new_w_locs, new_b_pieces, new_b_locs):
            legal.append(move)
    return legal


# ---------------------------------------------------------------------------
# Checkmate / stalemate detection
# ---------------------------------------------------------------------------

def is_checkmate(color, w_pieces, w_locations, b_pieces, b_locations):
    """
    Return True if the given color has no legal moves (checkmate or stalemate).
    The caller must separately call is_in_check to distinguish the two cases.
    """
    if color == 'white':
        pieces, locations = w_pieces, w_locations
    else:
        pieces, locations = b_pieces, b_locations

    all_moves = check_options(pieces, locations, color, w_locations, b_locations)
    for i in range(len(pieces)):
        legal = filter_legal_moves(i, color, all_moves[i],
                                   w_pieces, w_locations, b_pieces, b_locations)
        if legal:
            return False  # at least one legal move — not checkmate/stalemate
    return True


# ---------------------------------------------------------------------------
# Draw conditions
# ---------------------------------------------------------------------------

def check_insufficient_material(w_pieces, b_pieces):
    """
    Return True if neither side has enough material to deliver checkmate.
    Covers: K vs K, K+B vs K, K+N vs K.
    """
    all_pieces = w_pieces + b_pieces
    if len(all_pieces) == 2:
        return True
    if len(all_pieces) == 3 and ('bishop' in all_pieces or 'knight' in all_pieces):
        return True
    return False


def check_threefold(board_history, w_locations, b_locations, turn_step):
    """
    Return True if the current board position has occurred 3 or more times.
    A position is identified by (white_locations, black_locations, turn_step).
    """
    current_state = (tuple(w_locations), tuple(b_locations), turn_step)
    return board_history.count(current_state) >= 3


# ---------------------------------------------------------------------------
# In-game valid move helper (uses current turn state)
# ---------------------------------------------------------------------------

def get_valid_moves(selection, turn_step, white_options, black_options,
                    w_pieces, w_locations, b_pieces, b_locations):
    """
    Return the filtered legal moves for the currently selected piece,
    based on whose turn it is.
    """
    if turn_step < 2:
        raw_moves = white_options[selection]
        color = 'white'
    else:
        raw_moves = black_options[selection]
        color = 'black'
    return filter_legal_moves(selection, color, raw_moves,
                              w_pieces, w_locations, b_pieces, b_locations)
