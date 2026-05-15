import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import tempfile
from src.tools.report_generator import ReportGeneratorTool


class TestReportGeneratorTool(unittest.TestCase):
    def setUp(self):
        self.generator = ReportGeneratorTool()

    def test_generate_report_structure(self):
        report = self.generator.generate_report(
            "Test Report",
            {"calculator": {"result": 42}, "analysis": {"word_count": 100}},
            "All tests passed.",
        )
        self.assertEqual(report["report_title"], "Test Report")
        self.assertIn("generated_at", report)
        self.assertEqual(len(report["findings"]), 2)
        self.assertEqual(report["conclusion"], "All tests passed.")

    def test_generate_report_error_handling(self):
        report = self.generator.generate_report(
            "Error Test",
            {"failing_component": {"error": "Something broke"}},
        )
        self.assertEqual(report["findings"][0]["status"], "error")

    def test_export_to_json(self):
        report = self.generator.generate_report("Export Test", {"calc": {"value": 10}})
        output = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        output.close()

        try:
            result = self.generator.export_to_json(report, output.name)
            self.assertIn("message", result)
            self.assertTrue(os.path.exists(output.name))
        finally:
            os.unlink(output.name)

    def test_export_to_text(self):
        report = self.generator.generate_report("Text Export Test", {"calc": {"value": 10}})
        output = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        output.close()

        try:
            result = self.generator.export_to_text(report, output.name)
            self.assertIn("message", result)
            self.assertTrue(os.path.exists(output.name))

            with open(output.name, "r") as f:
                content = f.read()
            self.assertIn("Text Export Test", content)
        finally:
            os.unlink(output.name)

    def test_empty_analysis_results(self):
        report = self.generator.generate_report("Empty", {})
        self.assertEqual(len(report["findings"]), 0)


if __name__ == "__main__":
    unittest.main()
