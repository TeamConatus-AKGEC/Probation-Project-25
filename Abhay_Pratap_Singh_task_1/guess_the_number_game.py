import random as r

# it generate a random integer between 1 and 100 nd store it in comp variable
comp = r.randint(1,100)

# to count the number of attempts
attempts = 0

# loop until user guess the number correctly or uses all the attempts
while True:
    user = int(input(" \nGuess the number from 1 to 100: "))
    attempts += 1
    if user < comp:
        print("Too low! Attempts left: ", 7 - attempts)
    elif user > comp:
        print("Too high! Attempts left: ", 7 - attempts)
    elif user < 1 or user > 100:
        print("Please enter a number between 1 and 100")
        attempts -= 1
    elif user == comp:
        print("You guessed it! The number was", comp)
        print("You took", attempts, "attempts")
        break
    if attempts == 7:
        print("User lost! The number was ", comp)
        break
