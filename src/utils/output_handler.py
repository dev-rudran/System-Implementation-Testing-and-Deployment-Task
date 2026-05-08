import json
from typing import Any, Dict


class OutputHandler:
    def display_result(self, result: Any) -> None:
        if isinstance(result, dict):
            if "error" in result:
                print(f"[ERROR] {result['error']}")
            elif "message" in result:
                print(f"[OK] {result['message']}")
                for k, v in result.items():
                    if k != "message":
                        print(f"  {k}: {v}")
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))
        elif isinstance(result, list):
            for item in result:
                if isinstance(item, dict):
                    print(json.dumps(item, indent=2, ensure_ascii=False))
                else:
                    print(item)
                print("-" * 40)
        else:
            print(str(result))

    def display_help(self, commands: Dict[str, str]) -> None:
        print("\nAvailable commands:")
        print("-" * 60)
        for cmd, desc in commands.items():
            print(f"  {cmd:<15} {desc}")
        print()
        print("Usage examples:")
        print("  calculate 5 + 3")
        print("  analyze data/sample_data.csv")
        print("  convert data/sample_data.csv")
        print('  report "My Analysis"')
        print()

    def display_welcome(self) -> None:
        print("=" * 60)
        print("  AI-Assisted Data Analysis Agent")
        print("  Riga Technical University - Systems Analysis & Design")
        print("=" * 60)
        print('Type "help" for available commands or "exit" to quit.')
        print()

    def display_error(self, message: str) -> None:
        print(f"[ERROR] {message}")
