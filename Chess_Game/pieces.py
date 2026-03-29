# pieces.py
# Movement rules for all chess pieces.
# All functions are pure: they take board state as parameters and return move lists.

from config import BOARD_SIZE

MAX_INDEX = BOARD_SIZE - 1  # 4 for a 5x5 board


def check_options(pieces, locations, color, white_locations, black_locations):
    """Return a list of move lists for every piece of the given color."""
    all_moves = []
    for i in range(len(pieces)):
        piece = pieces[i]
        location = locations[i]
        if piece == 'pawn':
            moves = check_pawn(location, color, white_locations, black_locations)
        elif piece == 'rook':
            moves = check_rook(location, color, white_locations, black_locations)
        elif piece == 'knight':
            moves = check_knight(location, color, white_locations, black_locations)
        elif piece == 'bishop':
            moves = check_bishop(location, color, white_locations, black_locations)
        elif piece == 'queen':
            moves = check_queen(location, color, white_locations, black_locations)
        elif piece == 'king':
            moves = check_king(location, color, white_locations, black_locations)
        else:
            moves = []
        all_moves.append(moves)
    return all_moves


def check_pawn(position, color, white_locations, black_locations):
    """
    Pawn movement:
      - White moves upward (decreasing y).
      - Black moves downward (increasing y).
      - Captures diagonally forward.
    """
    moves = []
    x, y = position

    if color == 'white':
        # One square forward (up)
        if (x, y - 1) not in white_locations and (x, y - 1) not in black_locations and y > 0:
            moves.append((x, y - 1))
        # Diagonal captures
        if (x + 1, y - 1) in black_locations:
            moves.append((x + 1, y - 1))
        if (x - 1, y - 1) in black_locations:
            moves.append((x - 1, y - 1))
    else:
        # One square forward (down)
        if (x, y + 1) not in white_locations and (x, y + 1) not in black_locations and y < MAX_INDEX:
            moves.append((x, y + 1))
        # Diagonal captures
        if (x + 1, y + 1) in white_locations:
            moves.append((x + 1, y + 1))
        if (x - 1, y + 1) in white_locations:
            moves.append((x - 1, y + 1))

    return moves


def check_king(position, color, white_locations, black_locations):
    """King moves one square in any of the 8 directions."""
    friends = white_locations if color == 'white' else black_locations
    moves = []
    x, y = position
    for dx, dy in [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]:
        target = (x + dx, y + dy)
        if target not in friends and 0 <= target[0] <= MAX_INDEX and 0 <= target[1] <= MAX_INDEX:
            moves.append(target)
    return moves


def check_queen(position, color, white_locations, black_locations):
    """Queen combines rook and bishop movement."""
    return (
        check_bishop(position, color, white_locations, black_locations) +
        check_rook(position, color, white_locations, black_locations)
    )


def check_bishop(position, color, white_locations, black_locations):
    """Bishop slides diagonally until blocked."""
    friends = white_locations if color == 'white' else black_locations
    enemies = black_locations if color == 'white' else white_locations
    moves = []
    for dx, dy in [(1, -1), (-1, -1), (1, 1), (-1, 1)]:
        moves.extend(_sliding_moves(position, dx, dy, friends, enemies))
    return moves


def check_rook(position, color, white_locations, black_locations):
    """Rook slides horizontally and vertically until blocked."""
    friends = white_locations if color == 'white' else black_locations
    enemies = black_locations if color == 'white' else white_locations
    moves = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        moves.extend(_sliding_moves(position, dx, dy, friends, enemies))
    return moves


def check_knight(position, color, white_locations, black_locations):
    """Knight jumps in an L-shape; cannot be blocked."""
    friends = white_locations if color == 'white' else black_locations
    moves = []
    x, y = position
    for dx, dy in [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]:
        target = (x + dx, y + dy)
        if target not in friends and 0 <= target[0] <= MAX_INDEX and 0 <= target[1] <= MAX_INDEX:
            moves.append(target)
    return moves


def _sliding_moves(position, dx, dy, friends, enemies):
    """
    Helper: generate all squares a sliding piece can reach in direction (dx, dy).
    Stops when hitting a friendly piece (excluded) or an enemy piece (included).
    """
    moves = []
    chain = 1
    while True:
        target = (position[0] + chain * dx, position[1] + chain * dy)
        if not (0 <= target[0] <= MAX_INDEX and 0 <= target[1] <= MAX_INDEX):
            break
        if target in friends:
            break
        moves.append(target)
        if target in enemies:
            break
        chain += 1
    return moves
