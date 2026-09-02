"""
HIT137 Group Assesment 2
RIWAJ SHRESTHA
SAWAN GURUNG
JUNG-CHUAN CHIANG

Question 2 - Expression evaluator using recursive descent parsing

"""
import os 

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
def parse_exponent(tokens, position):
    left, position = parse_number_or_parentheses(tokens, position)
 
    if left == "ERROR":
        return "ERROR", position
 
    if is_operator(tokens, position, ("^",)):
        right, position = parse_exponent(tokens, position + 1)
 
        if right == "ERROR":
            return "ERROR", position
 
        left = ("^", left, right)
 
    return left, position
 
 
def parse_negative(tokens, position):
    if is_operator(tokens, position, ("+",)):
        return "ERROR", position
 
    if is_operator(tokens, position, ("-",)):
        value, position = parse_negative(tokens, position + 1)
 
        if value == "ERROR":
            return "ERROR", position
 
        return ("neg", value), position
 
    return parse_exponent(tokens, position)
 
 
def parse_multiplication(tokens, position):
    left, position = parse_negative(tokens, position)
 
    if left == "ERROR":
        return "ERROR", position
 
    while position < len(tokens):
 
        if is_operator(tokens, position, ("*", "/", "%")):
            operator = tokens[position][1]
 
            right, position = parse_negative(tokens, position + 1)
 
            if right == "ERROR":
                return "ERROR", position
 
            left = (operator, left, right)
 
        elif tokens[position][0] == "NUM":
            right, position = parse_negative(tokens, position)
 
            if right == "ERROR":
                return "ERROR", position
 
            left = ("*", left, right)
 
        elif tokens[position][0] == "LPAREN":
            right, position = parse_negative(tokens, position)
 
            if right == "ERROR":
                return "ERROR", position
 
            left = ("*", left, right)
 
        else:
            break
 
    return left, position
 
 
def parse_addition_subtraction(tokens, position):
    left, position = parse_multiplication(tokens, position)
 
    if left == "ERROR":
        return "ERROR", position
 
    while position < len(tokens):
 
        if is_operator(tokens, position, ("+", "-")):
            operator = tokens[position][1]
 
            right, position = parse_multiplication(tokens, position + 1)
 
            if right == "ERROR":
                return "ERROR", position
 
            left = (operator, left, right)
 
        else:
            break
 
    return left, position
 
def calculate_tree(tree):
    if isinstance(tree, (int, float)):
        return tree

    if tree[0] == "neg":
        return -calculate_tree(tree[1])

    operator = tree[0]

    left = calculate_tree(tree[1])
    right = calculate_tree(tree[2])

    if operator == "+":
        return left + right

    if operator == "-":
        return left - right

    if operator == "*":
        return left * right

    if operator == "/":
        if right == 0:
            raise Exception("cannot divide by zero")
        return left / right

    if operator == "%":
        if right == 0:
            raise Exception("cannot divide by zero")
        return left % right

    if operator == "^":
        return left ** right

    raise Exception("unknown operator")

def format_number(number):
    if number.is_integer():
        return str(int(number))
 
    return str(number)
 
 
def make_tree_string(tree):
    if isinstance(tree, (int, float)):
        return format_number(tree)
 
    if tree[0] == "neg":
        return "(neg " + make_tree_string(tree[1]) + ")"
 
    return (
        "(" + tree[0] + " "
        + make_tree_string(tree[1]) + " "
        + make_tree_string(tree[2]) + ")"
    )
 
 
def make_token_string(tokens):
    if tokens == "ERROR":
        return "ERROR"
 
    token_list = []
 
    for token_type, value in tokens:
        if token_type == "END":
            token_list.append("[END]")
        else:
            token_list.append("[" + token_type + ":" + value + "]")
 
    return " ".join(token_list)
 
 
def format_result(result):
    if result == "ERROR":
        return "ERROR"
 
    if result.is_integer():
        return str(int(result))
 
    return str(round(result, 4))
 
 
def process_one_expression(expression):
    tokens = tokenize_expression(expression)
 
    if tokens == "ERROR":
        return "ERROR", "ERROR", "ERROR"
 
    token_string = make_token_string(tokens)
 
    tree, position = parse_addition_subtraction(tokens, 0)
 
    if tree == "ERROR":
        return "ERROR", token_string, "ERROR"
 
    if position != len(tokens) - 1:
        return "ERROR", token_string, "ERROR"
 
    try:
        result = calculate_tree(tree)
    except:
        result = "ERROR"
 
    if result == "ERROR":
        return make_tree_string(tree), token_string, "ERROR"
 
    return make_tree_string(tree), token_string, result
 
 
def write_output(file, expression, tree, tokens, result):
    file.write("Input: " + expression + "\n")
    file.write("Tree: " + tree + "\n")
    file.write("Tokens: " + tokens + "\n")
    file.write("Result: " + format_result(result) + "\n")
    file.write("\n")
 
 
def evaluate_file(input_path: str):
    results = []
 
    folder = os.path.dirname(input_path)
    output_path = os.path.join(folder, "output.txt")
 
    try:
        with open(input_path, "r") as file:
            expressions = file.readlines()
    except:
        print("Input file was not found.")
        return results
 
    with open(output_path, "w") as file:
 
        for expression in expressions:
            expression = expression.rstrip("\r\n")
 
            tree, tokens, result = process_one_expression(expression)
 
            results.append({
                "input": expression,
                "tree": tree,
                "tokens": tokens,
                "result": result
            })
 
            write_output(file, expression, tree, tokens, result)
 
    return results
 
 
if __name__ == "__main__":
    evaluate_file("input.txt")
   
    print("Your Question 2: Expression Evaluation has been finished.")