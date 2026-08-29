"""
HIT137 Group Assesment 2
RIWAJ SHRESTHA
SAWAN GURUNG
JUNG-CHUAN CHIANG

Question 2 - Expression evaluator using recursive descent parsing.

Reads one expression per line from a text file and writes a four line block
(Input, Tree, Tokens, Result) for each one into output.txt .
"""

DIGITS = "0123456789"
OPERATORS = "+-*/%^"

def format_number(value):
    """Whole numbers print without a decimal point, the rest round to 4 places."""
    rounded = round(float(value), 4)
    if rounded == 0:
        rounded = 0.0
    if rounded.is_integer():
        return str(int(rounded))
    return f"{rounded:.4f}".rstrip("0").rstrip(".")


def read_number(text, start):
    """Read digits, then an optional dot followed by more digits."""
    index = start
    while index < len(text) and text[index] in DIGITS:
        index += 1

    if index < len(text) and text[index] == ".":
        index += 1
        if index >= len(text) or text[index] not in DIGITS:
            raise ValueError("a dot must be followed by a digit")
        while index < len(text) and text[index] in DIGITS:
            index += 1

    return float(text[start:index]), index


def tokenise(expression):
    """Turn the expression into a list of (type, value) pairs ending with END."""
    tokens = []
    index = 0

    while index < len(expression):
        character = expression[index]

        if character in " \t":
            index += 1
        elif character in DIGITS:
            value, index = read_number(expression, index)
            tokens.append(("NUM", value))
        elif character in OPERATORS:
            tokens.append(("OP", character))
            index += 1
        elif character == "(":
            tokens.append(("LPAREN", "("))
            index += 1
        elif character == ")":
            tokens.append(("RPAREN", ")"))
            index += 1
        else:
            raise ValueError("bad character: " + character)

    tokens.append(("END", None))
    return tokens


def format_tokens(tokens):
    """Build the tokens line, e.g. [NUM:3] [OP:+] [NUM:5] [END]"""
    parts = []
    for token_type, value in tokens:
        if token_type == "END":
            parts.append("[END]")
        elif token_type == "NUM":
            parts.append("[NUM:" + format_number(value) + "]")
        else:
            parts.append("[" + token_type + ":" + value + "]")
    return " ".join(parts)


print(format_tokens(tokenise("3.5 * (5.5-4)")))