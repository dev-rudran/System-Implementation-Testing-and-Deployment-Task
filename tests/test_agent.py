import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch
from src.agent import ResearchAgent


class TestResearchAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ResearchAgent()

    def test_process_calculate(self):
        result = self.agent.process("calculate 5 + 3")
        self.assertNotIn("error", result)
        self.assertEqual(result["result"], 8)

    def test_process_calculate_no_arg(self):
        result = self.agent.process("calculate")
        self.assertIn("error", result)

    def test_process_help(self):
        result = self.agent.process("help")
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")

    def test_process_unknown_command(self):
        result = self.agent.process("invalidcommand")
        self.assertIn("error", result)

    def test_process_exit(self):
        result = self.agent.process("exit")
        self.assertEqual(result["status"], "exit")

    def test_process_empty_input(self):
        result = self.agent.process("")
        self.assertIn("error", result)

    def test_process_analyze_csv_file_not_found(self):
        result = self.agent.process("analyze nonexistent.csv")
        self.assertIn("error", result["result"])

    def test_process_analyze_no_arg(self):
        result = self.agent.process("analyze")
        self.assertIn("error", result)

    def test_process_convert_no_arg(self):
        result = self.agent.process("convert")
        self.assertIn("error", result)

    def test_process_report_no_arg(self):
        result = self.agent.process("report")
        self.assertIn("error", result)

    def test_process_report_no_results(self):
        result = self.agent.process("report Test")
        self.assertIn("error", result)

    def test_session_results_tracking(self):
        self.agent.process("calculate 10 + 20")
        self.assertIn("last_calculation", self.agent.session_results)
        self.assertEqual(self.agent.session_results["last_calculation"], 30)

    def test_process_convert_unsupported(self):
        result = self.agent.process("convert test.xyz")
        self.assertIn("error", result)

    def test_analyze_text_file(self):
        import tempfile
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
        tmp.write("Hello world. This is a test.")
        tmp.close()
        try:
            result = self.agent.process(f"analyze {tmp.name}")
            self.assertNotIn("error", result)
            self.assertEqual(result["result"]["word_count"], 6)
        finally:
            os.unlink(tmp.name)


if __name__ == "__main__":
    unittest.main()
