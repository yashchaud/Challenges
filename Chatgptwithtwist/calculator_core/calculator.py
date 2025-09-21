import re
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

memory_stack = []
current_result = 0.0

@dataclass
class CalculationResult:
    result: float
    expression: str
    original_query: str
    timestamp: datetime
    operation_type: str

    def __str__(self):
        return f"{self.result}"


def calculate(query: str) -> CalculationResult:
    global current_result, memory_stack

    query = query.lower().strip()
    operation_type, numbers = parse_user_query(query)

    operations = {
        'add': add_numbers,
        'subtract': subtract_numbers,
        'multiply': multiply_numbers,
        'divide': divide_numbers,
        'previous': get_previous_result,
        'sum_all': sum_all_results,
        'clear': clear_memory
    }

    if operation_type in operations:
        result = operations[operation_type](numbers)
    else:
        result = evaluate_math_expression(query)
        operation_type = "expression"

    calc_result = CalculationResult(
        result=result,
        expression=build_readable_expression(operation_type, numbers),
        original_query=query,
        timestamp=datetime.now(),
        operation_type=operation_type
    )

    memory_stack.append(calc_result)
    current_result = result
    return calc_result


def parse_user_query(query: str) -> tuple[str, List[float]]:
    numbers = extract_numbers_from_text(query)

    if any(word in query for word in ['add', 'plus', '+']):
        return 'add', numbers
    elif any(word in query for word in ['subtract', 'minus', '-']):
        return 'subtract', numbers
    elif any(word in query for word in ['multiply', 'times', '*', 'x']):
        return 'multiply', numbers
    elif any(word in query for word in ['divide', '/', 'divided']):
        return 'divide', numbers
    elif any(word in query for word in ['previous', 'last', 'result']):
        return 'previous', []
    elif any(word in query for word in ['sum', 'total', 'all']):
        return 'sum_all', []
    elif any(word in query for word in ['clear', 'reset']):
        return 'clear', []
    else:
        return 'expression', numbers


def extract_numbers_from_text(query: str) -> List[float]:
    number_pattern = r'-?\d+\.?\d*'
    matches = re.findall(number_pattern, query)
    return [float(match) for match in matches if match]


def build_readable_expression(operation: str, numbers: List[float]) -> str:
    if operation == 'add' and len(numbers) >= 2:
        return f"{numbers[0]} + {numbers[1]}"
    elif operation == 'subtract' and len(numbers) >= 2:
        return f"{numbers[0]} - {numbers[1]}"
    elif operation == 'multiply' and len(numbers) >= 2:
        return f"{numbers[0]} * {numbers[1]}"
    elif operation == 'divide' and len(numbers) >= 2:
        return f"{numbers[0]} / {numbers[1]}"
    elif operation == 'previous':
        return "previous_result"
    elif operation == 'sum_all':
        return "sum_of_all_results"
    else:
        return f"expression({numbers})"


def add_numbers(numbers: List[float]) -> float:
    global current_result
    if len(numbers) < 2:
        return current_result + (numbers[0] if numbers else 0)
    return sum(numbers)


def subtract_numbers(numbers: List[float]) -> float:
    global current_result
    if len(numbers) < 2:
        return current_result - (numbers[0] if numbers else 0)
    return numbers[0] - numbers[1]


def multiply_numbers(numbers: List[float]) -> float:
    global current_result
    if len(numbers) < 2:
        return current_result * (numbers[0] if numbers else 1)

    result = numbers[0]
    for num in numbers[1:]:
        result *= num
    return result


def divide_numbers(numbers: List[float]) -> float:
    global current_result
    if len(numbers) < 2:
        divisor = numbers[0] if numbers else 1
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        return current_result / divisor

    if numbers[1] == 0:
        raise ValueError("Cannot divide by zero")
    return numbers[0] / numbers[1]


def get_previous_result(numbers: List[float]) -> float:
    if not memory_stack:
        return 0
    return memory_stack[-1].result


def sum_all_results(numbers: List[float]) -> float:
    if not memory_stack:
        return 0
    return sum(calc.result for calc in memory_stack)


def clear_memory(numbers: List[float]) -> float:
    global current_result, memory_stack
    memory_stack.clear()
    current_result = 0
    return 0


def evaluate_math_expression(expression: str) -> float:
    global current_result
    try:
        safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        if safe_expr.strip():
            return float(eval(safe_expr))
        else:
            return current_result
    except:
        raise ValueError(f"Cannot evaluate expression: {expression}")


def get_history() -> List[CalculationResult]:
    return memory_stack.copy()


def get_last_result() -> float:
    return current_result


if __name__ == "__main__":
    print("Simple Calculator Test")
    print("=" * 30)

    result1 = calculate("add 12 and 14")
    print(f"add 12 and 14 = {result1}")

    result2 = calculate("multiply by 5")
    print(f"multiply by 5 = {result2}")

    result3 = calculate("subtract the previous")
    print(f"subtract the previous = {result3}")

    result4 = calculate("sum all")
    print(f"sum all = {result4}")

    print("\nCalculation History:")
    for i, calc_result in enumerate(get_history(), 1):
        print(f"{i}. {calc_result.original_query} = {calc_result.result}")