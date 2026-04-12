
# two player chess in python with Pygame!
# part one, set up variables images and game loop
import pygame
pygame.init()

WIDTH = 700
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption('Two-Player Pygame Chess!')

font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 24)
big_font = pygame.font.Font('freesansbold.ttf', 24)
timer = pygame.time.Clock()
fps = 60
# game variables and images
# ✏️ CHANGED: 5x5 board - reduced pieces, no second pawn row
white_pieces = ['rook', 'knight', 'queen', 'king', 'bishop',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
                (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]
black_pieces = ['rook', 'knight', 'queen', 'king', 'bishop',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]

captured_pieces_white = []
captured_pieces_black = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('img/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('img/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('img/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('img/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('img/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('img/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('img/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('img/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('img/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('img/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('img/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('img/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                    white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                    black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False
game_mode = 0                  # ✏️ NEW
game_mode_selected = False     # ✏️ NEW
# draw main game board
def draw_mode_selection():
    screen.fill('dark gray')
    screen.blit(big_font.render('Select Game Mode', True, 'white'), (150, 100))

    # PvP button
    pygame.draw.rect(screen, 'gray', [150, 200, 400, 60])
    pygame.draw.rect(screen, 'gold', [150, 200, 400, 60], 3)
    screen.blit(medium_font.render('Player vs Player', True, 'white'), (200, 215))

    # Player vs AI button
    pygame.draw.rect(screen, 'gray', [150, 300, 400, 60])
    pygame.draw.rect(screen, 'gold', [150, 300, 400, 60], 3)
    screen.blit(medium_font.render('You(White) vs AI(Black)', True, 'white'), (155, 315))

    # AI vs Player button
    pygame.draw.rect(screen, 'gray', [150, 400, 400, 60])
    pygame.draw.rect(screen, 'gold', [150, 400, 400, 60], 3)
    screen.blit(medium_font.render('AI(White) vs You(Black)', True, 'white'), (155, 415))

    pygame.display.flip()
def draw_board():
    for row in range(5):                                      # ✏️ CHANGED: proper 5x5 checkerboard
        for col in range(5):
            if (row + col) % 2 == 1:
                pygame.draw.rect(screen, 'light gray', [col * 100, row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 500, WIDTH, 100])       # ✏️ CHANGED: 800 -> 500
        pygame.draw.rect(screen, 'gold', [0, 500, WIDTH, 100], 5)    # ✏️ CHANGED: 800 -> 500
        pygame.draw.rect(screen, 'gold', [500, 0, 200, HEIGHT], 5)   # ✏️ CHANGED: 800 -> 500
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                    'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 520))  # ✏️ CHANGED: 820 -> 520
        for i in range(6):                                                        # ✏️ CHANGED: 9 -> 6
            pygame.draw.line(screen, 'black', (0, 100 * i), (500, 100 * i), 2)   # ✏️ CHANGED: 800 -> 500
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 500), 2)   # ✏️ CHANGED: 800 -> 500
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (510, 530))     # ✏️ CHANGED: 810,830 -> 510,530
# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                100, 100], 2)
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                100, 100], 2)
# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list
# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 4 and 0 <= target[1] <= 4:  # ✏️ CHANGED: 7 -> 4 for 5x5 board
            moves_list.append(target)
    return moves_list
# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list
# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 4 and 0 <= position[1] + (chain * y) <= 4:  # ✏️ CHANGED: 7 -> 4 for 5x5 board
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list
# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 4 and 0 <= position[1] + (chain * y) <= 4:  # ✏️ CHANGED: 7 -> 4 for 5x5 board
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list
# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:  # white moves up (decreasing y)
            moves_list.append((position[0], position[1] - 1))
        # ✏️ REMOVED: double move — no room on 5x5 board
        if (position[0] + 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    else:
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 4:  # black moves down (increasing y)
            moves_list.append((position[0], position[1] + 1))
        # ✏️ REMOVED: double move — no room on 5x5 board
        if (position[0] + 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    return moves_list
# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 4 and 0 <= target[1] <= 4:  # ✏️ CHANGED: 7 -> 4 for 5x5 board
            moves_list.append(target)
    return moves_list
# ✏️ NEW: piece values for AI evaluation
PIECE_VALUES = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 1000
}

def evaluate_board():
    score = 0
    for piece in white_pieces:
        score += PIECE_VALUES[piece]
    for piece in black_pieces:
        score -= PIECE_VALUES[piece]
    return score  # positive = good for white, negative = good for black
def filter_legal_moves_sim(piece_index, color, moves, w_pieces, w_locations, b_pieces, b_locations):
    legal = []
    for move in moves:
        if color == 'white':
            new_w_locs = w_locations[:]
            new_w_pieces = w_pieces[:]
            new_b_locs = b_locations[:]
            new_b_pieces = b_pieces[:]
            new_w_locs[piece_index] = move
            if move in new_b_locs:
                idx = new_b_locs.index(move)
                new_b_locs.pop(idx)
                new_b_pieces.pop(idx)
        else:
            new_w_locs = w_locations[:]
            new_w_pieces = w_pieces[:]
            new_b_locs = b_locations[:]
            new_b_pieces = b_pieces[:]
            new_b_locs[piece_index] = move
            if move in new_w_locs:
                idx = new_w_locs.index(move)
                new_w_locs.pop(idx)
                new_w_pieces.pop(idx)
        if not is_in_check(color, new_w_pieces, new_w_locs, new_b_pieces, new_b_locs):
            legal.append(move)
    return legal
def minimax(depth, alpha, beta, maximizing, w_pieces, w_locations, b_pieces, b_locations):
    if depth == 0:
        # evaluate from passed-in state
        score = 0
        for piece in w_pieces:
            score += PIECE_VALUES[piece]
        for piece in b_pieces:
            score -= PIECE_VALUES[piece]
        return score, None, None

    if maximizing:  # white's turn
        max_score = -999999
        best_piece = None
        best_move = None
        all_moves = check_options(w_pieces, w_locations, 'white')
        for i in range(len(w_pieces)):
            legal = filter_legal_moves_sim(i, 'white', all_moves[i], w_pieces, w_locations, b_pieces, b_locations)
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
                score, _, _ = minimax(depth - 1, alpha, beta, False, new_w_pieces, new_w_locs, new_b_pieces, new_b_locs)
                if score > max_score:
                    max_score = score
                    best_piece = i
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return max_score, best_piece, best_move

    else:  # black's turn
        min_score = 999999
        best_piece = None
        best_move = None
        all_moves = check_options(b_pieces, b_locations, 'black')
        for i in range(len(b_pieces)):
            legal = filter_legal_moves_sim(i, 'black', all_moves[i], w_pieces, w_locations, b_pieces, b_locations)
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
                score, _, _ = minimax(depth - 1, alpha, beta, True, new_w_pieces, new_w_locs, new_b_pieces, new_b_locs)
                if score < min_score:
                    min_score = score
                    best_piece = i
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return min_score, best_piece, best_move
def _sliding_attacks(pos, directions, friends, enemies):  # ✏️ NEW helper
    attacks = []
    for dx, dy in directions:
        chain = 1
        while True:
            nx, ny = pos[0] + chain * dx, pos[1] + chain * dy
            if not (0 <= nx <= 4 and 0 <= ny <= 4):
                break
            target = (nx, ny)
            attacks.append(target)
            if target in friends or target in enemies:
                break
            chain += 1
    return attacks
def is_in_check(color, w_pieces, w_locations, b_pieces, b_locations):
    if color == 'white':
        if 'king' not in w_pieces:
            return False
        king_pos = w_locations[w_pieces.index('king')]
        # ✏️ FIX: manually compute enemy moves using passed-in lists, not globals
        for i in range(len(b_pieces)):
            piece = b_pieces[i]
            pos = b_locations[i]
            if piece == 'pawn':
                # black pawn attacks diagonally downward (increasing y)
                attacks = [(pos[0] + 1, pos[1] + 1), (pos[0] - 1, pos[1] + 1)]
            elif piece == 'knight':
                attacks = [(pos[0]+a, pos[1]+b) for a, b in
                        [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]]
            elif piece == 'king':
                attacks = [(pos[0]+a, pos[1]+b) for a, b in
                        [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
            elif piece == 'rook':
                attacks = _sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0)], w_locations, b_locations)
            elif piece == 'bishop':
                attacks = _sliding_attacks(pos, [(1,1),(1,-1),(-1,1),(-1,-1)], w_locations, b_locations)
            elif piece == 'queen':
                attacks = _sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)], w_locations, b_locations)
            else:
                attacks = []
            if king_pos in attacks:
                return True
        return False
    else:
        if 'king' not in b_pieces:
            return False
        king_pos = b_locations[b_pieces.index('king')]
        for i in range(len(w_pieces)):
            piece = w_pieces[i]
            pos = w_locations[i]
            if piece == 'pawn':
                # white pawn attacks diagonally upward (decreasing y)
                attacks = [(pos[0] + 1, pos[1] - 1), (pos[0] - 1, pos[1] - 1)]
            elif piece == 'knight':
                attacks = [(pos[0]+a, pos[1]+b) for a, b in
                        [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]]
            elif piece == 'king':
                attacks = [(pos[0]+a, pos[1]+b) for a, b in
                        [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
            elif piece == 'rook':
                attacks = _sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0)], b_locations, w_locations)
            elif piece == 'bishop':
                attacks = _sliding_attacks(pos, [(1,1),(1,-1),(-1,1),(-1,-1)], b_locations, w_locations)
            elif piece == 'queen':
                attacks = _sliding_attacks(pos, [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)], b_locations, w_locations)
            else:
                attacks = []
            if king_pos in attacks:
                return True
        return False

def filter_legal_moves(piece_index, color, moves):
    legal = []
    for move in moves:
        if color == 'white':
            new_w_locs = white_locations[:]
            new_w_pieces = white_pieces[:]
            new_b_locs = black_locations[:]
            new_b_pieces = black_pieces[:]
            new_w_locs[piece_index] = move
            if move in new_b_locs:
                idx = new_b_locs.index(move)
                new_b_locs.pop(idx)
                new_b_pieces.pop(idx)
        else:
            new_w_locs = white_locations[:]
            new_w_pieces = white_pieces[:]
            new_b_locs = black_locations[:]
            new_b_pieces = black_pieces[:]
            new_b_locs[piece_index] = move
            if move in new_w_locs:
                idx = new_w_locs.index(move)
                new_w_locs.pop(idx)
                new_w_pieces.pop(idx)
        if not is_in_check(color, new_w_pieces, new_w_locs, new_b_pieces, new_b_locs):
            legal.append(move)
    return legal

def is_checkmate(color):  # ✏️ NEW: check if the current player has no legal moves
    if color == 'white':
        pieces = white_pieces
        locations = white_locations
    else:
        pieces = black_pieces
        locations = black_locations
    for i in range(len(pieces)):
        if color == 'white':
            raw_moves = check_options(white_pieces, white_locations, 'white')[i]
        else:
            raw_moves = check_options(black_pieces, black_locations, 'black')[i]
        if filter_legal_moves(i, color, raw_moves):
            return False  # found at least one legal move, not checkmate
    return True  # no legal moves at all = checkmate

def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
        color = 'white'
    else:
        options_list = black_options
        color = 'black'
    valid_options = options_list[selection]
    return filter_legal_moves(selection, color, valid_options)
# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (510, 5 + 45 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (610, 5 + 45 * i))
# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if is_in_check('white', white_pieces, white_locations, black_pieces, black_locations):
            if 'king' in white_pieces:
                king_index = white_pieces.index('king')
                if counter < 15:
                    pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                          white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if is_in_check('black', white_pieces, white_locations, black_pieces, black_locations):
            if 'king' in black_pieces:
                king_index = black_pieces.index('king')
                if counter < 15:
                    pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                           black_locations[king_index][1] * 100 + 1, 100, 100], 5)
def draw_game_over():
    pygame.draw.rect(screen, 'black', [50, 200, 400, 70])        # ✏️ CHANGED
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (60, 210))   # ✏️ CHANGED
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (60, 240))  # ✏️ CHANGED
# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)

    # ✏️ NEW: show mode selection screen first
    if not game_mode_selected:
        draw_mode_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if 150 <= x <= 550:
                    if 200 <= y <= 260:
                        game_mode = 0
                        game_mode_selected = True
                    elif 300 <= y <= 360:
                        game_mode = 1
                        game_mode_selected = True
                    elif 400 <= y <= 460:
                        game_mode = 2
                        game_mode_selected = True
        continue  # skip the rest of the loop until mode is selected

    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (5, 5) or click_coords == (6, 5):  # ✏️ CHANGED: forfeit button coords 8,8 -> 5,5
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
                    if is_checkmate('black'):  # ✏️ NEW
                        winner = 'white'
            if turn_step > 1:
                if click_coords == (5, 5) or click_coords == (6, 5):  # ✏️ CHANGED: forfeit button coords 8,8 -> 5,5
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    if is_checkmate('white'):  # ✏️ NEW
                        winner = 'black'
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'queen', 'king', 'bishop',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn']          # ✏️ CHANGED: 5x5 pieces
                white_locations = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
                                (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]      # ✏️ CHANGED: white at bottom
                black_pieces = ['rook', 'knight', 'queen', 'king', 'bishop',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn']          # ✏️ CHANGED: 5x5 pieces
                black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1)]      # ✏️ CHANGED: black at top
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                game_mode_selected = False  # ✏️ NEW
                game_mode = 0 
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                # ✏️ NEW: AI move execution
    if not game_over and game_mode_selected:
        # AI plays black
        if game_mode == 1 and turn_step == 2:
            _, best_piece, best_move = minimax(3, -999999, 999999, False,
                                            white_pieces, white_locations,
                                            black_pieces, black_locations)
            if best_piece is not None and best_move is not None:
                black_locations[best_piece] = best_move
                if best_move in white_locations:
                    idx = white_locations.index(best_move)
                    captured_pieces_black.append(white_pieces[idx])
                    if white_pieces[idx] == 'king':
                        winner = 'white'
                    white_pieces.pop(idx)
                    white_locations.pop(idx)
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 0
                selection = 100
                valid_moves = []
                if is_checkmate('white'):  # ✏️ NEW
                    winner = 'black'
        # AI plays white
        elif game_mode == 2 and turn_step == 0:
            _, best_piece, best_move = minimax(3, -999999, 999999, True,
                                            white_pieces, white_locations,
                                            black_pieces, black_locations)
            if best_piece is not None and best_move is not None:
                white_locations[best_piece] = best_move
                if best_move in black_locations:
                    idx = black_locations.index(best_move)
                    captured_pieces_white.append(black_pieces[idx])
                    if black_pieces[idx] == 'king':
                        winner = 'white'
                    black_pieces.pop(idx)
                    black_locations.pop(idx)
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 2
                selection = 100
                valid_moves = []
                if is_checkmate('black'):  # ✏️ NEW
                    winner = 'white'
    if winner != '':
        game_over = True
        draw_game_over()
    pygame.display.flip()
pygame.quit()