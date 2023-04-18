import random

class Matrix:
    def __init__(self, array):
        self.m = array
        self.shape = self.define_shape()

    def generate_matrix(rows, columns, type = "int", min = 0, max = 100):
        if type == "int":
            return Matrix([[random.randint(min, max) for column in range(columns)] for row in range(rows)])
        elif type == "float":
            return Matrix([[random.uniform(min, max) for column in range(columns)] for row in range(rows)])
        else:
            raise Exception("Can't create matrix. Incorrect data type.")

    def define_shape(self):
        rows = len(self.m)
        columns = len(self.m[0])
        for row in self.m: 
            if len(row) != columns:
                raise Exception("Can't create matrix. Array shape is incorrect.")
        return (rows, columns)

    def __mul__(self, other):
        if type(other) == Matrix:
            if other.shape[0] != self.shape[1]:
                raise Exception("Can't multiply matrices. Matrix shape is incorrect.")
            result = []
            for i in range(self.shape[0]):
                result.append([])
                for j in range(other.shape[1]):
                    result[i].append(sum([self.m[i][k] * other.m[k][j] for k in range(self.shape[1])]))
            return Matrix(result)
        elif type(other) == int or type(other) == float:
            return Matrix([[num * other for num in row] for row in self.m])
        raise Exception("Can't multiply matrix with this data type.")

    def __add__(self, other):
        if type(other) == Matrix:
            if other.shape != self.shape:
                raise Exception("Can't add matrices. Matrix shape is incorrect.")
            return Matrix([[self.m[row][column] + other.m[row][column] for column in range(self.shape[1])] for row in range(self.shape[0])])
        raise Exception("Can't add matrix with this data type.")
