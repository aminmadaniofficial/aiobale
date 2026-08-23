import secrets


def generate_id(length=16):
    if length < 1:
        raise ValueError("Length must be at least 1.")
    first_digit = str(secrets.randbelow(9) + 1)
    remaining_digits = ''.join(str(secrets.randbelow(10)) for _ in range(length - 1))
    return int(first_digit + remaining_digits)
