Here's a Python script that tests the `add_numbers` function using Python's built-in `unittest` library.

```python
import unittest
from your_script_name import add_numbers  # replace this with your actual script name

class TestAddNumbers(unittest.TestCase):
    """
    This class consists of unittests for the function add_numbers.
    """
    
    def test_add_integers(self):
        """
        Test that the sum of two integers is calculated correctly.
        """
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)  # Expect: 2 + 3 = 5

    def test_add_floats(self):
        """
        Test that the sum of two floats is calculated correctly.
        """
        result = add_numbers(2.0, 3.5)
        self.assertAlmostEqual(result, 5.5)  # Expect: 2.0 + 3.5 = 5.5

    def test_add_mixed(self):
        """
        Test that the sum of an integer and a float is calculated correctly.
        """
        result = add_numbers(1, 2.5)
        self.assertAlmostEqual(result, 3.5)  # Expect: 1 + 2.5 = 3.5

    def test_add_negatives(self):
        """
        Test that the sum of negative numbers is calculated correctly.
        """
        result = add_numbers(-2, -5)
        self.assertEqual(result, -7)  # Expect: -2 + -5 = -7

    def test_type_error(self):
        """
        Test that a TypeError is raised when a non-numerical argument is passed.
        """
        with self.assertRaises(TypeError):
            add_numbers("2", 3)  # Raises TypeError as string is passed instead of number

    def test_add_zero(self):
        """
        Test that the sum of a number and zero is equal to that number.
        """
        self.assertEqual(add_numbers(5, 0), 5)  # Expect: 5
        self.assertEqual(add_numbers(0, 5), 5)  # Expect: 5

if __name__ == "__main__":
    unittest.main()
```

To execute the tests, save the code in a separate Python script (let's say `test_add_numbers.py`) in the same directory as your original script, then execute `test_add_numbers.py` directly. Note: Replace `your_script_name` with the actual name of your script where `add_numbers` function is defined.

Alternatively, you can run the test on the command line by navigating to the directory containing both scripts and executing `python -m unittest test_add_numbers`