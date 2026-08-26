import random as r
import numpy as np

arr = np.arange(1,21)
num = r.choices(arr, k=9)
mat = np.reshape(num, shape=(3,3))

print('Matrix: \n',mat)
print()
print('First row:\n',mat[0,:])
print()
print('Second column:\n',mat[:,1])
print()
print('Middle element:\n',mat[1,1])
print()
print('First two rows and column:\n',mat[:2,:2])
print()
mat[1,1] = 99
print('Modified Matiex:\n',mat)