import random

def randomiser():
    lissie = [1, 2, 3, 4, 5]
    random_digit = random.choice(lissie)
    print(f"Random digit: {random_digit}")

# Call the function
randomiser()
