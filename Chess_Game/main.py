# main.py
# Entry point: Pygame initialization, game state, main loop, and event handling.

import pygame
import random

from config import (WIDTH, HEIGHT, FPS,
                    WHITE_LOCATIONS_INIT, BLACK_LOCATIONS_INIT)
from board import (load_images, draw_mode_selection, draw_board, draw_pieces,
                    draw_valid, draw_captured, draw_check, draw_game_over)
from pieces import check_options
from utils import (is_in_check, is_checkmate, get_valid_moves,
                    check_insufficient_material, check_threefold)
from ai import get_ai_move


# ---------------------------------------------------------------------------
# Pygame setup
# ---------------------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')

font        = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 24)
big_font    = pygame.font.Font('freesansbold.ttf', 24)
timer       = pygame.time.Clock()

# Load all piece images
(white_images, small_white_images,
 black_images, small_black_images,
 white_pawn_img, black_pawn_img) = load_images()


# ---------------------------------------------------------------------------
# Back-row shuffler (Fisher-Yates on the 4 non-king pieces + random king pos)
# ---------------------------------------------------------------------------

def shuffle_back_row():
    """
    Return a randomised back row of 5 pieces guaranteed to contain exactly
    one king, one queen, one rook, one bishop, and one knight.
    """
    pieces_pool = ['rook', 'knight', 'queen', 'bishop']
    random.shuffle(pieces_pool)
    king_index = random.randint(0, 4)
    pieces_pool.insert(king_index, 'king')
    return pieces_pool


# ---------------------------------------------------------------------------
# Pawn promotion
# ---------------------------------------------------------------------------

def check_promotion(state, index, color):
    """Promote a pawn that has reached the far rank to a queen (in-place)."""
    wp = state['white_pieces']
    wl = state['white_locations']
    bp = state['black_pieces']
    bl = state['black_locations']

    if color == 'white':
        if wp[index] == 'pawn' and wl[index][1] == 0:
            wp[index] = 'queen'
    else:
        if bp[index] == 'pawn' and bl[index][1] == 4:
            bp[index] = 'queen'


# ---------------------------------------------------------------------------
# Game-state initialisation
# ---------------------------------------------------------------------------

def init_game_state():
    """Return a fresh game-state dictionary with shuffled back rows."""
    w_back = shuffle_back_row()
    b_back = shuffle_back_row()
    w_pieces = w_back + ['pawn'] * 5
    b_pieces = b_back + ['pawn'] * 5
    w_locs   = list(WHITE_LOCATIONS_INIT)
    b_locs   = list(BLACK_LOCATIONS_INIT)
    return {
        'white_pieces':           w_pieces,
        'white_locations':        w_locs,
        'black_pieces':           b_pieces,
        'black_locations':        b_locs,
        'captured_pieces_white':  [],   # black pieces taken by white
        'captured_pieces_black':  [],   # white pieces taken by black
        'turn_step':              0,    # 0/1 = white's turn, 2/3 = black's turn
        'selection':              100,  # 100 = nothing selected
        'valid_moves':            [],
        'counter':                0,    # flashing animation counter
        'winner':                 '',   # '', 'white', 'black', or 'draw'
        'game_over':              False,
        'game_mode':              0,    # 0=PvP, 1=Player(W) vs AI(B), 2=AI(W) vs Player(B)
        'game_mode_selected':     False,
        'board_history':          [],   # list of (w_locs_tuple, b_locs_tuple, turn_step)
        'halfmove_counter':       0,    # unused in game logic currently, reserved
        'move_counter':           0,    # full-move counter
        'white_options':          check_options(w_pieces, w_locs, 'white', w_locs, b_locs),
        'black_options':          check_options(b_pieces, b_locs, 'black', w_locs, b_locs),
    }


# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------

def handle_mode_selection(state, event):
    """Process a click on the mode-selection screen."""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        x, y = event.pos
        if 150 <= x <= 550:
            if 200 <= y <= 260:
                state['game_mode'] = 0
                state['game_mode_selected'] = True
            elif 300 <= y <= 360:
                state['game_mode'] = 1
                state['game_mode_selected'] = True
            elif 400 <= y <= 460:
                state['game_mode'] = 2
                state['game_mode_selected'] = True


def handle_click(state, click_coords):
    """Process a board click during normal gameplay."""
    wp  = state['white_pieces']
    wl  = state['white_locations']
    bp  = state['black_pieces']
    bl  = state['black_locations']
    ts  = state['turn_step']
    sel = state['selection']
    vm  = state['valid_moves']
    bh  = state['board_history']

    if ts <= 1:  # White's turn
        # Forfeit
        if click_coords in [(5, 5), (6, 5)]:
            state['winner'] = 'black'
            return

        # Select a white piece
        if click_coords in wl:
            state['selection'] = wl.index(click_coords)
            if ts == 0:
                state['turn_step'] = 1

        # Move to a valid square
        if click_coords in vm and sel != 100:
            # Capture first, then move
            if click_coords in bl:
                idx = bl.index(click_coords)
                state['captured_pieces_white'].append(bp[idx])
                if bp[idx] == 'king':
                    state['winner'] = 'white'
                bp.pop(idx)
                bl.pop(idx)

            wl[sel] = click_coords
            check_promotion(state, sel, 'white')

            # Refresh options
            state['white_options'] = check_options(wp, wl, 'white', wl, bl)
            state['black_options'] = check_options(bp, bl, 'black', wl, bl)

            # Record board state for repetition detection
            bh.append((tuple(wl), tuple(bl), 2))

            state['turn_step'] = 2
            state['selection'] = 100
            state['valid_moves'] = []

    elif ts > 1:  # Black's turn
        # Forfeit
        if click_coords in [(5, 5), (6, 5)]:
            state['winner'] = 'white'
            return

        # Select a black piece
        if click_coords in bl:
            state['selection'] = bl.index(click_coords)
            if ts == 2:
                state['turn_step'] = 3

        # Move to a valid square
        if click_coords in vm and sel != 100:
            # Capture first, then move
            if click_coords in wl:
                idx = wl.index(click_coords)
                state['captured_pieces_black'].append(wp[idx])
                if wp[idx] == 'king':
                    state['winner'] = 'black'
                wp.pop(idx)
                wl.pop(idx)

            bl[sel] = click_coords
            check_promotion(state, sel, 'black')

            # Refresh options
            state['black_options'] = check_options(bp, bl, 'black', wl, bl)
            state['white_options'] = check_options(wp, wl, 'white', wl, bl)

            # Record board state for repetition detection
            bh.append((tuple(wl), tuple(bl), 0))

            state['turn_step'] = 0
            state['selection'] = 100
            state['valid_moves'] = []


def handle_restart(state):
    """Reset game state for a new game (returns to mode selection)."""
    fresh = init_game_state()
    state.update(fresh)


# ---------------------------------------------------------------------------
# Win / draw detection (called once per frame after moves)
# ---------------------------------------------------------------------------

def check_end_conditions(state):
    """
    Evaluate checkmate, stalemate, insufficient material, and threefold
    repetition.  Sets state['winner'] when a terminal condition is found.
    """
    if state['winner'] != '' or state['game_over']:
        return

    wp = state['white_pieces']
    wl = state['white_locations']
    bp = state['black_pieces']
    bl = state['black_locations']
    ts = state['turn_step']
    bh = state['board_history']

    # Insufficient material
    if check_insufficient_material(wp, bp):
        state['winner'] = 'draw'
        return

    # Threefold repetition
    if check_threefold(bh, wl, bl, ts):
        state['winner'] = 'draw'
        return

    # Checkmate / stalemate
    if ts <= 1 and is_checkmate('white', wp, wl, bp, bl):
        state['winner'] = 'black' if is_in_check('white', wp, wl, bp, bl) else 'draw'
    elif ts > 1 and is_checkmate('black', wp, wl, bp, bl):
        state['winner'] = 'white' if is_in_check('black', wp, wl, bp, bl) else 'draw'


# ---------------------------------------------------------------------------
# AI move execution
# ---------------------------------------------------------------------------

def run_ai_if_needed(state):
    """If it's the AI's turn, compute and apply its move."""
    if state['game_over'] or not state['game_mode_selected']:
        return

    wp = state['white_pieces']
    wl = state['white_locations']
    bp = state['black_pieces']
    bl = state['black_locations']
    ts = state['turn_step']
    gm = state['game_mode']
    bh = state['board_history']
        # Determine if it's the AI's turn
    ai_turn = (gm == 1 and ts == 2) or (gm == 2 and ts == 0)

    if not ai_turn:
        state['ai_move_time'] = None   # reset when it's not AI's turn
        return

    # Start the timer the moment it becomes AI's turn
    if state['ai_move_time'] is None:
        state['ai_move_time'] = pygame.time.get_ticks()
        return

    # Wait until 1 second has passed
    if pygame.time.get_ticks() - state['ai_move_time'] < 1000:
        return

    # Mode 1: AI plays black (turn_step == 2)
    if gm == 1 and ts == 2:      
        best_piece, best_move = get_ai_move(False, wp, wl, bp, bl)
        if best_piece is not None and best_move is not None:
            if best_move in wl:
                idx = wl.index(best_move)
                state['captured_pieces_black'].append(wp[idx])
                if wp[idx] == 'king':
                    state['winner'] = 'white'
                wp.pop(idx)
                wl.pop(idx)
            bl[best_piece] = best_move
            check_promotion(state, best_piece, 'black')
            state['black_options'] = check_options(bp, bl, 'black', wl, bl)
            state['white_options'] = check_options(wp, wl, 'white', wl, bl)
            bh.append((tuple(wl), tuple(bl), 0))
            state['turn_step'] = 0
            state['selection'] = 100
            state['valid_moves'] = []

    # Mode 2: AI plays white (turn_step == 0)
    elif gm == 2 and ts == 0:
        pygame.display.flip()          # ← render your move first
        pygame.time.delay(2000)        # ← then wait 1 second
        best_piece, best_move = get_ai_move(True, wp, wl, bp, bl)
        if best_piece is not None and best_move is not None:  
            if best_move in bl:
                idx = bl.index(best_move)
                state['captured_pieces_white'].append(bp[idx])
                if bp[idx] == 'king':
                    state['winner'] = 'white'
                bp.pop(idx)
                bl.pop(idx)
            wl[best_piece] = best_move
            check_promotion(state, best_piece, 'white')
            state['white_options'] = check_options(wp, wl, 'white', wl, bl)
            state['black_options'] = check_options(bp, bl, 'black', wl, bl)
            bh.append((tuple(wl), tuple(bl), 2))
            state['turn_step'] = 2
            state['selection'] = 100
            state['valid_moves'] = []


# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------

def main():
    state = init_game_state()
    run   = True

    while run:
        timer.tick(FPS)

        # ── Mode selection screen ──────────────────────────────────────────
        if not state['game_mode_selected']:
            draw_mode_selection(screen, big_font, medium_font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                handle_mode_selection(state, event)
            continue

        # ── Animation counter ─────────────────────────────────────────────
        state['counter'] = (state['counter'] + 1) % 30

        # ── Render ────────────────────────────────────────────────────────
        screen.fill('dark gray')
        draw_board(screen, state['turn_step'], big_font, medium_font)
        draw_pieces(
            screen,
            state['white_pieces'], state['white_locations'],
            state['black_pieces'], state['black_locations'],
            state['turn_step'], state['selection'],
            white_images, black_images,
            white_pawn_img, black_pawn_img
        )
        draw_captured(
            screen,
            state['captured_pieces_white'], state['captured_pieces_black'],
            small_black_images, small_white_images
        )
        draw_check(
            screen,
            state['turn_step'], state['counter'],
            state['white_pieces'], state['white_locations'],
            state['black_pieces'], state['black_locations'],
            is_in_check
        )

        # Compute and draw valid moves for the selected piece
        if state['selection'] != 100:
            state['valid_moves'] = get_valid_moves(
                state['selection'], state['turn_step'],
                state['white_options'], state['black_options'],
                state['white_pieces'], state['white_locations'],
                state['black_pieces'], state['black_locations']
            )
            draw_valid(screen, state['valid_moves'], state['turn_step'])

        # ── Events ────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not state['game_over']:
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                handle_click(state, (x_coord, y_coord))

            if event.type == pygame.KEYDOWN and state['game_over']:
                if event.key == pygame.K_RETURN:
                    handle_restart(state)

        # ── AI turn ───────────────────────────────────────────────────────
        run_ai_if_needed(state)

        # ── End-condition check ───────────────────────────────────────────
        check_end_conditions(state)

        # ── Game over overlay ─────────────────────────────────────────────
        if state['winner'] != '':
            state['game_over'] = True
            draw_game_over(screen, state['winner'], font)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
