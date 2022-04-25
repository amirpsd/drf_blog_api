from string import digits, ascii_lowercase, ascii_uppercase
from random import choice as rand_choice
from secrets import choice as sec_choice
from os.path import basename, splitext


def get_filename_ext(filepath):
    base_name = basename(filepath)
    name, ext = splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"blogs/{final_name}"


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def slug_generator(size: int = 10, char: str = digits + ascii_uppercase + ascii_lowercase) -> str:
    return "".join(rand_choice(char) for _ in range(size))


def otp_generator(size: int = 6, char: str = digits) -> str:
    return "".join(sec_choice(char) for _ in range(size))
