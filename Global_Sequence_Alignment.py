# This function converts a string into list of characters
def str2char(string):
    list_char = ['-', '-']
    for i in range(len(string)):
        list_char.append(string[i])
    return list_char


# This function applies the first step in Global Sequence Alignment (Initialization)
def initialization(matrix, first_row, first_col, gap_score):
    matrix[0] = first_row
    for row in range(len(matrix)):
        matrix[row][0] = first_col[row]
    matrix[1][1] = 0
    value = 0
    for i in range(1, len(matrix[0])):
        matrix[1][i] = value
        value += gap_score
    value = 0
    for i in range(1, len(matrix)):
        matrix[i][1] = value
        value += gap_score
    return matrix


# This function fills the matrix based on the max score achieved from Diagonal, Up or Left
def matrix_filling(matrix, scores):
    for row in range(2, len(matrix)):
        for col in range(2, len(matrix[0])):
            if matrix[0][col] == matrix[row][0]:
                s1 = scores['Match'] + matrix[row - 1][col - 1]
            else:
                s1 = scores['Mismatch'] + matrix[row - 1][col - 1]
            s2 = scores['Gap'] + matrix[row - 1][col]
            s3 = scores['Gap'] + matrix[row][col - 1]
            matrix[row][col] = max(s1, s2, s3)
    return matrix


# This function requires the user's inputs and return a filled matrix to be ready for trace back
def global_seq_alignment(seq_1, seq_2, match_score, mismatch_score, gap_score):
    first_row = str2char(seq_1)
    first_col = str2char(seq_2)
    scores = {'Match': match_score, 'Mismatch': mismatch_score, 'Gap': gap_score}
    rows, cols = (len(seq_2) + 2, len(seq_1) + 2)
    matrix = []
    for row in range(rows):
        matrix += [[0] * cols]
    initialized_mat = initialization(matrix, first_row, first_col, scores['Gap'])
    filled_mat = matrix_filling(initialized_mat, scores)
    return filled_mat


# This function performs trace back for the path Recursively
def backtracking(matrix, row, col, match, misMatch, gap, seq1, seq2, cell_path=[], seq1_path=[], seq2_path=[], arrows=[], visited=False):
    if row == 1 or col == 1:
        if matrix[row][col] != 0:
            return
        else:
            print("end cell_path", cell_path)
            seq1_path = seq1_path[::-1]
            seq2_path = seq2_path[::-1]
            print(seq1_path)
            print(arrows)
            print(seq2_path)
            return

    # Check if UP
    if matrix[row][col] - gap == matrix[row - 1][col]:
        cell_path.append(matrix[row][col])
        seq1_path.append(seq1[col - 1])
        seq2_path.append("_")
        arrows.append(" ")
        if visited:
            del cell_path[cell_path.index(matrix[row][col]):len(cell_path) - 1]
            del seq1_path[cell_path.index(matrix[row][col]):len(seq1_path) - 1]
            del seq2_path[cell_path.index(matrix[row][col]):len(seq2_path) - 1]
            del arrows[cell_path.index(matrix[row][col]):len(arrows) - 1]
        backtracking(matrix, row - 1, col, match, misMatch, gap, seq1, seq2, cell_path, seq1_path, seq2_path, arrows, False)
        visited = True

    # Check if Left
    if matrix[row][col] - gap == matrix[row][col - 1]:
        cell_path.append(matrix[row][col])
        seq1_path.append(seq1[col - 2])
        seq2_path.append("_")
        arrows.append(" ")
        if visited:
            del cell_path[cell_path.index(matrix[row][col]):len(cell_path) - 1]
            del seq1_path[cell_path.index(matrix[row][col]):len(seq1_path) - 1]
            del seq2_path[cell_path.index(matrix[row][col]):len(seq2_path) - 1]
            del arrows[cell_path.index(matrix[row][col]):len(arrows) - 1]
        backtracking(matrix, row, col - 1, match, misMatch, gap, seq1, seq2, cell_path, seq1_path, seq2_path, arrows, False)

        visited = True

    # Check Diagonal Match
    if seq1[col - 2] == seq2[row - 2]:
        if matrix[row][col] - match == matrix[row - 1][col - 1]:
            cell_path.append(matrix[row][col])
            seq1_path.append(seq1[col - 2])
            seq2_path.append(seq2[row - 2])
            arrows.append("|")
            if visited:
                del cell_path[cell_path.index(matrix[row][col]):len(cell_path) - 1]
                del seq1_path[cell_path.index(matrix[row][col]):len(seq1_path) - 1]
                del seq2_path[cell_path.index(matrix[row][col]):len(seq2_path) - 1]
                del arrows[cell_path.index(matrix[row][col]):len(arrows) - 1]
            backtracking(matrix, row - 1, col - 1, match, misMatch, gap, seq1, seq2, cell_path, seq1_path, seq2_path, arrows, False)
            visited = True

    # Check Diagonal misMatch
    else:
        if matrix[row][col] - misMatch == matrix[row - 1][col - 1]:
            cell_path.append(matrix[row][col])
            seq1_path.append(seq1[col - 2])
            seq2_path.append(seq2[row - 2])
            arrows.append(" ")
            if visited == True:
                del cell_path[cell_path.index(matrix[row][col]):len(cell_path) - 1]
                del seq1_path[cell_path.index(matrix[row][col]):len(seq1_path) - 1]
                del seq2_path[cell_path.index(matrix[row][col]):len(seq2_path) - 1]
                del arrows[cell_path.index(matrix[row][col]):len(arrows) - 1]
            backtracking(matrix, row - 1, col - 1, match, misMatch, gap, seq1, seq2, cell_path, seq1_path, seq2_path, arrows, False)
            visited = True

    visited = False


# Run the code, then enter your sequences in this format
# default for both sequences to use a preset pairwise sequence or enter your own sequences
# Enter your score e.g: 4 -1 -3
seq1 = input('Enter Sequences(Write default if you want to enter the assigned sequence): ')
seq2 = input('Enter Sequence 2(Write default if you want to enter the assigned sequence): ')
m, mis, g = input('Enter Match, Mismatch and Gap Scores: ').split()

if seq1 == 'default' and seq2 == 'default':
    seq1 = 'CTATTGACGTAACAT'
    seq2 = 'CTATTGAACAT'

filledMat = global_seq_alignment(seq1, seq2, int(m), int(mis), int(g))
backtracking(filledMat, len(filledMat) - 1, len(filledMat[0]) - 1, int(m), int(mis), int(g), seq1, seq2)
