import random

a = ["python", "machine", "learning", "data", "science"]
w = random.choice(a)
i=0
c = 6
s = ""
while c>0:
    ch = input("Guess a letter: ")
    if ch == w[i]:
        s += ch
        print("Correct! Word: "+s)
        i=i+1
        if i==len(w):
            break
    else:
        c -= 1
        print("Wrong guess! Chances left:", c)
if c==0:
    print("User lost. The word was:", w)
else:
    print("You won! The word was:", w)