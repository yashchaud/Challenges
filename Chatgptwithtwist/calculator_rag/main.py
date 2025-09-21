from database import setup_database, get_embedding_model
from calculator import process_query


def main():
    print("Simple RAG Calculator")
    print("=" * 30)

    if not setup_database():
        print("Failed to setup database. Exiting.")
        return

    print("Initializing AI model...")
    get_embedding_model()

    print("Ready! Try commands like:")
    print("- 'ram has 5kg'")
    print("- 'sita takes 1kg from ram'")
    print("- 'ram gives 1kg to sita'")
    print("- 'ram balance'")
    print("- 'search ram transactions'")
    print("- 'undo ram last'")
    print()

    while True:
        try:
            user_input = input("Calculator> ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            result = process_query(user_input)
            print(result)
            print()

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()