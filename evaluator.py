"""
HIT137 Group Assesment 2
RIWAJ SHRESTHA
SAWAN GURUNG
JUNG-CHUAN CHIANG

Question 2 - Expression evaluator using recursive descent parsing.

Reads one expression per line from a text file and writes a four line block
(Input, Tree, Tokens, Result) for each one into output.txt .
"""

TOKEN_TYPES = {
    "+": "OP",
    "-": "OP",
    "*": "OP",
    "/": "OP",
    "%": "OP",
    "^": "OP",
    "(": "LPAREN",
    ")": "RPAREN"
}
 
def tokenize_expression(expression):
    tokens = []
    position = 0
 
    while position < len(expression):
        character = expression[position]
 
        if character.isspace():
            position += 1
 
        elif character.isdigit():
            number = ""
 
            while position < len(expression) and expression[position].isdigit():
                number += expression[position]
                position += 1
 
            tokens.append(("NUM", number))
 
        elif character in TOKEN_TYPES:
            tokens.append((TOKEN_TYPES[character], character))
            position += 1
 
        else:
            return "ERROR"
 
    tokens.append(("END", ""))
    return tokens
 
def is_operator(tokens, position, operators):
    if position >= len(tokens):
        return False
 
    if tokens[position][0] == "OP" and tokens[position][1] in operators:
        return True
 
    return False
 
 
def parse_number_or_parentheses(tokens, position):
    token_type, value = tokens[position]
 
    if token_type == "NUM":
        return float(value), position + 1
 
    if token_type == "LPAREN":
        tree, position = parse_addition_subtraction(tokens, position + 1)
 
        if tree == "ERROR":
            return "ERROR", position
 
        if position < len(tokens) and tokens[position][0] == "RPAREN":
            return tree, position + 1
 
    return "ERROR", position
 