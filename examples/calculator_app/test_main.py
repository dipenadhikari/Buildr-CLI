import unittest

from main import calculate


class CalculatorTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate(12, "+", 8), 20)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            calculate(1, "/", 0)


if __name__ == "__main__":
    unittest.main()

