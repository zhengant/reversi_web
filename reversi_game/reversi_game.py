import sys

import numpy as np

WHITE: int = 1
BLACK: int = -1
EMPTY: int = 0


def get_move(idx) -> tuple:
    row = idx // 8
    col = idx % 8

    return row, col


def str2board(board_str):
    board = np.zeros((8,8))
    for i, c in enumerate(board_str):
        value = EMPTY
        if c == 'B':
            value = BLACK
        elif c == 'W':
            value = WHITE

        row, col = get_move(i)
        board[row, col] = value

    return board


def board2str(board):
    result = ''
    for row in range(8):
        for col in range(8):
            if board[row, col] == EMPTY:
                result += '0'
            elif board[row, col] == BLACK:
                result += 'B'
            else:
                result += 'W'

    return result


def print_board(board: np.ndarray) -> None:
    """
    prints out the reversi board specified by board
    :param board: 8x8 numpy int array, where 1 indicates a white piece, -1 a black piece, and 0 an empty square
    :return: void
    """
    sys.stdout.write('  01234567\n')
    for i in range(8):
        sys.stdout.write(str(i) + ' ')
        for j in range(8):
            if board[i, j] == EMPTY:
                sys.stdout.write('-')
            elif board[i, j] == WHITE:
                sys.stdout.write('O')
            elif board[i, j] == BLACK:
                sys.stdout.write('X')
        sys.stdout.write('\n')

    sys.stdout.write('\n')


def make_move(board: np.ndarray, row: int, col: int, turn: int, mod: bool) -> bool:
    """
    makes or checks the specified move on the board specified
    if mod is true, the move is made and the board is modified based on the move
    if mod is false, the move is not actually made and the board is not modified
    in both cases, the legality of the move is returned (false if the move was not legal)
    :param board: 8x8 numpy int array. 1 is white, -1 is black, 0 is empty
    :param row: zero-indexed row for the move
    :param col: zero=indexed column for the move
    :param turn: 1 if it is white's turn to move, -1 if it is black's turn to move
    :param mod: whether or not to modify the board
    :return: true or false, whether or not the move was legal
    """

    if row >= 8 or col >= 8 or row < 0 or col < 0:
        return False
    if board[row, col] != EMPTY:
        return False

    legal = False

    # flip downward pieces
    for i in range(row + 1, 8):
        # matching piece on other end
        if board[i, col] == turn:
            # retrace back
            if mod:
                for j in range(i - 1, row, -1):
                    board[j, col] = turn

            # legal if made it past the first one
            if i > row + 1:
                legal = True
            break

        elif board[i, col] == EMPTY:
            break

    # flip upward pieces
    for i in range(row - 1, -1, -1):
        if board[i, col] == turn:
            if mod:
                for j in range(i + 1, row):
                    board[j, col] = turn

            if i < row - 1:
                legal = True
            break

        elif board[i, col] == EMPTY:
            break

    # flip leftward pieces
    for i in range(col - 1, -1, -1):
        if board[row, i] == turn:
            if mod:
                for j in range(i + 1, col):
                    board[row, j] = turn

            if i < col - 1:
                legal = True
            break

        elif board[row, i] == EMPTY:
            break

    # flip rightward pieces
    for i in range(col + 1, 8):
        if board[row, i] == turn:
            if mod:
                for j in range(i - 1, col, -1):
                    board[row, j] = turn

            if i > col + 1:
                legal = True
            break

        elif board[row, i] == EMPTY:
            break

    # flip northwest diagonal pieces
    # i = 1; i <= min(row, col); i++
    for i in range(1, min(row, col) + 1):
        if board[row - i, col - i] == turn:
            if mod:
                for j in range(i - 1, 0, -1):
                    board[row - j, col - j] = turn

            if i > 1:
                legal = True
            break
        elif board[row - i, col - i] == EMPTY:
            break

    # flip northeast diagonal pieces
    # i = 1; i <= min(row, 7-col); i++
    for i in range(1, min(row, 7-col) + 1):
        if board[row - i, col + i] == turn:
            if mod:
                for j in range(i - 1, 0, -1):
                    board[row - j, col + j] = turn

            if i > 1:
                legal = True
            break

        elif board[row - i, col + i] == EMPTY:
            break

    # flip southwest diagonal pieces
    for i in range(1, min(7 - row, col) + 1):
        if board[row + i, col - i] == turn:
            if mod:
                for j in range(i - 1, 0, -1):
                    board[row + j, col - j] = turn

            if i > 1:
                legal = True
            break
        elif board[row + i, col - i] == EMPTY:
            break

    # flip southeast diagonal pieces
    for i in range(1, min(7 - row, 7 - col) + 1):
        if board[row + i, col + i] == turn:
            if mod:
                for j in range(i - 1, 0, -1):
                    board[row + j, col + j] = turn

            if i > 1:
                legal = True
            break
        elif board[row + i, col + i] == EMPTY:
            break

    if mod and legal:
        board[row, col] = turn

    return legal


def check_moves(board: np.ndarray, turn: int) -> bool:
    """
    Checks if turn has any valid moves
    :param board: 8x8 numpy int array. 0 is empty, 1 is white, -1 is black
    :param turn: 1 for white, -1 for black
    :return: whether or not the given turn has any valid moves
    """
    for i in range(8):
        for j in range(8):
            if make_move(board, i, j, turn, False):
                return True
    return False


def check_winner(board: np.ndarray) -> tuple:
    """
    Checks if the game is over or not
    :param board: 8x8 numpy int array. 0 is empty, 1 is white, -1 is black
    :return: 1 if white has won, -1 if black has won, 0 if the game is still active, 2 if the game was a draw
    """
    white_count: int = 0
    black_count: int = 0
    for i in range(8):
        for j in range(8):
            if board[i, j] == WHITE:
                white_count += 1
            elif board[i, j] == BLACK:
                black_count += 1
            elif make_move(board, i, j, WHITE, False):
                return 0, white_count, black_count
            elif make_move(board, i, j, BLACK, False):
                return 0, white_count, black_count

    if white_count > black_count:
        return WHITE, white_count, black_count
    elif black_count > white_count:
        return BLACK, white_count, black_count
    else:
        return 2, white_count, black_count


def count_pieces(board: np.ndarray) -> tuple:
    black_count = 0
    white_count = 0

    for i in range(8):
        for j in range(8):
            if board[i, j] == BLACK:
                black_count += 1
            elif board[i, j] == WHITE:
                white_count += 1

    return black_count, white_count


def reset_board(board: np.ndarray) -> None:
    """
    Resets the given board to its starting state
    :param board: 8x8 numpy int array. 0 is empty, 1 is white, -1 is black
    :return: void
    """
    for i in range(8):
        for j in range(8):
            board[i, j] = EMPTY

    board[3, 3] = WHITE
    board[3, 4] = BLACK
    board[4, 3] = BLACK
    board[4, 4] = WHITE
