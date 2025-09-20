import numpy as np
print("Task 3.1 \n")

new_array = np.random.randint(1, 101, size=10)

print("Array: ",new_array)
print("Max Element: ",np.max(new_array))
print("Min Element: ",np.min(new_array))
print("Mean: ",np.mean(new_array))
print("Sum: ",np.sum(new_array))
print("Index of max element: ",np.argmax(new_array))
print("Index of min element: ",np.argmin(new_array))
print("Sorted array: ", np.sort(new_array))

print("\nTask 3.2 \n")

array_3d = np.random.randint(1, 21, size=(3,3))

print(array_3d)
print("First row: ",array_3d[0])
print("Second coloumn: ",array_3d[:,2])
print("Element at (2,2): ",array_3d[2,2])
print("Sub-array:\n",array_3d[0:2,0:2])
array_3d[1,1] = 99
print(array_3d)

print("\nTask 3.3 \n")

arr1 = np.random.randint(1, 21, size=10)
arr2 = np.random.randint(1, 21, size=10)
print("Array 1: ",arr1)
print("Array 2: ",arr2)
print("Sum of arrays: ",arr1 + arr2)
print("Sub of arrays: ",arr1 - arr2)
print("Multi of arrays: ",arr1 * arr2)
print("Division of arrays: ",np.round(arr1 / arr2,2))
print("Square of array: ",arr1**2)
print("Dot product of arrays: ",np.dot(arr1, arr2))
print("Sorted 2 array: ",np.sort(arr2))