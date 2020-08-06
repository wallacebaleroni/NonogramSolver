import copy

lines = [[3, 1], [3, 1], [0], [0], [0]]
columns = [[0], [0], [0], [0], [0]]

start_board = [['.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.']]


def fits(board, value, i, j):
    if i >= len(lines):
        return False
    if j >= len(columns):
        return False
    if len(lines) - j < value:
        return False
    if board[i][j] == 'X':
        return False
    if board[i][j] == 'O':
        return False
    if board[i][j] == '.':
        if value == 1:
            return True
        else:
            return fits(board, value-1, i, j+1)


def fill(board, value, i, j):
    board = copy.deepcopy(board)
    for k in range(value):
        board[i][j+k] = 'O'
    if j > 0:
        board[i][j-1] = 'X'
    if j+value < len(columns):
        board[i][j+value] = 'X'
    return board


def is_solution(board, line_values):
    sequence_size = 0
    values = line_values[:]
    for j in range(len(lines)):
        if board[0][j] == 'O':
            sequence_size += 1
        else:
            if values[0] == sequence_size:
                sequence_size = 0
                values.pop(0)
                if len(values) == 0:
                    return True
    if values[0] == sequence_size:
        values.pop(0)
        if len(values) == 0:
            return True
    return False


def evaluate(board, k_0, j_0):
    if is_solution(board, lines[0]):
        print(board)
    if k_0 > len(lines[0]) - 1:
        return
    for j in range(j_0, len(columns)):
        if fits(board, lines[0][k_0], 0, j):
            evaluate(fill(board, lines[0][k_0], 0, j), k_0+1, j)


evaluate(start_board, 0, 0)
