def calculate(left: float, operator: str, right: float) -> float:
    operations = {
        "+": lambda: left + right,
        "-": lambda: left - right,
        "*": lambda: left * right,
        "/": lambda: left / right,
    }
    if operator not in operations:
        raise ValueError("Operator must be one of: +, -, *, /")
    if operator == "/" and right == 0:
        raise ValueError("Cannot divide by zero")
    return operations[operator]()


if __name__ == "__main__":
    print(calculate(12, "+", 8))

