from string import digits, ascii_lowercase, ascii_uppercase
from random import choice


def slug_generator(size: int = 10, char: str = digits + ascii_uppercase + ascii_lowercase) -> str:
    return "".join(choice(char) for _ in range(size))


def otp_generator(size: int = 6, char: str = digits) -> str:
    return "".join(choice(char) for _ in range(size))
