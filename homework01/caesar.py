import typing as tp

#MY FUNCTION
def shift_counter(ch: str, shift: int) -> str:
    res = ch
    if 'A' < ch < 'Z':
        min_ch = 'A'
        max_ch = 'Z'
    elif 'a' < ch < 'z':
        min_ch = 'a'
        max_ch = 'z'
    else: 
        return res

    if (ord(ch) + shift <= ord(max_ch)):
        res = chr(ord(ch) + shift)
    else:
        dist = ord(max_ch) - ord(ch)
        new_shift = shift - dist
        res = chr(ord(min_ch) + new_shift)

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
    if shift > (ord('z') - ord('a')):
        return plaintext
    

    for ch in plaintext:
        ciphertext += shift_counter(ch, shift)
        
    #END OF CODE
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
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
