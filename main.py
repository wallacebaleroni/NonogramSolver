import copy

lines = [[5], [4], [3,3], [7,2], [8,2], [2,3,5], [10], [9,5], [11,3], [3,3,3,3],[2,5,3,2],[2,2,5,1],[1,2,2,3],[2,3,3],[3,2,2],[2,2,2],[2,1],[3],[3],[3]]
columns = [[1],[3],[2,3], [3, 5], [3,3,3], [1, 3, 2,6], [1, 2, 2, 8], [2,3,2,5], [2, 8], [3,6,1],[4,5,3],[7,5],[5,3],[2,4],[3,5,2],[3,6],[3,3],[4],[5],[2]]

start_board = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]


def increment_heat(line_heat, line):
    for i in range(len(line)):
        if line[i] == 'O':
            line_heat[i] += 1
    return line_heat


def is_solution_line(line, original_values):
    sequence_size = 0
    values = []

    for i in range(len(line)):
        if line[i] == 'O':
            sequence_size += 1
        else:
            if sequence_size > 0:
                values.append(sequence_size)
                sequence_size = 0
    if sequence_size > 0:
        values.append(sequence_size)

    if len(values) != len(original_values):
        return False

    for i in range(len(values)):
        if values[i] != original_values[i]:
            return False

    return True


def fill_line(original_line, value, j):
    line = copy.deepcopy(original_line)
    for k in range(value):
        line[j + k] = 'O'
    if j > 0:
        line[j - 1] = 'X'
    if j + value < len(columns):
        line[j + value] = 'X'
    return line


def fits_line(line, value, j):
    if j >= len(line):
        return False
    if len(lines) - j < value:
        return False
    if line[j] == 'X':
        return False
    else:
        if value == 1:
            if j == len(line) - 1:
                return True
            else:
                if line[j + 1] == 'O':
                    return False
                else:
                    return True
        else:
            return fits_line(line, value - 1, j + 1)


def evaluate_line_rec(line_heat, solutions, line, values, j_0, k):
    if is_solution_line(line, values):
        solutions += 1
        line_heat = increment_heat(line_heat, line)
        return line_heat, solutions
    if k > len(values) - 1:
        return line_heat, solutions
    for j in range(j_0, len(line)):
        if fits_line(line, values[k], j):
            line_heat, solutions = evaluate_line_rec(line_heat, solutions, fill_line(line, values[k], j), values, j + values[k] + 1, k + 1)
    return line_heat, solutions


def evaluate_line(line_heat, solutions, line, values):
    for j in range(len(line)):
        line_heat, solutions = evaluate_line_rec(line_heat, solutions, line, values, j, 0)
    return line_heat, solutions


def get_column(board, j):
    column = []
    for i in range(len(board)):
        column.append(board[i][j])
    return column


def main():
    changed = True
    loops_counter = 0
    while changed:
        changed = False
        loops_counter += 1

        for i in range(len(start_board)):
            line_heat = len(start_board[i]) * [0]
            solutions = 0
            line_heat, solutions = evaluate_line(line_heat, solutions, start_board[i], lines[i])
            for k in range(len(line_heat)):
                if line_heat[k] == solutions:
                    if start_board[i][k] == '.':
                        start_board[i][k] = 'O'
                        changed = True
                elif line_heat[k] == 0:
                    if start_board[i][k] == '.':
                        start_board[i][k] = 'X'
                        changed = True

        for j in range(len(start_board[0])):
            column_heat = len(start_board) * [0]
            solutions = 0
            column_heat, solutions = evaluate_line(column_heat, solutions, get_column(start_board, j), columns[j])
            for k in range(len(column_heat)):
                if column_heat[k] == solutions:
                    if start_board[k][j] == '.':
                        start_board[k][j] = 'O'
                        changed = True
                elif column_heat[k] == 0:
                    if start_board[k][j] == '.':
                        start_board[k][j] = 'X'
                        changed = True

    print(loops_counter)
    for i in range(len(start_board)):
        print(start_board[i])


main()
