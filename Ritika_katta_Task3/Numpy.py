import numpy as np
#Task 3.1

a1=np.random.randint(1,101,10)
print(a1)
print(np.max(a1))
print(np.min(a1))
print(np.mean(a1))
print(np.sum(a1))
print(np.argmax(a1))
print(np.argmin(a1))
print(np.sort(a1))

#Task2
a2=np.random.randint(1,21,9).reshape(3,3)
print(a2)
print(a2[0])

print(a2[:,1])
print(a2[2,2])
print(a2[0:2,0:2])
a2[1,1]=99
print(a2)

#Task3
a3=np.random.randint(1,21,10)
a4=np.random.randint(1,21,10)
print(a3)
print(a4)
print(a3+a4)
print(a3-a4)
print(a3*a4)
print(a3/a4)
print(a3//a4)
print(a3**2)
print(np.dot(a3,a4))
print(np.sort(a4))