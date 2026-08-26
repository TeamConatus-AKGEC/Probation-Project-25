import numpy as np
import random as r

arr = np.arange(1,21)
mat1 = np.array(r.choices(arr, k=10)).reshape(2,5)
mat2 = np.array(r.choices(arr, k=10)).reshape(2,5)

addition = mat1 + mat2
print(addition)
print()

subtraction = mat1 - mat2
print(subtraction)
print()

multiply = mat1 * mat2
print(multiply)
print()

division = mat1 / mat2
print(division)
print()

square = mat1 * mat1
print(square)
print()

mat2 = mat2.reshape(5,2)
dot = np.dot(mat1, mat2)
print(dot)
print()

mat2 = np.reshape(mat2, shape=(1,10))
mat2 = np.sort(mat2)
print(mat2)