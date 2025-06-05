import unittest
from unittest.mock import MagicMock

class TestExample(unittest.TestCase):
    def test_example(self):
        self.assertEqual(1, 1)

def test_mock_example():
    mock = MagicMock()
    mock.return_value = 42
    assert mock() == 42

if __name__ == "__main__":
    unittest.main() 