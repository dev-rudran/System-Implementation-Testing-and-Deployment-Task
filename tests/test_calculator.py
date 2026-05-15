import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from src.tools.calculator import CalculatorTool


class TestCalculatorTool(unittest.TestCase):
    def setUp(self):
        self.calc = CalculatorTool()

    def test_addition(self):
        result = self.calc.calculate("5 + 3")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calc.calculate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calc.calculate("6 * 7")
        self.assertEqual(result, 42)

    def test_division(self):
        result = self.calc.calculate("15 / 3")
        self.assertEqual(result, 5)

    def test_division_float(self):
        result = self.calc.calculate("10 / 3")
        self.assertAlmostEqual(result, 3.3333333333333335)

    def test_exponentiation(self):
        result = self.calc.calculate("2 ** 10")
        self.assertEqual(result, 1024)

    def test_modulo(self):
        result = self.calc.calculate("17 % 5")
        self.assertEqual(result, 2)

    def test_floor_division(self):
        result = self.calc.calculate("17 // 5")
        self.assertEqual(result, 3)

    def test_sqrt(self):
        result = self.calc.calculate("sqrt(16)")
        self.assertEqual(result, 4.0)

    def test_round(self):
        result = self.calc.calculate("round(3.14159, 2)")
        self.assertEqual(result, 3.14)

    def test_negative_numbers(self):
        result = self.calc.calculate("-5 + 3")
        self.assertEqual(result, -2)

    def test_invalid_expression(self):
        result = self.calc.calculate("")
        self.assertIsInstance(result, str)

    def test_zero_division(self):
        result = self.calc.calculate("5 / 0")
        self.assertIn("Error", str(result))


if __name__ == "__main__":
    unittest.main()
