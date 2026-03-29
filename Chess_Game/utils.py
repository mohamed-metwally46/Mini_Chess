# utils.py
# Utility functions: check detection, legal move filtering, and checkmate detection.
# All functions receive board state explicitly — no globals used.

from config import BOARD_SIZE
from pieces import check_options

MAX_INDEX = BOARD_SIZE - 1


# ---------------------------------------------------------------------------
# Attack helpers
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


def _piece_attacks(piece, pos, attacker_friends, attacker_enemies):
    """
    Return all squares attacked by a single piece.
    attacker_friends / attacker_enemies are from the attacker's perspective.
    """
    x, y = pos
    if piece == 'pawn':
        # Determine attack direction from which side the attacker is on.
        # If the attacker's friends are white_locations the pawn faces up (dy=-1),
        # but is_in_check always passes the enemy's own friend/enemy lists, so:
        #   - When checking white's king, the attackers are black pieces whose
        #     friends = black_locations → pawn attacks downward (dy=+1).
        #   - When checking black's king, the attackers are white pieces whose
        #     friends = white_locations → pawn attacks upward (dy=-1).
        # We differentiate by a convention tag passed in via the wrapper below.
        # This function therefore should NOT be called directly — use is_in_check.
        return []  # handled inline in is_in_check for clarity
    elif piece == 'knight':
        return [
            (x + dx, y + dy)
            for dx, dy in [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
        ]
    elif piece == 'king':
        return [
            (x + dx, y + dy)
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        ]
    elif piece == 'rook':
        return _sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0)], attacker_friends, attacker_enemies)
    elif piece == 'bishop':
        return _sliding_attacks(pos, [(1,1),(1,-1),(-1,1),(-1,-1)], attacker_friends, attacker_enemies)
    elif piece == 'queen':
        return _sliding_attacks(
            pos,
            [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)],
            attacker_friends, attacker_enemies
        )
    return []


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
        # Examine every black piece as an attacker
        for i in range(len(b_pieces)):
            piece = b_pieces[i]
            pos = b_locations[i]
            if piece == 'pawn':
                # Black pawns attack diagonally downward (increasing y)
                attacks = [(pos[0] + 1, pos[1] + 1), (pos[0] - 1, pos[1] + 1)]
            else:
                attacks = _piece_attacks(piece, pos, b_locations, w_locations)
            if king_pos in attacks:
                return True
        return False

    else:  # color == 'black'
        if 'king' not in b_pieces:
            return False
        king_pos = b_locations[b_pieces.index('king')]
        # Examine every white piece as an attacker
        for i in range(len(w_pieces)):
            piece = w_pieces[i]
            pos = w_locations[i]
            if piece == 'pawn':
                # White pawns attack diagonally upward (decreasing y)
                attacks = [(pos[0] + 1, pos[1] - 1), (pos[0] - 1, pos[1] - 1)]
            else:
                attacks = _piece_attacks(piece, pos, w_locations, b_locations)
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
        new_w_locs = w_locations[:]
        new_b_pieces = b_pieces[:]
        new_b_locs = b_locations[:]

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
# Checkmate detection
# ---------------------------------------------------------------------------

def is_checkmate(color, w_pieces, w_locations, b_pieces, b_locations):
    """
    Return True if the given color has no legal moves (checkmate or stalemate).
    """
    if color == 'white':
        pieces, locations = w_pieces, w_locations
    else:
        pieces, locations = b_pieces, b_locations

    all_moves = check_options(pieces, locations, color, w_locations, b_locations)
    for i in range(len(pieces)):
        legal = filter_legal_moves(i, color, all_moves[i], w_pieces, w_locations, b_pieces, b_locations)
        if legal:
            return False  # at least one legal move exists
    return True


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
    return filter_legal_moves(selection, color, raw_moves, w_pieces, w_locations, b_pieces, b_locations)
