import json
import os
from typing import Any, Dict, Union


class InputHandler:
    def __init__(self):
        self.supported_commands = {
            "analyze": "Analyze a CSV or text file",
            "calculate": "Perform a mathematical calculation",
            "convert": "Convert data between formats (CSV/JSON)",
            "report": "Generate a structured report",
            "help": "Show available commands",
            "exit": "Exit the application",
        }

    def get_supported_commands(self) -> Dict[str, str]:
        return dict(self.supported_commands)

    def parse_input(self, user_input: str) -> Dict[str, Any]:
        if not user_input or not user_input.strip():
            return {"error": "No input provided."}

        user_input = user_input.strip()

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        if command not in self.supported_commands:
            return {
                "command": "unknown",
                "original": user_input,
                "error": f"Unknown command '{command}'. Type 'help' for available commands.",
            }

        return {"command": command, "argument": argument, "original": user_input}

    def read_file(self, file_path: str) -> Union[str, Dict]:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            return {"error": f"Failed to read file: {e}"}
