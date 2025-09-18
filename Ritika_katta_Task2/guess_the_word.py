import random
a= ["python", "machine", "learning", "data", "science"]
b=random.choice(a)
chances=6
list=[]
for i in range(len(b)):
    list.append("_")
Word=" ".join(list) 
while(chances>0 and "_"in Word):
    print("Word:",Word)
    c=input("enter the letter").lower()
    if(c in b):
        print("Correct!")
        for i in range(len(b)):
            if(b[i]==c):
                list[i]=c
                Word=" ".join(list)
                print('Word:',Word)        
    else:
        chances=chances-1  
        print("Wrong guess! Chances left:",chances)
