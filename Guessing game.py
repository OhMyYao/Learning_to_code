import sys
import random

#generate a random number
n = random.randint(1, 100)
#Number of guesses set to 0
attempts = 0
#introductory
sys.stdout.write('Welcome to the guessing game. Can you guess what the number is? \n')
guess = 0

while guess != n:
    #check input error
    try:
         #user’s guess
        guess = int(input('What is your guess? '))
        attempts += 1
        #loop the game until guess is correct and adding to the attempts per attempt
        if guess < n:
            sys.stdout.write('Higher! Try again!\n')
        elif guess > n:
            sys.stdout.write('Lower! Try again!\n')
        else:
            sys.stdout.write(f'Correct! You took {attempts} attempts. \n')
    except ValueError:
        sys.stdout.write('Invalid input. Please choose a number between 1 to 100\n')