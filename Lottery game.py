#Lottery winnings game
import sys
import random
#list of winning numbers randomly generated
list1 = random.sample(range(1, 100), 9)
try:
#ask for user's number and prints out if number is a winning number
    number = int(input("What is your lottery number: "))
    if number in list1:
        sys.stdout.write("Congratulations!\n")
    else:
        sys.stdout.write("Sorry, you lose.\n")
except ValueError:
    sys.stdout.write("Invalid input! Numbers only.\n")