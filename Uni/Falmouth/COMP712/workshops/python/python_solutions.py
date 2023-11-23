'''
    possible solutions to the workshop 1's problems
    Dr Daniel Zhang @ Falmouth University
    Nov 2023
'''


import random


def is_prime(x):
    ''' return true if the input x is a prime '''
    if not isinstance(x, int) or x < 2:
        return False
    if x == 2:
        return True
    for c in range(2, int(x**0.5+1)):
        if x % c == 0:
            return False
    return True


def primes_n():
    ''' print all primes between [2,N] '''
    try:
        n = int(input('Please specify the number N: '))
        primes = [x for x in range(2, n+1) if is_prime(x)]
        print(f'There are {len(primes)} primes within [2, {n}]: {primes}')
    except:
        print('Error')


def guess_number():
    ''' a simple game to guess the number: return bigger or smaller '''
    while True:
        the_number = random.randint(0, 1000)
        guess = 0
        play = True
        while play:
            try:
                x = input('Please guess the number (q for exit): ').strip()
                if x.lower() == 'q':
                    print(f'Exhausted? OK, the number is: {the_number}')
                    play = False
                    break
                x = int(x)
                guess += 1
                if x == the_number:
                    print(
                        f"Yeah! You got it after {guess} {'guesses' if guess > 1 else 'guess'} - it is {the_number}!")
                    print('-'*40)
                    break
                elif x < the_number:
                    print(
                        f"Um, it is too small - {guess} {'guesses' if guess > 1 else 'guess'}!")
                elif x > the_number:
                    print(
                        f"Um, it is too big - {guess} {'guesses' if guess > 1 else 'guess'}!")
            except:
                print('Wrong input')
        if not play:
            break


def guess_number_adv():
    ''' another guess my number advanced, it will report the place and digit correctly guessed '''
    while True:
        the_number = random.randint(1000, 10000)
        guess = 0
        play = True
        while play:
            try:
                x = input('Please guess a 4-digit number (q for exit): ').strip()
                if x.lower() == 'q':
                    print(f'Exhausted? OK, the number is: {the_number}')
                    play = False
                    break
                guess += 1
                the_number = str(the_number)
                if x == the_number:
                    print(f'Yeah! You got it - it is {the_number}!')
                    print('-'*40)
                    break
                else:
                    good_dgs = len([d for d in x if d in the_number])
                    good_pos = len([x[i] for i in range(
                        len(x)) if x[i] == the_number[i]])
                    print(
                        f'correct digits: {good_dgs}, correct position: {good_pos}')
            except:
                print('Wrong input')
        if not play:
            break


if __name__ == '__main__':
    while True:
        print('''
[1]: Prime Number Calculation
[2]: Guess My Number Game
[3]: Guess The Number Game (Advanced)''')
        x = input('Please select the task index (1-3, q for exit): ').strip()
        if x.lower() == 'q':
            break
        try:
            x = int(x)
        except:
            print('Wrong input')
            continue
        if x < 1 or x > 3:
            continue
        print('-'*40)
        print(f'Your selection is Task [{x}]\n')
        # make a dict mapping from number of selection to functions
        funcs = {1: primes_n, 2: guess_number, 3: guess_number_adv}
        funcs[x]()
