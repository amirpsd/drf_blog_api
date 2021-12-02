from random import choice
from string import digits,ascii_lowercase,ascii_uppercase

def code_generator(size:int= 10, char:str = digits+ascii_uppercase+ascii_lowercase):
    return "".join(choice(char)for _ in range(size))
    