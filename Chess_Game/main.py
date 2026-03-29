# main.py
# Entry point: Pygame initialization, game state, main loop, and event handling.

import pygame

from config import (WIDTH, HEIGHT, FPS,
                    WHITE_PIECES_INIT, WHITE_LOCATIONS_INIT,
                    BLACK_PIECES_INIT, BLACK_LOCATIONS_INIT)
from board import (load_images, draw_mode_selection, draw_board, draw_pieces,
                draw_valid, draw_captured, draw_check, draw_game_over)
from pieces import check_options
from utils import is_in_check, is_checkmate, get_valid_moves
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
# Game-state initialisation
# ---------------------------------------------------------------------------

def init_game_state():
    """Return a fresh game-state dictionary."""
    w_pieces = WHITE_PIECES_INIT[:]
    w_locs   = WHITE_LOCATIONS_INIT[:]
    b_pieces = BLACK_PIECES_INIT[:]
    b_locs   = BLACK_LOCATIONS_INIT[:]
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
        'winner':                 '',
        'game_over':              False,
        'game_mode':              0,    # 0=PvP, 1=Player(W) vs AI(B), 2=AI(W) vs Player(B)
        'game_mode_selected':     False,
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
            wl[sel] = click_coords
            # Capture?
            if click_coords in bl:
                idx = bl.index(click_coords)
                state['captured_pieces_white'].append(bp[idx])
                if bp[idx] == 'king':
                    state['winner'] = 'white'
                bp.pop(idx)
                bl.pop(idx)
            # Refresh options and end turn
            state['white_options'] = check_options(wp, wl, 'white', wl, bl)
            state['black_options'] = check_options(bp, bl, 'black', wl, bl)
            state['turn_step'] = 2
            state['selection'] = 100
            state['valid_moves'] = []
            if is_checkmate('black', wp, wl, bp, bl):
                state['winner'] = 'white'

    if ts > 1:  # Black's turn
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
            bl[sel] = click_coords
            # Capture?
            if click_coords in wl:
                idx = wl.index(click_coords)
                state['captured_pieces_black'].append(wp[idx])
                if wp[idx] == 'king':
                    state['winner'] = 'black'
                wp.pop(idx)
                wl.pop(idx)
            # Refresh options and end turn
            state['black_options'] = check_options(bp, bl, 'black', wl, bl)
            state['white_options'] = check_options(wp, wl, 'white', wl, bl)
            state['turn_step'] = 0
            state['selection'] = 100
            state['valid_moves'] = []
            if is_checkmate('white', wp, wl, bp, bl):
                state['winner'] = 'black'


def handle_restart(state):
    """Reset game state for a new game."""
    fresh = init_game_state()
    state.update(fresh)


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

    # Mode 1: AI plays black (turn_step == 2)
    if gm == 1 and ts == 2:
        best_piece, best_move = get_ai_move(False, wp, wl, bp, bl)
        if best_piece is not None and best_move is not None:
            bl[best_piece] = best_move
            if best_move in wl:
                idx = wl.index(best_move)
                state['captured_pieces_black'].append(wp[idx])
                if wp[idx] == 'king':
                    state['winner'] = 'white'
                wp.pop(idx)
                wl.pop(idx)
            state['black_options'] = check_options(bp, bl, 'black', wl, bl)
            state['white_options'] = check_options(wp, wl, 'white', wl, bl)
            state['turn_step'] = 0
            state['selection'] = 100
            state['valid_moves'] = []
            if is_checkmate('white', wp, wl, bp, bl):
                state['winner'] = 'black'

    # Mode 2: AI plays white (turn_step == 0)
    elif gm == 2 and ts == 0:
        best_piece, best_move = get_ai_move(True, wp, wl, bp, bl)
        if best_piece is not None and best_move is not None:
            wl[best_piece] = best_move
            if best_move in bl:
                idx = bl.index(best_move)
                state['captured_pieces_white'].append(bp[idx])
                if bp[idx] == 'king':
                    state['winner'] = 'white'
                bp.pop(idx)
                bl.pop(idx)
            state['white_options'] = check_options(wp, wl, 'white', wl, bl)
            state['black_options'] = check_options(bp, bl, 'black', wl, bl)
            state['turn_step'] = 2
            state['selection'] = 100
            state['valid_moves'] = []
            if is_checkmate('black', wp, wl, bp, bl):
                state['winner'] = 'white'


# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------

def main():
    state = init_game_state()
    run = True

    while run:
        timer.tick(FPS)

        # ── Mode selection screen ──────────────────────────────────────────
        if not state['game_mode_selected']:
            draw_mode_selection(screen, big_font, medium_font)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                handle_mode_selection(state, event)
            continue  # don't draw the board until a mode is chosen

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

        # ── Game over overlay ─────────────────────────────────────────────
        if state['winner'] != '':
            state['game_over'] = True
            draw_game_over(screen, state['winner'], font)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
