import copy

MARKED = 'O'
UNMARKED = 'X'
CLEAR = '.'

rows = [[4],[4],[5],[3,4],[1,1,4],[1,4],[1,6],[2,4,1],[7],[7]]
columns = [[5,1],[1,3],[2,2],[2,2],[3,4],[4,5],[10],[7],[5],[1,2]]

board = [[CLEAR for x in range(len(columns))] for y in range(len(rows))]


def increment_heat(line_heat, line):
    for i in range(len(line)):
        if line[i] == MARKED:
            line_heat[i] += 1
    return line_heat


def is_line_solution(line, original_values):
    sequence_size = 0
    values = []

    for i in range(len(line)):
        if line[i] == MARKED:
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


def fill_value_in_line(original_line, value, j):
    line = copy.deepcopy(original_line)
    for k in range(value):
        line[j + k] = MARKED
    if j > 0:
        line[j - 1] = UNMARKED
    if j + value < len(columns):
        line[j + value] = UNMARKED
    return line


def value_fits_in_line(line, value, j):
    if j >= len(line):
        return False
    if len(rows) - j < value:
        return False
    if line[j] == UNMARKED:
        return False
    else:
        if value == 1:
            if j == len(line) - 1:
                return True
            else:
                if line[j + 1] == MARKED:
                    return False
                else:
                    return True
        else:
            return value_fits_in_line(line, value - 1, j + 1)


def evaluate_line_recursive(line_heat, solutions, line, values, j_0, k):
    if is_line_solution(line, values):
        solutions += 1
        line_heat = increment_heat(line_heat, line)
        return line_heat, solutions
    if k > len(values) - 1:
        return line_heat, solutions
    for j in range(j_0, len(line)):
        if value_fits_in_line(line, values[k], j):
            line_heat, solutions = evaluate_line_recursive(line_heat, solutions, fill_value_in_line(line, values[k], j), values, j + values[k] + 1, k + 1)
    return line_heat, solutions


def evaluate_line(line_heat, solutions, line, values):
    for j in range(len(line)):
        line_heat, solutions = evaluate_line_recursive(line_heat, solutions, line, values, j, 0)
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

        for i in range(len(rows)):
            row_heat = len(board[i]) * [0]
            solutions = 0
            row_heat, solutions = evaluate_line(row_heat, solutions, board[i], rows[i])
            for k in range(len(row_heat)):
                if row_heat[k] == solutions:
                    if board[i][k] == CLEAR:
                        board[i][k] = MARKED
                        changed = True
                elif row_heat[k] == 0:
                    if board[i][k] == CLEAR:
                        board[i][k] = UNMARKED
                        changed = True

        for j in range(len(columns)):
            column_heat = len(board) * [0]
            solutions = 0
            column_heat, solutions = evaluate_line(column_heat, solutions, get_column(board, j), columns[j])
            for k in range(len(column_heat)):
                if column_heat[k] == solutions:
                    if board[k][j] == CLEAR:
                        board[k][j] = MARKED
                        changed = True
                elif column_heat[k] == 0:
                    if board[k][j] == CLEAR:
                        board[k][j] = UNMARKED
                        changed = True

    print("Loops necessary: " + str(loops_counter))
    for i in range(len(rows)):
        for j in range(len(columns)):
            if board[i][j] == MARKED:
                print(' O ', end='')
            if board[i][j] == UNMARKED:
                print(' . ', end='')
            if board[i][j] == CLEAR:
                print(' . ', end='')
        print('', end='\n')


main()
