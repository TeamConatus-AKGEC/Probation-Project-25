import pandas as pd
import random as r
import numpy as np

# 1
arr = np.arange(1,101)
num = pd.Series(r.choices(arr, k=10), index={1,2,3,4,5,6,7,8,9,10})

# 2
print(num)
print()

print(num.head(5))
print()

print(num[:5])
print()
print(num[5:])
print()
print('Maximum: ',max(num),' Minimum: ',min(num))
print()
print('Mean: ',np.mean(num))

# 3
print()
numbers = list(num)
print(numbers)