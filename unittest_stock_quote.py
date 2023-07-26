import unittest
from script_input import StockQuote

class TestStockQuote(unittest.TestCase):
    def setUp(self):
        self.sq = StockQuote()

    def test_set_symbols(self):
        # Test valid input
        self.assertTrue(self.sq.set_symbols(['AAPL', 'GOOG']))
        # Test invalid input
        self.assertFalse(self.sq.set_symbols(['123', '!@#']))

if __name__ == '__main__':
    unittest.main()
