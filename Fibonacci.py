import sys 

#stores fibonacci in a dictionary to reduced execissive calculations
def fib(i, memo={}):
    if i in memo:
        return memo[i]
    if i == 0 or i == 1:
        return i
    memo[i] = fib(i - 1, memo) + fib(i - 2, memo)
    return memo[i]

def ask():
    while True:
        #input validation
        try:
            sys.stdout.write("Enter a value (negative to quit): ")
            i = int(sys.stdin.readline())
            if i < 0:
                break
            x = fib(i)
            sys.stdout.write(str(i) + ", " + str(x) + "\n")
        except ValueError:
            sys.stdout.write("Invalid input. Please enter an integer.\n")
ask()