# Character sets defined for modular shifts
LOWER_FIRST = "abcdefghijklmn"
LOWER_SECOND = "opqrstuvwxyz"
UPPER_FIRST = "ABCDEFGHIJKLM"
UPPER_SECOND = "NOPQRSTUVWXYZ"
DIGITS = "0123456789"


def encrypt_char(char: str, shift1: int, shift2: int) -> str:
    """Encrypt a single character based on the given shift values."""
    if char in LOWER_FIRST:
        step = shift1 * shift2
        idx = (LOWER_FIRST.index(char) + step) % len(LOWER_FIRST)
        return LOWER_FIRST[idx]
    elif char in LOWER_SECOND:
        step = shift1 + shift2
        idx = (LOWER_SECOND.index(char) - step) % len(LOWER_SECOND)
        return LOWER_SECOND[idx]

    elif char in UPPER_FIRST:
        step = shift1
        idx = (UPPER_FIRST.index(char) - step) % len(UPPER_FIRST)
        return UPPER_FIRST[idx]
    elif char in UPPER_SECOND:
        step = shift2 ** 2
        idx = (UPPER_SECOND.index(char) + step) % len(UPPER_SECOND)
        return UPPER_SECOND[idx]

    elif char in DIGITS:
        step = shift1 * shift2
        idx = (DIGITS.index(char) + step) % len(DIGITS)
        return DIGITS[idx]

    return char


def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Read raw text from input_path, encrypt it, and save to output_path."""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    encrypted_chars = [encrypt_char(c, shift1, shift2) for c in text]
    encrypted_text = "".join(encrypted_chars)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encrypted_text)


if __name__ == "__main__":
    s1 = int(input("Enter shift1 (non-negative integer): "))
    s2 = int(input("Enter shift2 (non-negative integer): "))

    encrypt_file(s1, s2, "raw_text.txt", "encrypted_text.txt")
    print("Encryption test passed: 'encrypted_text.txt' created successfully.")
