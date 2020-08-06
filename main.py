lines = [[3], [3], [0], [0], [0]]
columns = [[0], [0], [0], [0], [0]]

board = [['.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.']]


def is_solved():
    return False


def try_to_fill_line(i):
    minimum_filling = sum(lines[i]) + (len(lines[i]) - 1)
    if minimum_filling <= len(columns)//2:
        return False
    if len(lines[i]) == 1:
        padding = len(columns) - lines[i][0]
        start = padding
        end = len(columns) - padding - 1
        for j in range(start, end + 1):
            board[i][j] = 'O'
        return True
    return False


altered = True
while altered:
    altered = False
    for i in range(len(lines)):
        altered = try_to_fill_line(i)
    # para cada coluna
        # tentar preencher
    print(board)
