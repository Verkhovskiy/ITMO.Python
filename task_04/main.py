from generate_csv import generate_matrices
from benchmark import benchmark
import subprocess

def main():
    inp = input("""### Welcome to DGEMM! ###
Enter "Y" to start -> """)
    if inp.capitalize() != "Y":
        return
    print("Please input range of values of matrix elements:")
    low = int(input("Lowest value -> "))
    high = int(input("Highest value -> "))
    print("Please choose dimensions for matrices:")
    M = int(input("Matrix A rows -> "))
    K = int(input("Matrix A columns -> "))
    N = int(input("Matrix B columns -> "))
    generate_matrices(low, high, M, K, N)
    print("Please input alpha and beta:")
    alpha = float(input("Alpha -> "))
    beta = float(input("Beta -> "))
    print("Please input number if DGEMM iterations:")
    iterations = int(input("Iterations -> "))

    python_int_time, python_float_time = benchmark(alpha, beta, iterations)

    """ cmd = ['java', '-classpath', './', 'Main', str(alpha), str(beta), str(iterations)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output, error = process.communicate() """

    print(python_int_time, python_float_time)

if __name__ == "__main__":
    main()