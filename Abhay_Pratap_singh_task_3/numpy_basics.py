import random as r
import numpy as np

arr = np.arange(1,101)
num = r.choices(arr, k=10)

max = np.max(num)
print('Maximum Element: ',max)
min = np.min(num)
print('Minimum Element: ',min)
mean = np.mean(num)
print('Mean of All the Elements: ',mean)
sum = np.sum(num)
print('Sum of all the Elements: ',sum)
max_index = np.argmax(num)
print('Index of max Element: ',max_index)
min_index = np.argmin(num)
print('Index of min Element: ',min_index)
sort = np.sort(num)
print('Sorted array: ',sort)