"""
Project 4
Vignesh P
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Takes as input a set of characters alphabet and three scores diag_score, off_diag_score,
    and dash_score. The function returns a dictionary of dictionaries whose
    entries are indexed by pairs of characters in alphabet plus -. The score for any entry
    indexed by one or more dashes is dash_score. The score for the remaining diagonal entries
    is diag_score. Finally, the score for the remaining off-diagonal entries is off_diag_score.
    """

    characters = list(alphabet)
    characters.append("-")
    dictionary_of_scores = dict()
    for row_character in characters:
        dictionary_of_col = dict()
        for col_character in characters:
            if (row_character == "-" or col_character == "-"):
                dictionary_of_col[col_character] = dash_score
            elif (row_character == col_character):
                dictionary_of_col[col_character] = diag_score
            else:
                dictionary_of_col[col_character] = off_diag_score
        dictionary_of_scores[row_character] = dictionary_of_col
    return dictionary_of_scores


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix
    scoring_matrix. The function computes and returns the alignment matrix for seq_x and seq_y as described in the
    Homework. If global_flag is True, each entry of the alignment matrix is computed using the method described in
    Question 8 of the Homework. If global_flag is False, each entry is computed using the method described in Question 12
    of the Homework.
    """
    alignment_matrix = list()
    # fill alignment matrix with 0's, makes it easier to edit later
    for idx1 in range(len(seq_x) + 1):
        temp_list = list()
        for idx2 in range(len(seq_y) + 1):
            temp_list.append(0)
        alignment_matrix.append(temp_list)

    # initialization of values
    for idx in range(1, len(seq_x) + 1):
        alignment_matrix[idx][0] = alignment_matrix[idx - 1][0] + scoring_matrix[seq_x[idx - 1]]["-"]
        if (not global_flag and alignment_matrix[idx][0] < 0):
            alignment_matrix[idx][0] = 0
    for idx in range(1, len(seq_y) + 1):
        alignment_matrix[0][idx] = alignment_matrix[0][idx - 1] + scoring_matrix["-"][seq_y[idx - 1]]
        if (not global_flag and alignment_matrix[0][idx] < 0):
            alignment_matrix[0][idx] = 0
    for idx1 in range(1, len(seq_x) + 1):
        for idx2 in range(1, len(seq_y) + 1):
            alignment_matrix[idx1][idx2] = max(
                alignment_matrix[idx1 - 1][idx2 - 1] + scoring_matrix[seq_x[idx1 - 1]][seq_y[idx2 - 1]],
                alignment_matrix[idx1 - 1][idx2] + scoring_matrix[seq_x[idx1 - 1]]["-"],
                alignment_matrix[idx1][idx2 - 1] + scoring_matrix["-"][seq_y[idx2 - 1]]
            )
            if (not global_flag and alignment_matrix[idx1][idx2] < 0):
                alignment_matrix[idx1][idx2] = 0

    return alignment_matrix


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix
    scoring_matrix. This function computes a global alignment of seq_x and seq_y using the global alignment
    matrix alignment_matrix.The function returns a tuple of the form (score, align_x, align_y) where score is
    the score of the global alignment align_x and align_y. Note that align_x and align_y should have the same
    length and may include the padding character -.
    """
    row = len(seq_x)
    col = len(seq_y)
    seq_x_prime = str()
    seq_y_prime = str()
    score = 0

    while row != 0 and col != 0:
        if (alignment_matrix[row][col] == alignment_matrix[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]):
            seq_x_prime = seq_x[row - 1] + seq_x_prime
            seq_y_prime = seq_y[col - 1] + seq_y_prime
            score += scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]
            row = row - 1
            col = col - 1
        elif (alignment_matrix[row][col] == alignment_matrix[row - 1][col] + scoring_matrix[seq_x[row - 1]]["-"]):
            seq_x_prime = seq_x[row - 1] + seq_x_prime
            seq_y_prime = "-" + seq_y_prime
            score += scoring_matrix[seq_x[row - 1]]["-"]
            row = row - 1
        else:
            seq_x_prime = "-" + seq_x_prime
            seq_y_prime = seq_y[col - 1] + seq_y_prime
            score += scoring_matrix["-"][seq_y[col - 1]]
            col = col - 1

    while row != 0:
        seq_x_prime = seq_x[row - 1] + seq_x_prime
        seq_y_prime = "-" + seq_y_prime
        score += scoring_matrix[seq_x[row - 1]]["-"]
        row = row - 1

    while col != 0:
        seq_x_prime = "-" + seq_x_prime
        seq_y_prime = seq_y[col - 1] + seq_y_prime
        score += scoring_matrix["-"][seq_y[col - 1]]
        col = col - 1

    return (score, seq_x_prime, seq_y_prime)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common alphabet with the scoring matrix
    scoring_matrix. This function computes a local alignment of seq_x and seq_y using the local alignment matrix
    alignment_matrix.The function returns a tuple of the form (score, align_x, align_y) where score is the score
    of the optimal local alignment align_x and align_y. Note that align_x and align_y should have the same length
    and may include the padding character -.
    """

    row = 0
    col = 0
    maximum = 0

    for idx1 in range(len(seq_x) + 1):
        for idx2 in range(len(seq_y) + 1):
            if (alignment_matrix[idx1][idx2] > maximum):
                maximum = alignment_matrix[idx1][idx2]
                row = idx1
                col = idx2

    seq_x_prime = str()
    seq_y_prime = str()
    score = 0

    while row != 0 and col != 0 and alignment_matrix[row][col] != 0:
        print "This is row: " + str(row)
        print "This is col: " + str(col)
        if (alignment_matrix[row][col] == alignment_matrix[row - 1][col - 1] + scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]):
            seq_x_prime = seq_x[row - 1] + seq_x_prime
            seq_y_prime = seq_y[col - 1] + seq_y_prime
            score += scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]
            row = row - 1
            col = col - 1
        elif (alignment_matrix[row][col] == alignment_matrix[row - 1][col] + scoring_matrix[seq_x[row - 1]]["-"]):
            seq_x_prime = seq_x[row - 1] + seq_x_prime
            seq_y_prime = "-" + seq_y_prime
            score += scoring_matrix[seq_x[row - 1]]["-"]
            row = row - 1
        else:
            seq_x_prime = "-" + seq_x_prime
            seq_y_prime = seq_y[col - 1] + seq_y_prime
            score += scoring_matrix["-"][seq_y[col - 1]]
            col = col - 1

    return (score, seq_x_prime, seq_y_prime)


scoring_matrix = build_scoring_matrix(["A", "C", "T", "G"], 10, 4, -6)
alignment_matrix = compute_alignment_matrix("AA", "TAAT", scoring_matrix, False)
print alignment_matrix
compute_local_alignment("AA", "TAAT", scoring_matrix, alignment_matrix)


"""
print compute_local_alignment('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0, 0], [0, 6]])

print compute_global_alignment('ACTACT', 'AGCTA', {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1}, 'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1}, '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0}, 'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1}, 'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}, [[0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2], [0, 2, 3, 4, 4, 4], [0, 2, 3, 4, 6, 6], [0, 2, 3, 4, 6, 8], [0, 2, 3, 5, 6, 8], [0, 2, 3, 5, 7, 8]])


print compute_global_alignment('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 
                                    'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
                                    '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 
                                    'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
                                    'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, 
                         [[0, -4], [-4, 6]])
 expected ({'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, 6, 'A', 'A', True)
print compute_global_alignment('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2}, 
                                        'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2}, 
                                        '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4}, 
                                        'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
                                        'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, [[0]]) 
print compute_alignment_matrix('ACTACT', 'GGACTGCTTCTGG', {'A': {'A': 2, 'C': 1, '-': 0, 'T': 1, 'G': 1},
                                                           'C': {'A': 1, 'C': 2, '-': 0, 'T': 1, 'G': 1},
                                                           '-': {'A': 0, 'C': 0, '-': 0, 'T': 0, 'G': 0},
                                                           'T': {'A': 1, 'C': 1, '-': 0, 'T': 2, 'G': 1},
                                                           'G': {'A': 1, 'C': 1, '-': 0, 'T': 1, 'G': 2}}, True)
print compute_alignment_matrix('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
                                        'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
                                        '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
                                        'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
                                        'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True)
print compute_alignment_matrix('A', 'A', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
                                          'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
                                          '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
                                          'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2},
                                          'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True)

print compute_alignment_matrix('', '', {'A': {'A': 6, 'C': 2, '-': -4, 'T': 2, 'G': 2},
                                  'C': {'A': 2, 'C': 6, '-': -4, 'T': 2, 'G': 2},
                                  '-': {'A': -4, 'C': -4, '-': -4, 'T': -4, 'G': -4},
                                  'T': {'A': 2, 'C': 2, '-': -4, 'T': 6, 'G': 2}, 
                                  'G': {'A': 2, 'C': 2, '-': -4, 'T': 2, 'G': 6}}, True)
"""
# print build_scoring_matrix(set(["a", "b", "c", "d"]), 5, 3, 0)

# print compute_alignment_matrix("ABC", range(3), range(3), range(3))