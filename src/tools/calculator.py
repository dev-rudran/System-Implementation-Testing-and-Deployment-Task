import math
from typing import Union


class CalculatorTool:
    def calculate(
        self, expression: str
    ) -> Union[str, float, int]:
        safe_ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "**": lambda a, b: a ** b,
            "//": lambda a, b: a // b,
            "%": lambda a, b: a % b,
        }

        expression = expression.strip()

        if expression.lower().startswith("sqrt"):
            num = float(expression[4:].strip().lstrip("(").rstrip(")"))
            return math.sqrt(num)

        if expression.lower().startswith("round"):
            inner = expression[5:].strip().lstrip("(").rstrip(")")
            parts = [p.strip() for p in inner.split(",")]
            num = float(parts[0])
            decimals = int(parts[1]) if len(parts) > 1 else 0
            return round(num, decimals)

        tokens = expression.split()
        if len(tokens) == 3:
            a, op, b = tokens
            a, b = float(a), float(b)
            if op in safe_ops:
                try:
                    result = safe_ops[op](a, b)
                except ZeroDivisionError:
                    return "Error: Division by zero"
                if isinstance(result, float) and result == int(result):
                    return int(result)
                return result

        try:
            result = eval(expression, {"__builtins__": {}}, {"math": math})
            if isinstance(result, float) and result == int(result):
                return int(result)
            return result
        except Exception as e:
            return f"Error: {e}"
