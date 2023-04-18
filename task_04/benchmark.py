from matrix import Matrix
import csv
import time

def upload_marices_from_csv(path, data_type):
    with open(path, newline='') as csvfile:
        matrixreader = csv.reader(csvfile, delimiter=',')
        matrices = []
        matrix = []
        for row in matrixreader:
            if len(row):
                if data_type.casefold() == 'int':
                    matrix.append([int(num) for num in row])
                elif data_type.casefold() == 'float':
                    matrix.append([float(num) for num in row])
            else:
                matrices.append(matrix)
                matrix = []
        matrices.append(matrix)
        return [Matrix(matrix) for matrix in matrices]
    
def output_result(C_int, C_float):
    with open('data/python_result_int.csv', 'w', newline='') as csvfile:
        matrixwriter = csv.writer(csvfile, delimiter=',')
        for row in C_int.m:
            matrixwriter.writerow(row)
    with open('data/python_result_float.csv', 'w', newline='') as csvfile:
        matrixwriter = csv.writer(csvfile, delimiter=',')
        for row in C_float.m:
            matrixwriter.writerow(row)

def benchmark(alpha, beta, iterations):
    alpha_int = int(alpha)
    beta_int = int(beta)
    alpha_float = int(alpha)
    beta_float = int(beta)
    A_int, B_int, C_int = upload_marices_from_csv('data/int_matrices.csv', 'int')
    A_float, B_float, C_float = upload_marices_from_csv('data/float_matrices.csv', 'float')

    int_start_time = time.time()
    for _ in range(iterations):
        C_int = A_int * alpha_int * B_int + C_int * beta_int
    int_benchmark_time = time.time() - int_start_time
    
    float_start_time = time.time()
    for _ in range(iterations):
        C_float = A_float * alpha_float * B_float + C_float * beta_float
    float_benchmark_time = time.time() - float_start_time

    output_result(C_int, C_float)

    return int_benchmark_time, float_benchmark_time