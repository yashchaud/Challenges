from calculator import calculate, get_history


def start_calculator():
    print("🧮 Simple Calculator with Memory")
    print("=" * 40)
    print("Try commands like:")
    print("- 'add 12 and 14'")
    print("- 'multiply by 5'")
    print("- 'subtract previous'")
    print("- 'sum all'")
    print("- 'history' to see all calculations")
    print("- 'quit' to exit")
    print()

    while True:
        try:
            user_input = input("Calculator> ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            elif user_input.lower() == 'history':
                show_calculation_history()
                continue

            elif user_input.lower() == 'help':
                show_help_menu()
                continue

            elif not user_input:
                continue

            result = calculate(user_input)
            print(f"Result: {result}")

        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


def show_calculation_history():
    print("\nCalculation History:")
    history = get_history()
    if not history:
        print("No calculations yet.")
    else:
        for i, calc_result in enumerate(history, 1):
            print(f"{i}. {calc_result.original_query} = {calc_result.result}")
    print()


def show_help_menu():
    print("\nAvailable operations:")
    print("- Addition: 'add 5 and 3', '5 + 3'")
    print("- Subtraction: 'subtract 8 from 10', '10 - 8'")
    print("- Multiplication: 'multiply 4 by 7', '4 * 7'")
    print("- Division: 'divide 15 by 3', '15 / 3'")
    print("- Memory: 'previous', 'sum all', 'clear'")
    print()


if __name__ == "__main__":
    start_calculator()