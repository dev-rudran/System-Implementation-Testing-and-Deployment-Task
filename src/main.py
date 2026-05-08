import sys
from src.agent import ResearchAgent
from src.utils import OutputHandler


def main():
    agent = ResearchAgent()
    output_handler = OutputHandler()

    output_handler.display_welcome()

    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue
        except (EOFError, KeyboardInterrupt):
            print()
            break

        result = agent.process(user_input)

        if isinstance(result, dict) and result.get("status") == "exit":
            print("Goodbye!")
            break

        output_handler.display_result(result)


if __name__ == "__main__":
    main()
