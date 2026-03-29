# board.py
# All Pygame rendering functions.
# Each function receives the data it needs as parameters — no globals.

import pygame
from config import WIDTH, HEIGHT, BOARD_SIZE, CELL_SIZE, PIECE_LIST


def draw_mode_selection(screen, big_font, medium_font):
    """Render the game-mode selection screen."""
    screen.fill('dark gray')
    screen.blit(big_font.render('Select Game Mode', True, 'white'), (150, 100))

    # Player vs Player
    pygame.draw.rect(screen, 'gray', [150, 200, 400, 60])
    pygame.draw.rect(screen, 'gold', [150, 200, 400, 60], 3)
    screen.blit(medium_font.render('Player vs Player', True, 'white'), (200, 215))

    # Player vs AI
    pygame.draw.rect(screen, 'gray', [150, 300, 400, 60])
    pygame.draw.rect(screen, 'gold', [150, 300, 400, 60], 3)
    screen.blit(medium_font.render('You(White) vs AI(Black)', True, 'white'), (155, 315))

    # AI vs Player
    pygame.draw.rect(screen, 'gray', [150, 400, 400, 60])
    pygame.draw.rect(screen, 'gold', [150, 400, 400, 60], 3)
    screen.blit(medium_font.render('AI(White) vs You(Black)', True, 'white'), (155, 415))

    pygame.display.flip()


def draw_board(screen, turn_step, big_font, medium_font):
    """Draw the checkerboard, grid lines, status bar, and forfeit button."""
    board_px = BOARD_SIZE * CELL_SIZE  # 500

    # Checkerboard squares
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                pygame.draw.rect(screen, 'light gray',
                                 [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE])

    # Status bar at the bottom
    pygame.draw.rect(screen, 'gray', [0, board_px, WIDTH, HEIGHT - board_px])
    pygame.draw.rect(screen, 'gold', [0, board_px, WIDTH, HEIGHT - board_px], 5)

    # Right panel border
    pygame.draw.rect(screen, 'gold', [board_px, 0, WIDTH - board_px, HEIGHT], 5)

    # Turn status text
    status_text = [
        'White: Select a Piece to Move!',
        'White: Select a Destination!',
        'Black: Select a Piece to Move!',
        'Black: Select a Destination!',
    ]
    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 520))

    # Grid lines
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, 'black', (0, CELL_SIZE * i), (board_px, CELL_SIZE * i), 2)
        pygame.draw.line(screen, 'black', (CELL_SIZE * i, 0), (CELL_SIZE * i, board_px), 2)

    # Forfeit button label
    screen.blit(medium_font.render('FORFEIT', True, 'black'), (510, 530))


def draw_pieces(screen, white_pieces, white_locations, black_pieces, black_locations,
                turn_step, selection, white_images, black_images, white_pawn_img, black_pawn_img):
    """Draw all pieces onto the board and highlight the selected piece."""
    # White pieces
    for i in range(len(white_pieces)):
        index = PIECE_LIST.index(white_pieces[i])
        x = white_locations[i][0] * 100
        y = white_locations[i][1] * 100
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn_img, (x + 22, y + 30))
        else:
            screen.blit(white_images[index], (x + 10, y + 10))
        # Highlight selected white piece
        if turn_step < 2 and selection == i:
            pygame.draw.rect(screen, 'red', [x + 1, y + 1, 100, 100], 2)

    # Black pieces
    for i in range(len(black_pieces)):
        index = PIECE_LIST.index(black_pieces[i])
        x = black_locations[i][0] * 100
        y = black_locations[i][1] * 100
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn_img, (x + 22, y + 30))
        else:
            screen.blit(black_images[index], (x + 10, y + 10))
        # Highlight selected black piece
        if turn_step >= 2 and selection == i:
            pygame.draw.rect(screen, 'blue', [x + 1, y + 1, 100, 100], 2)


def draw_valid(screen, moves, turn_step):
    """Draw dots on all valid destination squares for the selected piece."""
    color = 'red' if turn_step < 2 else 'blue'
    for move in moves:
        pygame.draw.circle(screen, color,
                           (move[0] * 100 + 50, move[1] * 100 + 50), 5)


def draw_captured(screen, captured_pieces_white, captured_pieces_black,
                  small_black_images, small_white_images):
    """
    Draw captured pieces in the right panel.
    captured_pieces_white = black pieces captured by white (shown as small black icons).
    captured_pieces_black = white pieces captured by black (shown as small white icons).
    """
    for i, piece in enumerate(captured_pieces_white):
        index = PIECE_LIST.index(piece)
        screen.blit(small_black_images[index], (510, 5 + 45 * i))
    for i, piece in enumerate(captured_pieces_black):
        index = PIECE_LIST.index(piece)
        screen.blit(small_white_images[index], (610, 5 + 45 * i))


def draw_check(screen, turn_step, counter,
               white_pieces, white_locations, black_pieces, black_locations,
               is_in_check_fn):
    """Flash a colored border around the king that is currently in check."""
    if counter >= 15:
        return  # only flash during first half of the counter cycle

    if turn_step < 2:
        if is_in_check_fn('white', white_pieces, white_locations, black_pieces, black_locations):
            if 'king' in white_pieces:
                idx = white_pieces.index('king')
                x, y = white_locations[idx]
                pygame.draw.rect(screen, 'dark red',
                                 [x * 100 + 1, y * 100 + 1, 100, 100], 5)
    else:
        if is_in_check_fn('black', white_pieces, white_locations, black_pieces, black_locations):
            if 'king' in black_pieces:
                idx = black_pieces.index('king')
                x, y = black_locations[idx]
                pygame.draw.rect(screen, 'dark blue',
                                 [x * 100 + 1, y * 100 + 1, 100, 100], 5)


def draw_game_over(screen, winner, font):
    """Overlay a game-over message in the centre of the board area."""
    pygame.draw.rect(screen, 'black', [50, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (60, 210))
    screen.blit(font.render('Press ENTER to Restart!', True, 'white'), (60, 240))


def load_images():
    """
    Load and scale all piece images from the img/ directory.
    Returns: white_images, small_white_images, black_images, small_black_images,
             white_pawn_img, black_pawn_img
    Image order matches PIECE_LIST: ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
    """
    def load(path, size):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    # Full-size images
    white_pawn   = load('img/white pawn.png',   (65, 65))
    white_queen  = load('img/white queen.png',  (80, 80))
    white_king   = load('img/white king.png',   (80, 80))
    white_knight = load('img/white knight.png', (80, 80))
    white_rook   = load('img/white rook.png',   (80, 80))
    white_bishop = load('img/white bishop.png', (80, 80))

    black_pawn   = load('img/black pawn.png',   (65, 65))
    black_queen  = load('img/black queen.png',  (80, 80))
    black_king   = load('img/black king.png',   (80, 80))
    black_knight = load('img/black knight.png', (80, 80))
    black_rook   = load('img/black rook.png',   (80, 80))
    black_bishop = load('img/black bishop.png', (80, 80))

    # Small versions for the captured-pieces panel
    white_pawn_s   = pygame.transform.scale(white_pawn,   (45, 45))
    white_queen_s  = pygame.transform.scale(white_queen,  (45, 45))
    white_king_s   = pygame.transform.scale(white_king,   (45, 45))
    white_knight_s = pygame.transform.scale(white_knight, (45, 45))
    white_rook_s   = pygame.transform.scale(white_rook,   (45, 45))
    white_bishop_s = pygame.transform.scale(white_bishop, (45, 45))

    black_pawn_s   = pygame.transform.scale(black_pawn,   (45, 45))
    black_queen_s  = pygame.transform.scale(black_queen,  (45, 45))
    black_king_s   = pygame.transform.scale(black_king,   (45, 45))
    black_knight_s = pygame.transform.scale(black_knight, (45, 45))
    black_rook_s   = pygame.transform.scale(black_rook,   (45, 45))
    black_bishop_s = pygame.transform.scale(black_bishop, (45, 45))

    # Order: ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
    white_images       = [white_pawn,   white_queen,   white_king,   white_knight,   white_rook,   white_bishop]
    small_white_images = [white_pawn_s, white_queen_s, white_king_s, white_knight_s, white_rook_s, white_bishop_s]
    black_images       = [black_pawn,   black_queen,   black_king,   black_knight,   black_rook,   black_bishop]
    small_black_images = [black_pawn_s, black_queen_s, black_king_s, black_knight_s, black_rook_s, black_bishop_s]

    return (white_images, small_white_images, black_images, small_black_images,
            white_pawn, black_pawn)
