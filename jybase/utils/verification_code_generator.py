import random


def generate_verification_code(
        include_letter=True, include_upper=True, length=4):
    upper_code = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ' * 5)
    lower_code = list('abcdefghijklmnopqrstuvwxyz' * 5)
    code_to_choice = list('123456789' * 5)
    if include_letter:
        if include_upper:
            code_to_choice.extend(lower_code + upper_code)
        else:
            code_to_choice.extend(lower_code)

    code = ''.join(random.sample(code_to_choice, length))
    return code
