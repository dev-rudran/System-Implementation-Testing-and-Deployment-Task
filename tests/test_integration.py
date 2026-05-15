import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import tempfile
import json
from src.agent import ResearchAgent
from src.tools.calculator import CalculatorTool
from src.tools.text_analyzer import TextAnalyzerTool
from src.tools.csv_analyzer import CSVAnalyzerTool
from src.tools.data_converter import DataConverterTool
from src.tools.report_generator import ReportGeneratorTool
from src.utils.input_handler import InputHandler
from src.utils.output_handler import OutputHandler


class TestIntegration(unittest.TestCase):
    def test_full_workflow_calculate_then_report(self):
        agent = ResearchAgent()
        calc_result = agent.process("calculate 15 * 3")
        self.assertEqual(calc_result["result"], 45)

        report_result = agent.process("report Calculation Results")
        self.assertNotIn("error", report_result)
        self.assertIn("report", report_result)
        self.assertEqual(report_result["report"]["report_title"], "Calculation Results")

    def test_full_workflow_analyze_csv_then_report(self):
        csv_file = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        csv_file.write("Product,Price,Quantity\nApple,1.20,50\nBanana,0.80,30\n")
        csv_file.close()

        try:
            agent = ResearchAgent()
            analyze_result = agent.process(f"analyze {csv_file.name}")
            self.assertNotIn("error", analyze_result)
            self.assertEqual(analyze_result["result"]["row_count"], 2)

            report_result = agent.process("report Product Analysis")
            self.assertNotIn("error", report_result)
            self.assertIn("report", report_result)
        finally:
            os.unlink(csv_file.name)

    def test_calculator_then_converter_independent(self):
        agent = ResearchAgent()
        agent.process("calculate 100 / 4")
        self.assertEqual(agent.session_results["last_calculation"], 25)

        csv_file = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        csv_file.write("City,Population\nRiga,632000\nJelgava,56000\n")
        csv_file.close()
        json_output = csv_file.name.replace(".csv", ".json")

        try:
            convert_result = agent.process(f"convert {csv_file.name}")
            self.assertNotIn("error", convert_result)
            self.assertTrue(os.path.exists(json_output))
        finally:
            os.unlink(csv_file.name)
            if os.path.exists(json_output):
                os.unlink(json_output)

    def test_text_analyzer_tool_directly(self):
        analyzer = TextAnalyzerTool()
        result = analyzer.analyze("Systems Analysis and Design is a course at RTU.")
        self.assertGreater(result["word_count"], 5)
        self.assertGreater(result["sentence_count"], 0)

    def test_report_generator_export_formats(self):
        generator = ReportGeneratorTool()
        report = generator.generate_report("Multi-format Test", {"calc": {"value": 99}})

        txt_output = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        txt_output.close()
        json_output = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        json_output.close()

        try:
            txt_result = generator.export_to_text(report, txt_output.name)
            self.assertIn("message", txt_result)

            json_result = generator.export_to_json(report, json_output.name)
            self.assertIn("message", json_result)

            with open(json_output.name, "r") as f:
                loaded = json.load(f)
            self.assertEqual(loaded["report_title"], "Multi-format Test")
        finally:
            os.unlink(txt_output.name)
            os.unlink(json_output.name)

    def test_data_conversion_roundtrip(self):
        converter = DataConverterTool()

        csv_file = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        csv_file.write("X,Y\n1,2\n3,4\n")
        csv_file.close()
        json_path = csv_file.name.replace(".csv", ".json")
        csv_roundtrip = csv_file.name.replace(".csv", "_roundtrip.csv")

        try:
            to_json = converter.csv_to_json(csv_file.name, json_path)
            self.assertEqual(to_json["records_converted"], 2)

            to_csv = converter.json_to_csv(json_path, csv_roundtrip)
            self.assertEqual(to_csv["records_converted"], 2)

            with open(csv_roundtrip, "r") as f:
                content = f.read()
            self.assertIn("X,Y", content)
            self.assertIn("1,2", content)
        finally:
            os.unlink(csv_file.name)
            if os.path.exists(json_path):
                os.unlink(json_path)
            if os.path.exists(csv_roundtrip):
                os.unlink(csv_roundtrip)

    def test_input_handler_parsing(self):
        handler = InputHandler()
        result = handler.parse_input("calculate 2 + 2")
        self.assertEqual(result["command"], "calculate")
        self.assertEqual(result["argument"], "2 + 2")

        result = handler.parse_input("")
        self.assertIn("error", result)

        result = handler.parse_input("unknown_command")
        self.assertIn("error", result)

    def test_output_handler_no_errors(self):
        handler = OutputHandler()
        try:
            handler.display_result({"status": "success", "message": "test"})
            handler.display_help({"cmd": "description"})
            handler.display_welcome()
            handler.display_error("test error")
        except Exception as e:
            self.fail(f"OutputHandler raised exception: {e}")


if __name__ == "__main__":
    unittest.main()
