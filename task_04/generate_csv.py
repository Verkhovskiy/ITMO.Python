from matrix import Matrix
import csv

def generate_matrices(lowest_matrix_value, highest_matrix_value, matrix_A_rows, matrix_A_columns, matrix_B_columns):
    a_int = Matrix.generate_matrix(matrix_A_rows, matrix_A_columns, "int", lowest_matrix_value, highest_matrix_value)
    a_float = Matrix.generate_matrix(matrix_A_rows, matrix_A_columns, "float", lowest_matrix_value, highest_matrix_value)
    b_int = Matrix.generate_matrix(matrix_A_columns, matrix_B_columns, "int", lowest_matrix_value, highest_matrix_value)
    b_float = Matrix.generate_matrix(matrix_A_columns, matrix_B_columns, "float", lowest_matrix_value, highest_matrix_value)
    c_int = Matrix.generate_matrix(matrix_A_rows, matrix_B_columns, "int", lowest_matrix_value, highest_matrix_value)
    c_float = Matrix.generate_matrix(matrix_A_rows, matrix_B_columns, "float", lowest_matrix_value, highest_matrix_value)

    with open('data/int_matrices.csv', 'w', newline='') as csvfile:
        matrixwriter = csv.writer(csvfile, delimiter=',')
        for row in a_int.m:
            matrixwriter.writerow(row)
        matrixwriter.writerow("")
        for row in b_int.m:
            matrixwriter.writerow(row)
        matrixwriter.writerow("")
        for row in c_int.m:
            matrixwriter.writerow(row)

    with open('data/float_matrices.csv', 'w', newline='') as csvfile:
        matrixwriter = csv.writer(csvfile, delimiter=',')
        for row in a_float.m:
            matrixwriter.writerow(row)
        matrixwriter.writerow("")
        for row in b_float.m:
            matrixwriter.writerow(row)
        matrixwriter.writerow("")
        for row in c_float.m:
            matrixwriter.writerow(row)