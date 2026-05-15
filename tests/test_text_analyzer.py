import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from src.tools.text_analyzer import TextAnalyzerTool


class TestTextAnalyzerTool(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextAnalyzerTool()

    def test_word_count(self):
        result = self.analyzer.analyze("Hello world")
        self.assertEqual(result["word_count"], 2)

    def test_character_count(self):
        result = self.analyzer.analyze("Hi")
        self.assertEqual(result["character_count"], 2)

    def test_character_count_no_spaces(self):
        result = self.analyzer.analyze("Hello world")
        self.assertEqual(result["character_count_no_spaces"], 10)

    def test_sentence_count_single(self):
        result = self.analyzer.analyze("This is a test.")
        self.assertEqual(result["sentence_count"], 1)

    def test_sentence_count_multiple(self):
        result = self.analyzer.analyze("First. Second. Third.")
        self.assertEqual(result["sentence_count"], 3)

    def test_unique_word_count(self):
        result = self.analyzer.analyze("the cat and the dog")
        self.assertEqual(result["unique_word_count"], 4)

    def test_top_words(self):
        result = self.analyzer.analyze("a a a b b c")
        top = result["top_words"]
        self.assertEqual(top[0][0], "a")
        self.assertEqual(top[0][1], 3)

    def test_average_word_length(self):
        result = self.analyzer.analyze("hello world")
        self.assertEqual(result["average_word_length"], 5.0)

    def test_empty_text(self):
        result = self.analyzer.analyze("")
        self.assertIn("error", result)

    def test_none_text(self):
        result = self.analyzer.analyze(None)
        self.assertIn("error", result)

    def test_text_with_punctuation(self):
        result = self.analyzer.analyze("Hello, world! How are you?")
        self.assertEqual(result["word_count"], 5)
        self.assertEqual(result["sentence_count"], 2)


if __name__ == "__main__":
    unittest.main()
