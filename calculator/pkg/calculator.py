# calculator.py

class Calculator:
    def __init__(self):
        # map operator symbol to the function that performs it
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        # operator precedence: higher number = higher priority
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
         # empty or whitespace-only expressions return None
        if not expression or expression.isspace():
            return None
        # split by spaces into tokens like ["3", "+", "4", "*", "2"]
        tokens = expression.strip().split()
        # evaluate infix expression using stacks
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = [] # stack of numeric values
        operators = [] # stack of operator symbols

        for token in tokens:
            if token in self.operators:
                # while top of operator stack has >= precedence, apply it first
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                # push current operator
                operators.append(token)
            else:
                try:
                    # push numeric value
                    values.append(float(token))
                except ValueError:
                    # token is neither operator nor number
                    raise ValueError(f"invalid token: {token}")
                
        # apply any remaining operators
        while operators:
            self._apply_operator(operators, values)

        # after evaluation, there should be exactly one value
        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
         # no-op if no operators (defensive)
        if not operators:
            return

        operator = operators.pop()
        # need two operands to apply a binary operator
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()  # right operand
        a = values.pop()  # left operand
         # compute and push result
        values.append(self.operators[operator](a, b))
