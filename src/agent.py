from typing import Any, Dict, Optional

from src.tools import (
    CalculatorTool,
    TextAnalyzerTool,
    CSVAnalyzerTool,
    DataConverterTool,
    ReportGeneratorTool,
)
from src.utils import InputHandler, OutputHandler


class ResearchAgent:
    def __init__(self):
        self.calculator = CalculatorTool()
        self.text_analyzer = TextAnalyzerTool()
        self.csv_analyzer = CSVAnalyzerTool()
        self.data_converter = DataConverterTool()
        self.report_generator = ReportGeneratorTool()
        self.input_handler = InputHandler()
        self.output_handler = OutputHandler()
        self.session_results = {}

    def process(self, user_input: str) -> Dict[str, Any]:
        parsed = self.input_handler.parse_input(user_input)
        if "error" in parsed:
            return {"error": parsed["error"]}

        command = parsed["command"]
        argument = parsed["argument"]

        handlers = {
            "help": self._handle_help,
            "analyze": self._handle_analyze,
            "calculate": self._handle_calculate,
            "convert": self._handle_convert,
            "report": self._handle_report,
            "exit": self._handle_exit,
        }

        handler = handlers.get(command, self._handle_unknown)
        return handler(argument)

    def _handle_help(self, argument: str) -> Dict[str, Any]:
        commands = self.input_handler.get_supported_commands()
        self.output_handler.display_help(commands)
        return {"status": "success", "message": "Help displayed"}

    def _handle_calculate(self, argument: str) -> Dict[str, Any]:
        if not argument:
            return {"error": "No expression provided. Usage: calculate <expression> (e.g., 'calculate 5 + 3')"}
        result = self.calculator.calculate(argument)
        self.session_results["last_calculation"] = result
        return {"command": "calculate", "expression": argument, "result": result}

    def _handle_analyze(self, argument: str) -> Dict[str, Any]:
        if not argument:
            return {"error": "No file specified. Usage: analyze <file_path>"}

        ext = argument.lower()
        if ext.endswith(".csv"):
            result = self.csv_analyzer.analyze(argument)
        else:
            content = self.input_handler.read_file(argument)
            if isinstance(content, dict) and "error" in content:
                return content
            if isinstance(content, str):
                result = self.text_analyzer.analyze(content)
            else:
                result = self.text_analyzer.analyze(str(content))

        self.session_results["last_analysis"] = result
        return {"command": "analyze", "file": argument, "result": result}

    def _handle_convert(self, argument: str) -> Dict[str, Any]:
        if not argument:
            return {"error": "No file specified. Usage: convert <file_path>"}

        if argument.endswith(".csv"):
            result = self.data_converter.csv_to_json(argument)
        elif argument.endswith(".json"):
            result = self.data_converter.json_to_csv(argument)
        elif argument.endswith(".txt"):
            result = self.data_converter.convert_text_to_json(argument)
        else:
            return {"error": f"Unsupported file format: {argument}. Supported: .csv, .json, .txt"}

        self.session_results["last_conversion"] = result
        return {"command": "convert", "file": argument, "result": result}

    def _handle_report(self, argument: str) -> Dict[str, Any]:
        if not argument:
            return {"error": "No report title specified. Usage: report <title>"}

        if not self.session_results:
            return {"error": "No analysis results available. Run 'analyze' or 'calculate' first."}

        report = self.report_generator.generate_report(
            title=argument,
            analysis_results=self.session_results,
            conclusion=f"Generated report based on {len(self.session_results)} analysis components.",
        )

        report_file = f"report_{argument.lower().replace(' ', '_')}.json"
        export_result = self.report_generator.export_to_json(report, report_file)

        self.session_results["last_report"] = report
        return {
            "command": "report",
            "title": argument,
            "report": report,
            "export": export_result,
        }

    def _handle_exit(self, argument: str) -> Dict[str, Any]:
        return {"status": "exit", "message": "Exiting application."}

    def _handle_unknown(self, argument: str) -> Dict[str, Any]:
        return {"error": f"Unknown command."}
