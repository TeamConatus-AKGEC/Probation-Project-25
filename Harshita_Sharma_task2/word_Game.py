import random
guess = random.choice(["python", "machine", "learning", "data", "science"])
n= len(guess)
name = ""  
chance = 6
i = 0      
print("_"*n)
while chance > 0 and i < n:
    user = input("Enter the guessed letter ")
    if user == guess[i]:   
        name +=user
        i += 1
        print("Correct so far:",name,("_"*(n-i)))
        if name == guess:
            print("Congratulations! You guessed the correct word:", guess)
            break
        else:
          continue
    else:
        chance -= 1
        print("Wrong guess! Chances left:", chance)

if name != guess:
    print("Game over! The word was:", guess)
