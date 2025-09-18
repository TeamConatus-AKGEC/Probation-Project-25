import random
print("Hello!!")
print("Welcome To Guess the Number Game!!")
chances=7
cmp=random.randrange(1,101)
while(chances>0):
 Guess=int(input("enter the number"))
 if(Guess==cmp):
    print("Correct! User Wins")
    break
 else:
   if(Guess>cmp):
     chances=chances-1
     print("Too High! Attempt left:",chances)  
   else:
       chances=chances-1
       print("Too Low! Attempt left:",chances)   
if(chances==0):
  print("User Lost! The Number was",cmp)       