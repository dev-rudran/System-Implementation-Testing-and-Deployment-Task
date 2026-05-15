import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import tempfile
from src.tools.csv_analyzer import CSVAnalyzerTool


class TestCSVAnalyzerTool(unittest.TestCase):
    def setUp(self):
        self.analyzer = CSVAnalyzerTool()
        self.temp_csv = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        self.temp_csv.write("Name,Age,Score\nAnna,22,95.5\nJanis,21,82.3\n")
        self.temp_csv.close()
        self.csv_path = self.temp_csv.name

    def tearDown(self):
        os.unlink(self.csv_path)

    def test_analyze_row_count(self):
        result = self.analyzer.analyze(self.csv_path)
        self.assertEqual(result["row_count"], 2)

    def test_analyze_column_count(self):
        result = self.analyzer.analyze(self.csv_path)
        self.assertEqual(result["column_count"], 3)

    def test_analyze_field_names(self):
        result = self.analyzer.analyze(self.csv_path)
        self.assertEqual(result["field_names"], ["Name", "Age", "Score"])

    def test_numeric_column_stats(self):
        result = self.analyzer.analyze(self.csv_path)
        self.assertIn("Score", result["numeric_columns"])
        self.assertAlmostEqual(result["numeric_columns"]["Score"]["avg"], 88.9)

    def test_file_not_found(self):
        result = self.analyzer.analyze("nonexistent.csv")
        self.assertIn("error", result)

    def test_search_found(self):
        result = self.analyzer.search(self.csv_path, "Name", "Anna")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["Age"], "22")

    def test_search_not_found(self):
        result = self.analyzer.search(self.csv_path, "Name", "Unknown")
        self.assertIn("message", result[0])

    def test_empty_csv(self):
        empty_csv = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        empty_csv.write("Name,Age\n")
        empty_csv.close()
        result = self.analyzer.analyze(empty_csv.name)
        self.assertIn("error", result)
        os.unlink(empty_csv.name)


if __name__ == "__main__":
    unittest.main()
