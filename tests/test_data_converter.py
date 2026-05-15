import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import tempfile
import json
from src.tools.data_converter import DataConverterTool


class TestDataConverterTool(unittest.TestCase):
    def setUp(self):
        self.converter = DataConverterTool()

    def test_csv_to_json(self):
        csv_file = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        csv_file.write("Name,Age\nAnna,22\nJanis,21\n")
        csv_file.close()
        json_output = csv_file.name.replace(".csv", ".json")

        try:
            result = self.converter.csv_to_json(csv_file.name, json_output)
            self.assertIn("records_converted", result)
            self.assertEqual(result["records_converted"], 2)
            self.assertTrue(os.path.exists(json_output))

            with open(json_output, "r") as f:
                data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["Name"], "Anna")
        finally:
            os.unlink(csv_file.name)
            if os.path.exists(json_output):
                os.unlink(json_output)

    def test_json_to_csv(self):
        json_file = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        json.dump([{"Name": "Anna", "Age": 22}, {"Name": "Janis", "Age": 21}], json_file)
        json_file.close()
        csv_output = json_file.name.replace(".json", ".csv")

        try:
            result = self.converter.json_to_csv(json_file.name, csv_output)
            self.assertIn("records_converted", result)
            self.assertEqual(result["records_converted"], 2)
            self.assertTrue(os.path.exists(csv_output))
        finally:
            os.unlink(json_file.name)
            if os.path.exists(csv_output):
                os.unlink(csv_output)

    def test_csv_to_json_file_not_found(self):
        result = self.converter.csv_to_json("nonexistent.csv")
        self.assertIn("error", result)

    def test_json_to_csv_file_not_found(self):
        result = self.converter.json_to_csv("nonexistent.json")
        self.assertIn("error", result)

    def test_text_to_json(self):
        text_file = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
        text_file.write("Hello\nWorld\n")
        text_file.close()
        json_output = text_file.name.replace(".txt", ".json")

        try:
            result = self.converter.convert_text_to_json(text_file.name, json_output)
            self.assertIn("message", result)
            self.assertTrue(os.path.exists(json_output))

            with open(json_output, "r") as f:
                data = json.load(f)
            self.assertEqual(data["line_count"], 2)
        finally:
            os.unlink(text_file.name)
            if os.path.exists(json_output):
                os.unlink(json_output)

    def test_unsupported_format_handling(self):
        result = self.converter.csv_to_json("test.xyz")
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
