import random
a= ["python", "machine", "learning", "data", "science"]
b=random.choice(a)
chances=6
word=[]
for i in range(len(a)):
    word.append("_")
Word=" ".join(word) 
print("Word:",Word)
