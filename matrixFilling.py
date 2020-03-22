import numpy as np


def str2char(string):
    list_char = ['-', '-']
    for i in range(len(string)):
        list_char.append(string[i])
    return list_char


def initialization(matrix, first_row, first_col, gap_score):
    matrix[0] = first_row
    for row in range(len(matrix)):
        matrix[row][0] = first_col[row]
    matrix[1][1] = 0
    value = 0
    value = 0
    for i in range(1, len(matrix[0])):
        matrix[1][i] = value
        value += gap_score
    value = 0
    for i in range(1, len(matrix)):
        matrix[i][1] = value
        value += gap_score
    return matrix


def matrix_filling(matrix, scores):
    for row in range(2, len(matrix)):
        for col in range(2, len(matrix[0])):
            if matrix[0][col] == matrix[row][0]:
                s1 = scores['Match'] + matrix[row-1][col-1]
            else:
                s1 = scores['Mismatch'] + matrix[row - 1][col - 1]
            s2 = scores['Gap'] + matrix[row-1][col]
            s3 = scores['Gap'] + matrix[row][col-1]
            matrix[row][col] = max(s1, s2, s3)
    return matrix


def global_seq_alignment(seq_1, seq_2, match_score, mismatch_score, gap_score):
    first_row = str2char(seq_1)
    first_col = str2char(seq_2)
    scores = {'Match': match_score, 'Mismatch': mismatch_score, 'Gap': gap_score}
    rows, cols = (len(seq_2)+2, len(seq_1)+2)
    matrix = []
    for row in range(rows):
        matrix += [[0] * cols]
    initialized_mat = initialization(matrix, first_row, first_col, scores['Gap'])
    filled_mat = matrix_filling(initialized_mat, scores)
    print(filled_mat)
    return filled_mat


def backtracking(matrix, row, col, path, match, misMatch, gap,flag,seq1,seq2):
    if(row==1 or col==1):
        if(matrix[row][col]!=0):
            path.clear()
            return
        else:
            print("(end at )")
            print("end path",path)
            path.clear()
            return
    # up

    if(matrix[row][col]-gap==matrix[row-1][col]):
        print("go up ",matrix[row][col])
        path.append(matrix[row][col])
        # path1=path
        print("Before path", path)
        if(flag==True):
            print("branching")
            print(" After path", path)

        backtracking(matrix, row - 1, col, path, match, misMatch, gap,False,seq1,seq2)

        flag=True

    # left
    if(matrix[row][col]-gap==matrix[row][col-1]) :
        print("Go left",matrix[row][col])
        path.append(matrix[row][col])
        print("Before path", path)
        if(flag==True):
            print("branching")
            print(" after path", path)
            # path1=path
        backtracking(matrix, row, col - 1, path, match, misMatch, gap,False,seq1,seq2)

        flag=True

    # diagonal Match
    if(seq1[col-2]==seq2[row-2]):
        if (matrix[row][col] - match == matrix[row - 1][col - 1]):
            print("Go diagonal match",matrix[row][col])
            path.append(matrix[row][col])
            print("Before path", path)
            if(flag==True):
                print("branching")
                print("after path",path)
                # path=path[:matrix[row][col]]
            backtracking(matrix, row - 1, col - 1, path, match, misMatch, gap,False,seq1,seq2)
            flag=True

        # diagonal Mismatch
    else:
        if (matrix[row][col] - misMatch == matrix[row - 1][col - 1]):
            print("Go diagonal misMatch",matrix[row][col])
            path.append(matrix[row][col])
            print("Before path", path)
            if(flag==True):
                print(" after branching")
                print("path", path)
            backtracking(matrix, row - 1, col - 1, path, match, misMatch, gap,False,seq1,seq2)
            flag=True

    flag=False








seq1 = 'GAATTCAGTTA'
seq2 = 'GGATCGA'
m = 5
mis = -3
g = -4
filledMat=global_seq_alignment(seq1, seq2, m, mis, g)
path=[]
backtracking(filledMat,len(filledMat)-1,len(filledMat[0])-1,path,m,mis,g,False,seq1,seq2)