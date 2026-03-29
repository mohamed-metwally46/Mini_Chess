# ai.py
# AI logic: board evaluation and minimax with alpha-beta pruning.
# Operates entirely on passed-in board state — no globals.

from config import PIECE_VALUES, AI_DEPTH
from pieces import check_options
from utils import filter_legal_moves


def evaluate_board(w_pieces, b_pieces):
    """
    Static board evaluation.
    Positive score = good for white; negative score = good for black.
    """
    score = 0
    for piece in w_pieces:
        score += PIECE_VALUES[piece]
    for piece in b_pieces:
        score -= PIECE_VALUES[piece]
    return score


def minimax(depth, alpha, beta, maximizing, w_pieces, w_locations, b_pieces, b_locations):
    """
    Minimax with alpha-beta pruning.

    Returns: (score, best_piece_index, best_move_coords)
    """
    if depth == 0:
        return evaluate_board(w_pieces, b_pieces), None, None

    if maximizing:
        return _maximize(depth, alpha, beta, w_pieces, w_locations, b_pieces, b_locations)
    else:
        return _minimize(depth, alpha, beta, w_pieces, w_locations, b_pieces, b_locations)


def _maximize(depth, alpha, beta, w_pieces, w_locations, b_pieces, b_locations):
    """White tries to maximise the score."""
    max_score = -999999
    best_piece = None
    best_move = None

    all_moves = check_options(w_pieces, w_locations, 'white', w_locations, b_locations)
    for i in range(len(w_pieces)):
        legal = filter_legal_moves(i, 'white', all_moves[i], w_pieces, w_locations, b_pieces, b_locations)
        for move in legal:
            new_w_pieces = w_pieces[:]
            new_w_locs = w_locations[:]
            new_b_pieces = b_pieces[:]
            new_b_locs = b_locations[:]

            new_w_locs[i] = move
            if move in new_b_locs:
                idx = new_b_locs.index(move)
                new_b_locs.pop(idx)
                new_b_pieces.pop(idx)

            score, _, _ = minimax(depth - 1, alpha, beta, False,
                                  new_w_pieces, new_w_locs, new_b_pieces, new_b_locs)
            if score > max_score:
                max_score = score
                best_piece = i
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break

    return max_score, best_piece, best_move


def _minimize(depth, alpha, beta, w_pieces, w_locations, b_pieces, b_locations):
    """Black tries to minimise the score."""
    min_score = 999999
    best_piece = None
    best_move = None

    all_moves = check_options(b_pieces, b_locations, 'black', w_locations, b_locations)
    for i in range(len(b_pieces)):
        legal = filter_legal_moves(i, 'black', all_moves[i], w_pieces, w_locations, b_pieces, b_locations)
        for move in legal:
            new_w_pieces = w_pieces[:]
            new_w_locs = w_locations[:]
            new_b_pieces = b_pieces[:]
            new_b_locs = b_locations[:]

            new_b_locs[i] = move
            if move in new_w_locs:
                idx = new_w_locs.index(move)
                new_w_locs.pop(idx)
                new_w_pieces.pop(idx)

            score, _, _ = minimax(depth - 1, alpha, beta, True,
                                  new_w_pieces, new_w_locs, new_b_pieces, new_b_locs)
            if score < min_score:
                min_score = score
                best_piece = i
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break

    return min_score, best_piece, best_move


def get_ai_move(maximizing, w_pieces, w_locations, b_pieces, b_locations):
    """
    Convenience wrapper: run minimax at the configured depth and return
    (best_piece_index, best_move_coords).  Returns (None, None) if no move found.
    """
    _, best_piece, best_move = minimax(
        AI_DEPTH, -999999, 999999, maximizing,
        w_pieces, w_locations, b_pieces, b_locations
    )
    return best_piece, best_move
