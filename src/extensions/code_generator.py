from string import digits, ascii_lowercase, ascii_uppercase
from random import choice as rand_choice
from secrets import choice as sec_choice


def slug_generator(size: int = 10, char: str = digits + ascii_uppercase + ascii_lowercase) -> str:
    return "".join(rand_choice(char) for _ in range(size))


def otp_generator(size: int = 6, char: str = digits) -> str:
    return "".join(sec_choice(char) for _ in range(size))
