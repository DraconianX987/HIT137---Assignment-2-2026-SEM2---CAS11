# Question 2 (Gokul Shajan)

def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        char = expr[i]

        if char.isspace():
            i = i + 1
            continue

        if char.isdigit():
            j = i
            while j < n and expr[j].isdigit():
                j = j + 1
            if j < n and expr[j] == '.':
                if j + 1 < n and expr[j + 1].isdigit():
                    j = j + 1
                    while j < n and expr[j].isdigit():
                        j = j + 1
                else:
                    return None
            tokens.append(('NUM', expr[i:j]))
            i = j
            continue

        if char in '+-*/%^':
            tokens.append(('OP', char))
            i = i + 1
            continue

        if char == '(':
            tokens.append(('LPAREN', '('))
            i = i + 1
            continue

        if char == ')':
            tokens.append(('RPAREN', ')'))
            i = i + 1
            continue

        return None

    tokens.append(('END', ''))
    return tokens


def tokens_to_string(tokens):
    parts = []
    for token in tokens:
        token_type = token[0]
        token_value = token[1]
        if token_type == 'END':
            parts.append('[END]')
        else:
            parts.append(f'[{token_type}:{token_value}]')
    return " ".join(parts)


def parse_expr(tokens, pos):
    node, pos = parse_term(tokens, pos)
    while tokens[pos][0] == 'OP' and tokens[pos][1] in ('+', '-'):
        op = tokens[pos][1]
        pos = pos + 1
        right, pos = parse_term(tokens, pos)
        node = ('op', op, node, right)
    return node, pos


def parse_term(tokens, pos):
    node, pos = parse_unary(tokens, pos)
    while True:
        token_type = tokens[pos][0]
        token_value = tokens[pos][1]
        if token_type == 'OP' and token_value in ('*', '/', '%'):
            pos = pos + 1
            right, pos = parse_unary(tokens, pos)
            node = ('op', token_value, node, right)
        elif token_type == 'LPAREN':
            right, pos = parse_unary(tokens, pos)
            node = ('op', '*', node, right)
        else:
            break
    return node, pos


def parse_unary(tokens, pos):
    token_type = tokens[pos][0]
    token_value = tokens[pos][1]
    if token_type == 'OP' and token_value == '-':
        pos = pos + 1
        operand, pos = parse_unary(tokens, pos)
        return ('neg', operand), pos
    return parse_power(tokens, pos)


def parse_power(tokens, pos):
    node, pos = parse_primary(tokens, pos)
    token_type = tokens[pos][0]
    token_value = tokens[pos][1]
    if token_type == 'OP' and token_value == '^':
        pos = pos + 1
        right, pos = parse_unary(tokens, pos)
        node = ('op', '^', node, right)
    return node, pos


def parse_primary(tokens, pos):
    token_type = tokens[pos][0]
    token_value = tokens[pos][1]

    if token_type == 'NUM':
        return ('num', float(token_value)), pos + 1

    if token_type == 'LPAREN':
        pos = pos + 1
        node, pos = parse_expr(tokens, pos)
        if tokens[pos][0] != 'RPAREN':
            raise ValueError('missing closing bracket')
        pos = pos + 1
        return node, pos

    raise ValueError('expected a number, - or (')


def parse(tokens):
    node, pos = parse_expr(tokens, 0)
    if tokens[pos][0] != 'END':
        raise ValueError('leftover tokens after expression')
    return node


def format_number(value):
    value = round(value, 4)
    if value == int(value):
        return str(int(value))
    else:
        return str(value)


def tree_to_string(node):
    kind = node[0]
    if kind == 'num':
        return format_number(node[1])
    if kind == 'neg':
        return f"(neg {tree_to_string(node[1])})"
    op = node[1]
    left = node[2]
    right = node[3]
    return f"({op} {tree_to_string(left)} {tree_to_string(right)})"


def eval_tree(node):
    kind = node[0]

    if kind == 'num':
        return node[1]

    if kind == 'neg':
        return -eval_tree(node[1])

    op = node[1]
    left = eval_tree(node[2])
    right = eval_tree(node[3])

    if op == '+':
        return left + right
    elif op == '-':
        return left - right
    elif op == '*':
        return left * right
    elif op == '/':
        if right == 0:
            raise ZeroDivisionError('cannot divide by zero')
        return left / right
    elif op == '%':
        if right == 0:
            raise ZeroDivisionError('cannot modulo by zero')
        return left % right
    elif op == '^':
        return left ** right


def evaluate_expression(expr):
    tokens = tokenize(expr)

    if tokens is None:
        return {"input": expr, "tree": "ERROR", "tokens": "ERROR", "result": "ERROR"}

    token_string = tokens_to_string(tokens)

    try:
        tree = parse(tokens)
    except (ValueError, IndexError):
        return {"input": expr, "tree": "ERROR", "tokens": token_string, "result": "ERROR"}

    tree_string = tree_to_string(tree)

    try:
        value = eval_tree(tree)
        result = round(value, 4)
    except (ZeroDivisionError, OverflowError, ValueError):
        result = "ERROR"

    return {"input": expr, "tree": tree_string, "tokens": token_string, "result": result}


def evaluate_file(input_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    results = []

    for line in lines:
        expr = line.rstrip('\r\n')
        if expr.strip() == '':
            continue
        results.append(evaluate_expression(expr))

    if '/' in input_path:
        output_path = input_path.rsplit('/', 1)[0] + '/output.txt'
    else:
        output_path = 'output.txt'

    blocks = []

    for r in results:
        if isinstance(r["result"], str):
            result_display = r["result"]
        else:
            result_display = format_number(r["result"])

        block = f"Input: {r['input']}\n"
        block = block + f"Tree: {r['tree']}\n"
        block = block + f"Tokens: {r['tokens']}\n"
        block = block + f"Result: {result_display}"
        blocks.append(block)

    with open(output_path, 'w') as f:
        f.write("\n\n".join(blocks) + "\n")

    return results


if __name__ == '__main__':
    evaluate_file('input.txt')