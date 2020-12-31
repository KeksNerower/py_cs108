import typing as tp

from caesar import shift_counter


def shift_parser(shift_in_chars: str) -> tp.List[int]:
    shift_in_ints = []
    shift_in_chars = shift_in_chars.lower()

    for ch in shift_in_chars:
        shift_in_ints.append(ord(ch) - ord("a"))

    return shift_in_ints



def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    if shift > (ord("z") - ord("a")):
        return plaintext

    for ch in plaintext:
        ciphertext += shift_counter(ch, shift)

    return ciphertext
    # END OF CODE


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    converted_keyword = shift_parser(keyword)

    for i in range(len(ciphertext)):
        plaintext += shift_counter(ciphertext[i], -converted_keyword[i % len(converted_keyword)])
    
    return plaintext
    # END OF CODE
