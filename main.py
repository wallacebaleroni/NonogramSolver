# lines = [[3], [3], [0], [0], [0]]
# columns = [[0], [0], [0], [0], [0]]
#
# board = [['.', '.', '.', '.', '.'],
#          ['.', '.', '.', '.', '.'],
#          ['.', '.', '.', '.', '.'],
#          ['.', '.', '.', '.', '.'],
#          ['.', '.', '.', '.', '.']]
#
#
# def is_solved():
#     return False
#
#
# def try_to_fill_line(i):
#     minimum_filling = sum(lines[i]) + (len(lines[i]) - 1)
#     if minimum_filling <= len(columns)//2:
#         return False
#     if len(lines[i]) == 1:
#         padding = len(columns) - lines[i][0]
#         start = padding
#         end = len(columns) - padding - 1
#         for j in range(start, end + 1):
#             board[i][j] = 'O'
#         return True
#     return False
#
#
# def evaluate_line_rec(line, k, values):
#     if values[0] == 0:
#         values.pop(0)
#         if len(values) > 0:
#             return evaluate_line_rec(line, k + 1, values)
#         else:
#             print(line)
#             return values
#     else:
#         if board[i][k] != 'X':
#             line[k] += 1
#             values[0] -= 1
#             evaluate_line_rec(line, k + 1, values)
#             line[k] -= 1
#             values[0] += 1
#             evaluate_line_rec(line, k + 1, values)
#         else:
#             return values
#
#
# def evaluate_line(i):
#     line = len(columns) * [0]
#     values = lines[i]
#     k = 0
#     if values[0] > 0:
#         line[k] += 1
#         values[0] -= 1
#         evaluate_line_rec(line, k + 1, values)
#
#
# altered = True
# while altered:
#     altered = False
#     for i in range(len(lines)):
#         altered = try_to_fill_line(i)
#         evaluate_line(i)
#     # para cada coluna
#         # tentar preencher
#     print(board)

#
import copy

lines =   [[2], [2], [6], [4], [1,3], [6,3], [1,3,4], [8,5], [1,3,5], [6,4], [1,3,5]]
columns = [[1], [3], [2,3], [3,5], [3,3,3], [1,3,2,6], [1,2,2,8], [2,3,2,5], [2,8], [3,6,1]]

start_board = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]


def increment_heat(line_heat, line):
    for i in range(len(line)):
        if line[i] == 'O':
            line_heat[i] += 1
    return line_heat


def is_solution_line(line, original_values):
    sequence_size = 0
    values = original_values[:]
    for j in range(len(lines)):
        if line[j] == 'O':
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


def fill_line(original_line, value, j):
    line = copy.deepcopy(original_line)
    for k in range(value):
        line[j+k] = 'O'
    if j > 0:
        line[j-1] = 'X'
    if j+value < len(columns):
        line[j+value] = 'X'
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
            return True
        else:
            return fits_line(line, value-1, j+1)


def evaluate_line_rec(line_heat, solutions, line, values, j_0, k):
    if is_solution_line(line, values):
        solutions += 1
        line_heat = increment_heat(line_heat, line)
        return line_heat, solutions
    if k > len(values) - 1:
        return line_heat, solutions
    for j in range(j_0, len(line)):
        if fits_line(line, values[k], j):
            line_heat, solutions = evaluate_line_rec(line_heat, solutions, fill_line(line, values[k], j), values, j, k+1)
    return line_heat, solutions


def evaluate_line(line_heat, solutions, line, values):
    for j in range(len(line)):
        line_heat, solutions = evaluate_line_rec(line_heat, solutions, line, values, j, 0)
    return line_heat, solutions


def get_column(start_board, j):
    column = []
    for i in range(len(start_board)):
        column.append(start_board[i][j])
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
