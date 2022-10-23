import pygame


class Piece:
    def __init__(self, color: str, piece_type: str):
        self.color = color
        self.type = piece_type
        self.image_path = f"Sprites/{color} {piece_type}.png"
        self.image = pygame.image.load(self.image_path)
        self.move_count = 0
        if self.type == "pawn":
            self.en_passant = False

    def copy(self):
        return Piece(self.color, self.type)


# b -- board, selected_p -- selected_piece, p_pos -- piece_pos, n -- number_of_repeats
def possible_moves(b, selected_p, p_pos, n=0):
    pos_moves = []  # pos_moves -- possible_moves
    if selected_p.type == "king":
        pos_moves = [(p_pos[0], p_pos[1] - 1), (p_pos[0] + 1, p_pos[1] - 1), (p_pos[0] + 1, p_pos[1]),
                     (p_pos[0] + 1, p_pos[1] + 1), (p_pos[0], p_pos[1] + 1), (p_pos[0] - 1, p_pos[1] + 1),
                     (p_pos[0] - 1, p_pos[1]), (p_pos[0] - 1, p_pos[1] - 1)]

        if selected_p.move_count == 0:
            if b[p_pos[1]][p_pos[0] + 3] != "'":
                if b[p_pos[1]][p_pos[0] + 3].type == "rook":
                    if b[p_pos[1]][p_pos[0] + 3].move_count == 0:
                        if b[p_pos[1]][p_pos[0] + 1] == "'" and b[p_pos[1]][p_pos[0] + 2] == "'":
                            cell_under_attack = check_around_for_pieces(b, selected_p.color, (p_pos[0] + 1, p_pos[1]))
                            king_in_check = check_around_for_pieces(b, selected_p.color, (p_pos[0], p_pos[1]))
                            if not cell_under_attack and not king_in_check:
                                pos_moves.append((p_pos[0] + 2, p_pos[1]))

            if b[p_pos[1]][p_pos[0] - 4] != "'":
                if b[p_pos[1]][p_pos[0] - 4].type == "rook":
                    if b[p_pos[1]][p_pos[0] - 4].move_count == 0:
                        if b[p_pos[1]][p_pos[0] - 3] == "'" and b[p_pos[1]][p_pos[0] - 2] == "'" and \
                                b[p_pos[1]][p_pos[0] - 1] == "'":

                            cell_under_attack = check_around_for_pieces(b, selected_p.color,
                                                                        (p_pos[0] - 1, p_pos[1]))
                            king_in_check = check_around_for_pieces(b, selected_p.color, (p_pos[0], p_pos[1]))
                            if not cell_under_attack and not king_in_check:
                                pos_moves.append((p_pos[0] - 2, p_pos[1]))
    elif selected_p.type == "knight":
        pos_moves = [(p_pos[0] - 1, p_pos[1] - 2), (p_pos[0] + 1, p_pos[1] - 2), (p_pos[0] + 2, p_pos[1] - 1),
                     (p_pos[0] + 2, p_pos[1] + 1), (p_pos[0] + 1, p_pos[1] + 2), (p_pos[0] - 1, p_pos[1] + 2),
                     (p_pos[0] - 2, p_pos[1] + 1), (p_pos[0] - 2, p_pos[1] - 1)]

    elif selected_p.type == "rook":
        i = 1
        try:
            while b[p_pos[1]][p_pos[0] + i] == "'" and p_pos[0] + i < 8:
                pos_moves.append((p_pos[0] + i, p_pos[1]))
                i += 1

            if b[p_pos[1]][p_pos[0] + i] != "'" and p_pos[0] + i < 8:
                if b[p_pos[1]][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1]))

        except IndexError:
            pass

        i = 1
        try:
            while b[p_pos[1] + i][p_pos[0]] == "'" and p_pos[1] + i < 8:
                pos_moves.append((p_pos[0], p_pos[1] + i))
                i += 1

            if b[p_pos[1] + i][p_pos[0]] != "'" and p_pos[1] + i < 8:
                if b[p_pos[1] + i][p_pos[0]].color != selected_p.color:
                    pos_moves.append((p_pos[0], p_pos[1] + i))

        except IndexError:
            pass

        i = -1
        try:
            while b[p_pos[1]][p_pos[0] + i] == "'" and p_pos[0] + i >= 0:
                pos_moves.append((p_pos[0] + i, p_pos[1]))
                i -= 1

            if b[p_pos[1]][p_pos[0] + i] != "'" and p_pos[0] + i >= 0:
                if b[p_pos[1]][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1]))

        except IndexError:
            pass

        i = -1
        try:
            while b[p_pos[1] + i][p_pos[0]] == "'" and p_pos[1] + i >= 0:
                pos_moves.append((p_pos[0], p_pos[1] + i))
                i -= 1

            if b[p_pos[1] + i][p_pos[0]] != "'" and p_pos[1] + i >= 0:
                if b[p_pos[1] + i][p_pos[0]].color != selected_p.color:
                    pos_moves.append((p_pos[0], p_pos[1] + i))

        except IndexError:
            pass

    elif selected_p.type == "bishop":
        i = 1
        j = 1

        try:
            while b[p_pos[1] + j][p_pos[0] + i] == "'" and p_pos[0] + i < 8 and p_pos[1] + j < 8:
                pos_moves.append((p_pos[0] + i, p_pos[1] + j))
                i += 1
                j += 1

            if b[p_pos[1] + j][p_pos[0] + i] != "'" and p_pos[0] + i < 8 and p_pos[1] + j < 8:
                if b[p_pos[1] + j][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1] + j))

        except IndexError:
            pass

        i = -1
        j = 1

        try:
            while b[p_pos[1] + j][p_pos[0] + i] == "'" and p_pos[0] + i >= 0 and p_pos[1] + j < 8:
                pos_moves.append((p_pos[0] + i, p_pos[1] + j))
                i -= 1
                j += 1

            if b[p_pos[1] + j][p_pos[0] + i] != "'" and p_pos[0] + i >= 0 and p_pos[1] + j < 8:
                if b[p_pos[1] + j][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1] + j))

        except IndexError:
            pass

        i = 1
        j = -1

        try:
            while b[p_pos[1] + j][p_pos[0] + i] == "'" and p_pos[0] + i < 8 and p_pos[1] + j >= 0:
                pos_moves.append((p_pos[0] + i, p_pos[1] + j))
                i += 1
                j -= 1

            if b[p_pos[1] + j][p_pos[0] + i] != "'" and p_pos[0] + i < 8 and p_pos[1] + j >= 0:
                if b[p_pos[1] + j][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1] + j))

        except IndexError:
            pass

        i = -1
        j = -1

        try:
            while b[p_pos[1] + j][p_pos[0] + i] == "'" and p_pos[0] + i >= 0 and p_pos[1] + j >= 0:
                pos_moves.append((p_pos[0] + i, p_pos[1] + j))
                i -= 1
                j -= 1

            if b[p_pos[1] + j][p_pos[0] + i] != "'" and p_pos[0] + i >= 0 and p_pos[1] + j >= 0:
                if b[p_pos[1] + j][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1] + j))

        except IndexError:
            pass

    elif selected_p.type == "queen":
        i = 1
        try:
            while b[p_pos[1]][p_pos[0] + i] == "'" and p_pos[0] + i < 8:
                pos_moves.append((p_pos[0] + i, p_pos[1]))
                i += 1

            if b[p_pos[1]][p_pos[0] + i] != "'" and p_pos[0] + i < 8:
                if b[p_pos[1]][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1]))

        except IndexError:
            pass

        i = 1
        try:
            while b[p_pos[1] + i][p_pos[0]] == "'" and p_pos[1] + i < 8:
                pos_moves.append((p_pos[0], p_pos[1] + i))
                i += 1

            if b[p_pos[1] + i][p_pos[0]] != "'" and p_pos[1] + i < 8:
                if b[p_pos[1] + i][p_pos[0]].color != selected_p.color:
                    pos_moves.append((p_pos[0], p_pos[1] + i))

        except IndexError:
            pass

        i = -1
        try:
            while b[p_pos[1]][p_pos[0] + i] == "'" and p_pos[0] + i >= 0:
                pos_moves.append((p_pos[0] + i, p_pos[1]))
                i -= 1

            if b[p_pos[1]][p_pos[0] + i] != "'" and p_pos[0] + i >= 0:
                if b[p_pos[1]][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1]))

        except IndexError:
            pass

        i = -1
        try:
            while b[p_pos[1] + i][p_pos[0]] == "'" and p_pos[1] + i >= 0:
                pos_moves.append((p_pos[0], p_pos[1] + i))
                i -= 1

            if b[p_pos[1] + i][p_pos[0]] != "'" and p_pos[1] + i >= 0:
                if b[p_pos[1] + i][p_pos[0]].color != selected_p.color:
                    pos_moves.append((p_pos[0], p_pos[1] + i))

        except IndexError:
            pass

        i = 1
        j = 1

        try:
            while b[p_pos[1] + j][p_pos[0] + i] == "'" and p_pos[0] + i < 8 and p_pos[1] + j < 8:
                pos_moves.append((p_pos[0] + i, p_pos[1] + j))
                i += 1
                j += 1

            if b[p_pos[1] + j][p_pos[0] + i] != "'" and p_pos[0] + i < 8 and p_pos[1] + j < 8:
                if b[p_pos[1] + j][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1] + j))

        except IndexError:
            pass

        i = -1
        j = 1

        try:
            while b[p_pos[1] + j][p_pos[0] + i] == "'" and p_pos[0] + i >= 0 and p_pos[1] + j < 8:
                pos_moves.append((p_pos[0] + i, p_pos[1] + j))
                i -= 1
                j += 1

            if b[p_pos[1] + j][p_pos[0] + i] != "'" and p_pos[0] + i >= 0 and p_pos[1] + j < 8:
                if b[p_pos[1] + j][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1] + j))

        except IndexError:
            pass

        i = 1
        j = -1

        try:
            while b[p_pos[1] + j][p_pos[0] + i] == "'" and p_pos[0] + i < 8 and p_pos[1] + j >= 0:
                pos_moves.append((p_pos[0] + i, p_pos[1] + j))
                i += 1
                j -= 1

            if b[p_pos[1] + j][p_pos[0] + i] != "'" and p_pos[0] + i < 8 and p_pos[1] + j >= 0:
                if b[p_pos[1] + j][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1] + j))

        except IndexError:
            pass

        i = -1
        j = -1

        try:
            while b[p_pos[1] + j][p_pos[0] + i] == "'" and p_pos[0] + i >= 0 and p_pos[1] + j >= 0:
                pos_moves.append((p_pos[0] + i, p_pos[1] + j))
                i -= 1
                j -= 1

            if b[p_pos[1] + j][p_pos[0] + i] != "'" and p_pos[0] + i >= 0 and p_pos[1] + j >= 0:
                if b[p_pos[1] + j][p_pos[0] + i].color != selected_p.color:
                    pos_moves.append((p_pos[0] + i, p_pos[1] + j))

        except IndexError:
            pass

    elif selected_p.type == "pawn":
        if selected_p.color == "black":

            try:
                if b[p_pos[1]][p_pos[0] - 1].en_passant:
                    pos_moves.append((p_pos[0] - 1, p_pos[1] + 1))

            except (AttributeError, IndexError):
                pass

            try:
                if b[p_pos[1]][p_pos[0] + 1].en_passant:
                    pos_moves.append((p_pos[0] + 1, p_pos[1] + 1))

            except (AttributeError, IndexError):
                pass

            try:
                if b[p_pos[1] + 1][p_pos[0]] == "'":
                    pos_moves.append((p_pos[0], p_pos[1] + 1))

            except IndexError:
                pass

            try:
                if p_pos[1] == 1 and b[p_pos[1] + 2][p_pos[0]] == "'" and b[p_pos[1] + 1][p_pos[0]] == "'":
                    pos_moves.append((p_pos[0], p_pos[1] + 2))
            except IndexError:
                pass

            try:
                if b[p_pos[1] + 1][p_pos[0] + 1] != "'":
                    pos_moves.append((p_pos[0] + 1, p_pos[1] + 1))

            except IndexError:
                pass

            try:
                if b[p_pos[1] + 1][p_pos[0] - 1] != "'":
                    pos_moves.append((p_pos[0] - 1, p_pos[1] + 1))

            except IndexError:
                pass

        elif selected_p.color == "white":

            try:
                if b[p_pos[1]][p_pos[0] - 1].en_passant:
                    pos_moves.append((p_pos[0] - 1, p_pos[1] - 1))

            except (IndexError, AttributeError):
                pass

            try:
                if b[p_pos[1]][p_pos[0] + 1].en_passant:
                    pos_moves.append((p_pos[0] + 1, p_pos[1] - 1))

            except (IndexError, AttributeError):
                pass

            try:
                if b[p_pos[1] - 1][p_pos[0]] == "'":
                    pos_moves.append((p_pos[0], p_pos[1] - 1))

            except IndexError:
                pass

            try:
                if p_pos[1] == 6 and b[p_pos[1] - 2][p_pos[0]] == "'" and b[p_pos[1] - 1][p_pos[0]] == "'":
                    pos_moves.append((p_pos[0], p_pos[1] - 2))
            except IndexError:
                pass

            try:
                if b[p_pos[1] - 1][p_pos[0] + 1] != "'":
                    pos_moves.append((p_pos[0] + 1, p_pos[1] - 1))

            except IndexError:
                pass

            try:
                if b[p_pos[1] - 1][p_pos[0] - 1] != "'":
                    pos_moves.append((p_pos[0] - 1, p_pos[1] - 1))

            except IndexError:
                pass

    pos_moves = check_for_possibility(b, pos_moves, selected_p, p_pos, n)
    return pos_moves


# b -- board, l_of_moves -- list_of_moves, p_pos -- piece_pos, n -- number of repeats
def check_for_possibility(b, l_of_moves, selected_p, p_pos, n=0):
    new_l_of_moves = []

    king_pos = None
    if selected_p != "king":
        king_pos = return_king_pos(b, selected_p.color)

    for move in l_of_moves:
        try:
            if move[0] >= 0 <= move[1]:
                if b[move[1]][move[0]] == "'" or b[move[1]][move[0]].color != selected_p.color:
                    if n == 0:
                        new_b = simulate_move(b, move, p_pos, selected_p)

                        if selected_p.type == "king":
                            king_pos = move

                        king_in_check = check_around_for_pieces(new_b, selected_p.color, king_pos)

                        if not king_in_check:
                            new_l_of_moves.append(move)

                    else:
                        new_l_of_moves.append(move)

        except (IndexError, AttributeError):
            pass

    return new_l_of_moves


def simulate_move(b, move, p_pos, selected_p):  # b -- board, p_pos -- piece_position
    new_b = []
    for row in b:
        new_row = []
        for cell in row:
            if cell != "'":
                new_row.append(cell.copy())
            else:
                new_row.append("'")

        new_b.append(new_row)

    new_b[p_pos[1]][p_pos[0]] = "'"
    new_b[move[1]][move[0]] = selected_p

    # if the move is en-passant
    if selected_p.type == "pawn":
        if p_pos[0] != move[0] and b[move[1]][move[0]] == "'":
            new_b[p_pos[1]][move[0]] = "'"

    # if the move is castling
    if selected_p.type == "king":
        if p_pos[0] - move[0] == 2:
            new_b[p_pos[1]][move[0] + 1] = new_b[p_pos[1]][0]
            new_b[p_pos[1]][0] = "'"

        elif p_pos[0] - move[0] == -2:
            new_b[p_pos[1]][move[0] - 1] = new_b[p_pos[1]][7]
            new_b[p_pos[1]][7] = "'"

    return new_b


def return_king_pos(b, color):
    king_pos = None
    for row_counter, row in enumerate(b):
        for cell_counter, piece in enumerate(row):
            if piece != "'":
                if piece.type == "king" and piece.color == color:
                    king_pos = (cell_counter, row_counter)

    return king_pos


def return_enemies_moves(b, friend_color, n):
    enemies_moves = []
    for row_counter, row in enumerate(b):
        for cell_counter, piece in enumerate(row):
            if piece != "'":
                if piece.color != friend_color:
                    moves = possible_moves(b, piece, (cell_counter, row_counter), n)
                    for move in moves:
                        enemies_moves.append(move)

    return enemies_moves


def check_around_for_pieces(b, color, p_pos):  # b -- board
    piece_under_attack = False

    # check for pawns
    direction_to_check = -1 if color == "white" else 1
    enemy_piece_pos_to_check = [(p_pos[0] - 1, p_pos[1] + direction_to_check),
                                (p_pos[0] + 1, p_pos[1] + direction_to_check)]

    for enemy_pos in enemy_piece_pos_to_check:
        if enemy_pos[0] >= 0 <= enemy_pos[1]:
            try:
                if b[enemy_pos[1]][enemy_pos[0]].type == "pawn" and b[enemy_pos[1]][enemy_pos[0]].color != color:
                    piece_under_attack = True
            except (IndexError, AttributeError):
                pass

    if not piece_under_attack:
        enemy_piece_pos_to_check = [(p_pos[0] - 1, p_pos[1] - 2), (p_pos[0] + 1, p_pos[1] - 2),
                                    (p_pos[0] + 2, p_pos[1] - 1), (p_pos[0] + 2, p_pos[1] + 1),
                                    (p_pos[0] + 1, p_pos[1] + 2), (p_pos[0] - 1, p_pos[1] + 2),
                                    (p_pos[0] - 2, p_pos[1] + 1), (p_pos[0] - 2, p_pos[1] - 1)]

        for enemy_pos in enemy_piece_pos_to_check:
            if enemy_pos[0] >= 0 <= enemy_pos[1]:
                try:
                    if b[enemy_pos[1]][enemy_pos[0]].type == "knight" and b[enemy_pos[1]][enemy_pos[0]].color != color:
                        piece_under_attack = True
                except (IndexError, AttributeError):
                    pass

    if not piece_under_attack:
        enemy_piece_pos_to_check = [(p_pos[0] + 1, p_pos[1]), (p_pos[0] + 1, p_pos[1] + 1), (p_pos[0], p_pos[1] + 1),
                                    (p_pos[0] - 1, p_pos[1] + 1), (p_pos[0] - 1, p_pos[1]),
                                    (p_pos[0] - 1, p_pos[1] - 1),
                                    (p_pos[0], p_pos[1] - 1), (p_pos[0] + 1, p_pos[1] - 1)]

        for enemy_pos in enemy_piece_pos_to_check:
            if enemy_pos[0] >= 0 <= enemy_pos[1]:
                try:
                    if b[enemy_pos[1]][enemy_pos[0]].type == "king" and b[enemy_pos[1]][enemy_pos[0]].color != color:
                        piece_under_attack = True
                except (IndexError, AttributeError):
                    pass

    if not piece_under_attack:
        append_stages = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for i, j in append_stages:
            if not piece_under_attack:

                while 8 > p_pos[0] + i >= 0 and 8 > p_pos[1] + j >= 0:
                    if b[p_pos[1] + j][p_pos[0] + i] != "'":
                        if (b[p_pos[1] + j][p_pos[0] + i].type == "rook" or
                            b[p_pos[1] + j][p_pos[0] + i].type == "queen") and \
                                b[p_pos[1] + j][p_pos[0] + i].color != color:
                            piece_under_attack = True

                        else:
                            break

                    i += int(i / abs(i)) if i != 0 else 0
                    j += int(j / abs(j)) if j != 0 else 0

            else:
                break

    if not piece_under_attack:
        append_stages = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for i, j in append_stages:
            if not piece_under_attack:

                while 8 > p_pos[0] + i >= 0 and 8 > p_pos[1] + j >= 0:
                    if b[p_pos[1] + j][p_pos[0] + i] != "'":
                        if (b[p_pos[1] + j][p_pos[0] + i].type == "bishop" or
                            b[p_pos[1] + j][p_pos[0] + i].type == "queen") and \
                                b[p_pos[1] + j][p_pos[0] + i].color != color:
                            piece_under_attack = True

                        else:
                            break

                    i += int(i / abs(i))
                    j += int(j / abs(j))

            else:
                break

    return piece_under_attack


def print_check_mate(b, winner, p_to_move, king_pos):
    if winner is None:
        piece_under_attack = check_around_for_pieces(b, p_to_move, king_pos)

        having_pos_moves = False

        for row_counter, row in enumerate(b):
            for cell_counter, piece in enumerate(row):
                if piece != "'" and not having_pos_moves:
                    if piece.color == p_to_move:
                        if len(possible_moves(b, piece, (cell_counter, row_counter))) > 0:
                            having_pos_moves = True

        if piece_under_attack and not having_pos_moves:
            winner = "black" if p_to_move == "white" else "white"

        elif not piece_under_attack and not having_pos_moves:
            winner = "stalemate"

    else:
        return winner, True

    return winner, piece_under_attack
