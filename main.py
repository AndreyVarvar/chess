import pieces
from pieces import *
import pygame
import time

pygame.init()

display_width, display_height = 720, 640

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Chess")

clock = pygame.time.Clock()


class Button:
    def __init__(self, rect, text: str, button_color, text_color, outline_width, outline_color, corner_radius,
                 font="Aerial", font_size=30):
        self.rect = rect
        self.color = button_color
        self.new_color = self.color
        self.text_color = text_color
        self.outline_width = outline_width
        self.outline_color = outline_color
        self.new_outline_color = self.outline_color
        self.corner_radius = corner_radius
        self.font_size = font_size

        self.font = pygame.font.SysFont(font, font_size)
        self.text = text
        self.text_object = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_object.get_rect()

        self.hover_sound = pygame.mixer.Sound("Sounds/button hover.wav")
        self.click_sound = pygame.mixer.Sound("Sounds/button click.wav")
        self.hover_sound.set_volume(0.5)
        self.click_sound.set_volume(0.5)
        self.hovered = False
        self.clicked = False

    def render(self):
        self.text_rect.center = (display_width / 2, self.rect[1] + self.rect[2] / 2 - 10)

        if self.text_rect[2] > self.rect[2]:
            self.rect = self.text_rect[2] + 10

        if self.text_rect[3] > self.rect[3]:
            self.rect[3] = self.text_rect[3] + 10

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        self.new_color = self.color
        self.new_outline_color = self.outline_color

        if pygame.Rect(self.rect).collidepoint(mouse_pos[0], mouse_pos[1]):
            if not self.hovered and not self.clicked:
                pygame.mixer.Sound.play(self.hover_sound)
                pygame.mixer.music.stop()
                self.hovered = True

            if not self.clicked and mouse_pressed[0]:
                pygame.mixer.Sound.play(self.click_sound)
                pygame.mixer.music.stop()
                self.clicked = True
            elif not mouse_pressed[0]:
                self.clicked = False

            color_darkener = 20

            if self.clicked:
                color_darkener = 35

            self.new_color = (self.color[0] - color_darkener if self.color[0] > color_darkener else self.color[0],
                              self.color[1] - color_darkener if self.color[1] > color_darkener else self.color[1],
                              self.color[2] - color_darkener if self.color[2] > color_darkener else self.color[2])

            self.new_outline_color = (
                self.outline_color[0] - color_darkener if self.outline_color[0] > color_darkener else
                self.outline_color[0],

                self.outline_color[1] - color_darkener if self.outline_color[1] > color_darkener else
                self.outline_color[1],

                self.outline_color[2] - color_darkener if self.outline_color[2] > color_darkener else
                self.outline_color[2])

        else:
            self.hovered = False
            self.clicked = False

        pygame.draw.rect(display, self.new_color, self.rect, 0, self.corner_radius)

        if self.outline_width > 0:
            pygame.draw.rect(display, self.new_outline_color, self.rect, self.outline_width, self.corner_radius)

        text_to_screen(self.text, 0, ((self.rect[3] - display_height) / 2) + self.rect[1], (250, 250, 250), 30)

    def return_if_pressed(self):
        mouse_pos = pygame.mouse.get_pos()
        return True if pygame.Rect(self.rect).collidepoint(mouse_pos[0], mouse_pos[1]) else False


def promotion(p_pos, m_pos, m_pressed):  # p_pos -- piece_pos, m_pos -- mouse_pos, m_pressed -- mouse_pressed
    overlay = pygame.Surface((640, 640))
    overlay.set_alpha(150)
    overlay.fill((50, 50, 50))
    display.blit(overlay, (0, 0))

    new_piece = None

    if p_pos[1] == 0:
        new_piece_pos = {(p_pos[0] * 80, 0): "queen",
                         (p_pos[0] * 80, 80): "rook",
                         (p_pos[0] * 80, 160): "knight",
                         (p_pos[0] * 80, 240): "bishop"}

        pygame.draw.rect(display, (140, 160, 140), (p_pos[0] * 80, 0, 80, 320), 0, 3)

        pygame.draw.rect(display, (120, 140, 120), (p_pos[0] * 80, 0, 80, 80), 5)
        display.blit(Piece("white", "queen").image, (p_pos[0] * 80, 0))

        pygame.draw.rect(display, (120, 140, 120), (p_pos[0] * 80, 80, 80, 80), 5)
        display.blit(Piece("white", "rook").image, (p_pos[0] * 80, 80))

        pygame.draw.rect(display, (120, 140, 120), (p_pos[0] * 80, 160, 80, 80), 5)
        display.blit(Piece("white", "knight").image, (p_pos[0] * 80, 160))

        pygame.draw.rect(display, (120, 140, 120), (p_pos[0] * 80, 240, 80, 80), 5)
        display.blit(Piece("white", "bishop").image, (p_pos[0] * 80, 240))

        if m_pressed[0]:
            m_pos = ((m_pos[0] // 80) * 80, (m_pos[1] // 80) * 80)

            try:
                new_piece = Piece("white", new_piece_pos[m_pos])

            except KeyError:
                new_piece = None

    elif p_pos[1] == 7:
        new_piece_pos = {(p_pos[0] * 80, 320): "queen",
                         (p_pos[0] * 80, 400): "rook",
                         (p_pos[0] * 80, 480): "knight",
                         (p_pos[0] * 80, 560): "bishop"}

        pygame.draw.rect(display, (140, 160, 140), (p_pos[0] * 80, 320, 80, 320), 0, 3)

        pygame.draw.rect(display, (120, 140, 120), (p_pos[0] * 80, 0, 320, 80), 5)
        display.blit(Piece("black", "queen").image, (p_pos[0] * 80, 320))

        pygame.draw.rect(display, (120, 140, 120), (p_pos[0] * 80, 80, 400, 80), 5)
        display.blit(Piece("black", "rook").image, (p_pos[0] * 80, 400))

        pygame.draw.rect(display, (120, 140, 120), (p_pos[0] * 80, 160, 480, 80), 5)
        display.blit(Piece("black", "knight").image, (p_pos[0] * 80, 480))

        pygame.draw.rect(display, (120, 140, 120), (p_pos[0] * 80, 240, 560, 80), 5)
        display.blit(Piece("black", "bishop").image, (p_pos[0] * 80, 560))

        if m_pressed[0]:
            m_pos = ((m_pos[0] // 80) * 80, (m_pos[1] // 80) * 80)

            try:
                new_piece = Piece("black", new_piece_pos[m_pos])

            except KeyError:
                new_piece = None
    return new_piece


def which_piece_selected(b, m_p):  # b -- board, m_p -- mouse_pos
    cell_pos = (m_p[0] // 80, m_p[1] // 80)

    p_selected = None
    p_pos = None

    for rank_counter, rank in enumerate(b):
        for cell_counter, cell in enumerate(rank):
            if (cell_counter, rank_counter) == cell_pos:
                p_selected = cell
                p_pos = cell_pos

    if p_selected == "'":
        p_selected = None
        p_pos = None

    return p_selected, p_pos


def draw_pieces(b):  # b -- board
    for rank_counter, rank in enumerate(b):
        for cell_counter, cell in enumerate(rank):
            if cell != "'":
                display.blit(cell.image, (cell_counter * 80, rank_counter * 80))


def draw_board():  # b -- board
    cell_width = 80

    display.fill((80, 80, 80))
    pygame.draw.rect(display, (60, 60, 60), (640, 0, 80, 640), 3)

    for rank in range(8):
        for file in range(8):
            if (file + rank) % 2 == 0:
                color1 = (238, 238, 210)
                color2 = (198, 198, 170)
            else:
                color1 = (118, 150, 86)
                color2 = (78, 110, 46)

            pygame.draw.rect(display, color1, (file * cell_width, rank * cell_width, cell_width, cell_width))
            pygame.draw.rect(display, color2, (file * cell_width, rank * cell_width, cell_width, cell_width), 3)


def draw_eaten_pieces(pieces_eaten_dict, color):
    all_pieces = ["pawn", "knight", "bishop", "rook", "queen"]

    scale = (30, 30)

    if color == "black":
        for i, piece in enumerate(all_pieces):
            display.blit(pygame.transform.scale(pygame.image.load(f"Sprites/black {piece}.png"), scale),
                         (645, 130 - (i * 30)))
            text_to_screen(f": {pieces_eaten_dict[piece + 's']}", -(display_height / 2) + 645,
                           -(display_height / 2) + 145 - (i * 30), (250, 250, 250), 20)

    else:
        for i, piece in enumerate(all_pieces):
            display.blit(pygame.transform.scale(pygame.image.load(f"Sprites/white {piece}.png"), scale),
                         (645, 600 - (i * 30)))
            text_to_screen(f": {pieces_eaten_dict[piece + 's']}", -(display_height / 2) + 645,
                           -(display_height / 2) + 615 - (i * 30), (250, 250, 250), 20)


def main_loop():
    board = [[Piece("black", "rook"), Piece("black", "knight"), Piece("black", "bishop"), Piece("black", "queen"),
              Piece("black", "king"), Piece("black", "bishop"), Piece("black", "knight"), Piece("black", "rook")],

             [Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn"),
              Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn"), Piece("black", "pawn")],

             ["'", "'", "'", "'", "'", "'", "'", "'"],

             ["'", "'", "'", "'", "'", "'", "'", "'"],

             ["'", "'", "'", "'", "'", "'", "'", "'"],

             ["'", "'", "'", "'", "'", "'", "'", "'"],

             [Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn"),
              Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn"), Piece("white", "pawn")],

             [Piece("white", "rook"), Piece("white", "knight"), Piece("white", "bishop"), Piece("white", "queen"),
              Piece("white", "king"), Piece("white", "bishop"), Piece("white", "knight"), Piece("white", "rook")]]

    g_o = False

    piece_selected = None
    piece_pos = None

    pos_moves = []

    player_to_move = "white"

    freeze_game = False

    win = None

    king_in_check = False

    run_one_more_time = False

    b_pieces_eaten = {"pawns": 0,
                      "knights": 0,
                      "bishops": 0,
                      "rooks": 0,
                      "queens": 0}

    w_pieces_eaten = {"pawns": 0,
                      "knights": 0,
                      "bishops": 0,
                      "rooks": 0,
                      "queens": 0}

    piece_placed_sound = pygame.mixer.Sound("Sounds/piece_placed.wav")
    game_over_sound = pygame.mixer.Sound("Sounds/game_over.wav")

    g_e = False

    while ((not g_o and win is None) or run_one_more_time) and not g_e:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_e = True

        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        draw_board()

        if piece_selected is not None:
            if piece_selected.type == "king":
                king_in_check = None

        if king_in_check is not None:
            if king_in_check:
                king_pos = return_king_pos(board, player_to_move)

                pygame.draw.rect(display, (203, 67, 53), (king_pos[0] * 80, king_pos[1] * 80, 80, 80))
                pygame.draw.rect(display, (173, 37, 23), (king_pos[0] * 80, king_pos[1] * 80, 80, 80), 3)

        if piece_selected is not None:
            if piece_selected.color == player_to_move:
                for move_pos in pos_moves:
                    if (move_pos[0] + move_pos[1]) % 2 == 0:
                        pygame.draw.rect(display, (148, 148, 120), (move_pos[0] * 80, move_pos[1] * 80, 80, 80))
                        pygame.draw.rect(display, (108, 108, 80), (move_pos[0] * 80, move_pos[1] * 80, 80, 80), 3)
                    else:
                        pygame.draw.rect(display, (58, 90, 26), (move_pos[0] * 80, move_pos[1] * 80, 80, 80))
                        pygame.draw.rect(display, (18, 50, 0), (move_pos[0] * 80, move_pos[1] * 80, 80, 80), 3)

        draw_pieces(board)

        if piece_selected is not None:
            if piece_selected.color == player_to_move:
                board[piece_pos[1]][piece_pos[0]] = "'"
                display.blit(piece_selected.image, (mouse_pos[0] - 40, mouse_pos[1] - 40))

        if mouse_pressed[0] and piece_selected is None and not freeze_game:
            piece_selected, piece_pos = which_piece_selected(board, mouse_pos)

            if piece_selected is not None:
                if piece_selected.color == player_to_move:
                    pos_moves = pieces.possible_moves(board, piece_selected, piece_pos)

            else:
                piece_selected = None
                piece_pos = None
                pos_moves = []

        elif not mouse_pressed[0] and piece_selected is not None:
            if (mouse_pos[0] // 80, mouse_pos[1] // 80) in pos_moves:

                new_piece_pos = (mouse_pos[0] // 80, mouse_pos[1] // 80)

                # Check, if you ate a piece, and if yes, increase the pieces_eaten variable
                if board[new_piece_pos[1]][new_piece_pos[0]] != "'":
                    print("huh")
                    if player_to_move == "white":
                        b_pieces_eaten[board[new_piece_pos[1]][new_piece_pos[0]].type + "s"] += 1
                        print(b_pieces_eaten)
                    else:
                        w_pieces_eaten[board[new_piece_pos[1]][new_piece_pos[0]].type + "s"] += 1
                        print(w_pieces_eaten)

                if piece_selected != "'":
                    piece_selected.move_count += 1

                # change the player to move
                if player_to_move == "white":
                    player_to_move = "black"
                else:
                    player_to_move = "white"

                # check, if any pawns on these rows can be en_passant-ed, and if yes, set it to False
                row4 = board[3]
                row5 = board[4]

                for piece in row4:
                    if piece != "'":
                        if piece.type == "pawn":
                            piece.en_passant = False

                for piece in row5:
                    if piece != "'":
                        if piece.type == "pawn":
                            piece.en_passant = False

                if piece_selected.type == "pawn":
                    if abs(piece_pos[1] - new_piece_pos[1]) == 2:
                        piece_selected.en_passant = True

                # check, if the move you just made is an en_passant
                if piece_selected.type == "pawn":
                    if piece_pos[0] != (new_piece_pos[0]) and board[new_piece_pos[1]][new_piece_pos[0]] == "'":
                        board[piece_pos[1]][new_piece_pos[0]] = "'"

                # check if you castled with the king
                if piece_selected.type == "king":
                    if piece_pos[0] - new_piece_pos[0] == 2:
                        board[piece_pos[1]][new_piece_pos[0] + 1] = board[piece_pos[1]][0]
                        board[piece_pos[1]][0] = "'"

                    elif piece_pos[0] - new_piece_pos[0] == -2:
                        board[piece_pos[1]][new_piece_pos[0] - 1] = board[piece_pos[1]][7]
                        board[piece_pos[1]][7] = "'"

                # move the piece to the cell, the mouse clicked on
                board[mouse_pos[1] // 80][mouse_pos[0] // 80] = piece_selected

                pygame.mixer.Sound.play(piece_placed_sound)
                pygame.mixer.music.stop()

            else:
                board[piece_pos[1]][piece_pos[0]] = piece_selected

            piece_selected, piece_pos = None, []
            pos_moves = []

            win, king_in_check = pieces.print_check_mate(board, win, player_to_move,
                                                         pieces.return_king_pos(board, player_to_move))

            # Check, if only kings are left on the board
            only_kings_left = True  # set it to True, and when you find a piece that is not a king, that means
            # there are not only kings left on the board
            for row in board:
                for piece in row:
                    if piece != "'":
                        if piece.type != "king":
                            only_kings_left = False  # founded a piece that is not a king

            if only_kings_left:
                win = "draw"

        # check for any pawns on the sides of the board for promotion
        row1 = board[0]
        row8 = board[7]
        for index, piece in enumerate(row1):
            if piece != "'":
                if piece.type == "pawn":
                    freeze_game = True
                    if promotion([index, 0], mouse_pos, mouse_pressed) is not None:
                        freeze_game = False
                        board[0][index] = promotion([index, 0], mouse_pos, mouse_pressed)

        for index, piece in enumerate(row8):
            if piece != "'":
                if piece.type == "pawn":
                    freeze_game = True
                    if promotion([index, 7], mouse_pos, mouse_pressed) is not None:
                        board[7][index] = promotion([index, 7], mouse_pos, mouse_pressed)
                        freeze_game = False

        draw_eaten_pieces(b_pieces_eaten, "white")
        draw_eaten_pieces(w_pieces_eaten, "black")

        clock.tick(100)

        pygame.display.update()

        if win is not None and not run_one_more_time:
            run_one_more_time = True
            pygame.mixer.Sound.play(game_over_sound)
            pygame.mixer.music.stop()
        else:
            run_one_more_time = False

    time.sleep(1.5)

    return g_o, win, g_e


def text_to_screen(text, x_displace, y_displace, color, size):
    font = pygame.font.SysFont("Arial", size)

    text = font.render(text, True, color)
    text_rect = text.get_rect()
    text_rect.center = ((display_width // 2) + x_displace, (display_height // 2) + y_displace)
    display.blit(text, text_rect)


def post_game_screen(win, g_e, s_g):
    button_width = 170
    button_height = 50
    button_x = (display_width / 2) - (button_width / 2)
    button_1 = Button((button_x, 300, button_width, button_height), "New game", (160, 219, 142),
                      (255, 255, 255), 3, (130, 189, 112), 5, "Arial", 30)
    button_2 = Button((button_x, 370, button_width, button_height), "Title screen", (255, 165, 0),
                      (255, 255, 255), 3, (225, 135, 0), 5, "Arial", 30)

    button_1_pressed = False
    button_2_pressed = False

    background = pygame.image.load("Sprites/post game background.png")
    background.set_alpha(128)
    pygame.transform.scale(background, (1240, 640))

    while not g_e and not s_g:

        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_e = True

            if event.type == 1026:  # event 1026 -- mouse button up, cuz pygame.KEYUP not working
                mouse_clicked = True

        display.fill((0, 0, 0))
        display.blit(background, (-200, 0))

        if win == "stalemate" or win == "draw":
            text = "Draw"
        else:
            text = f"{win} won!"
            text[0].upper()
        text_to_screen(text, 0, -200, (250, 250, 250), 50)
        text_to_screen("That was an epic fight!", 0, -160, (250, 250, 250), 20)

        if mouse_clicked:
            if button_1_pressed:
                s_g = True
            elif button_2_pressed:
                g_e, s_g = title_screen()

        button_1_pressed = button_1.return_if_pressed()

        button_2_pressed = button_2.return_if_pressed()

        button_1.render()
        button_2.render()

        if not g_e:
            pygame.display.update()

        clock.tick(100)

    return g_e, s_g


def title_screen():
    background = pygame.image.load("Sprites/title screen background.png")
    background.set_alpha(128)
    background = pygame.transform.scale(background, (1045, 640))

    g_e = False
    s_g = False

    button_width = 170
    button_height = 50
    button_x = (display_width / 2) - (button_width / 2)
    button_1 = Button((button_x, 300, button_width, button_height), "New game", (160, 219, 142),
                      (255, 255, 255), 3, (130, 189, 112), 5, "Arial", 30)
    button_2 = Button((button_x, 370, button_width, button_height), "Exit game", (174, 0, 0),
                      (255, 255, 255), 3, (144, 0, 0), 5, "Arial", 30)

    button_1_pressed = False
    button_2_pressed = False

    while not g_e and not s_g:

        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g_e = True

            if event.type == 1026:  # event 1026 -- mouse button up, cuz pygame.KEYUP not working
                mouse_clicked = True

        display.fill((0, 0, 0))
        display.blit(background, (-200, 0))

        if mouse_clicked:
            if button_1_pressed:
                s_g = True
            if button_2_pressed:
                g_e = True

        button_1_pressed = button_1.return_if_pressed()

        button_2_pressed = button_2.return_if_pressed()

        button_1.render()
        button_2.render()

        pygame.display.update()

        clock.tick(100)

    return g_e, s_g


game_exit, start_game = title_screen()
while not game_exit:
    if start_game:
        game_over, winner, game_exit = main_loop()
        start_game = False
    else:
        winner = None

    game_exit, start_game = post_game_screen(winner, game_exit, start_game)
