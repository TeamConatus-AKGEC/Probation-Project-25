import random as r
words = ["python", "machine", "learning", "data", "science"]
comp = r.choices(words)
length = len(comp[0])

chances = 6
progress = []
for word in comp:
    for i in word:
        progress.append(i)

def trackProgress(letter, chances):
    if progress == []:
        print('Guess Correctly. You Won. Word was',comp[0])
        return True
    else:
        if letter in progress:
            print('Correct Guess.')
        else:
            chances -= 1
            print('out')
            print('Wrong Guess. Chances left: ',chances)
        while letter in progress:
            progress.remove(letter)
        print()
        return False, chances
            
def showProgress(progress):
    for char in comp[0]:
        if char in progress:
            print('_', end="")
        else:
            print(char, end="")
    print()



while chances > 0:
    letter = str(input('Guess a character: '))
    isWon, chances = trackProgress(letter, chances)
    if isWon == True:
        break
    showProgress(progress)
    print()
