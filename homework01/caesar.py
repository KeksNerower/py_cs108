import typing as tp


#THIS IS JUST FOR NEW REQUEST
# MY FUNCTION
def shift_counter(ch: str, shift: int) -> str:
    res = ch

    if "a" <= ch <= "z":
        from_ch = "a"
        to_ch = "z"
    elif "A" <= ch <= "Z":
        from_ch = "A"
        to_ch = "Z"
    else:
        return res

    reverser = 1
    r_shift_flag = shift < 0  # true => reverse shift

    if r_shift_flag:
        from_ch, to_ch = to_ch, from_ch
        reverser = -1

    up_moving_flag = (
        ord(ch) + shift <= ord(to_ch) and not r_shift_flag
    )  # true => ch-position after shift <= then to_ch-position & normal shift
    down_moving_flag = (
        ord(ch) + shift >= ord(to_ch) and r_shift_flag
    )  # true => ch-position after shift >= to_ch-position & reverse shift

    if up_moving_flag or down_moving_flag:
        res = chr(ord(ch) + shift)
    else:
        dist = ord(to_ch) - ord(ch)
        new_shift = shift - dist - 1 * reverser
        res = chr(ord(from_ch) + new_shift)

    return res


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    if shift > (ord("z") - ord("a")):
        return plaintext

    for ch in plaintext:
        ciphertext += shift_counter(ch, shift)

    # END OF CODE
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    if shift > (ord("z") - ord("a")):
        return ciphertext

    for ch in ciphertext:
        plaintext += shift_counter(ch, -shift)
    # END CODE
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
