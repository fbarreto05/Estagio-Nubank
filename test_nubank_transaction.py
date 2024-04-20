import unittest
import nubank
from unittest.mock import patch

class TestTransaction(unittest.TestCase):
    @patch('datetime.datetime')
    def test_init(self, datetime_now_mock):
        instance = None
        self.assertEqual(None, instance)
        datetime_now_mock.now.return_value = 'Time'
        instance = nubank.Transaction(2500, 'Merchant')
        self.assertEqual(2500, instance.amount)
        self.assertEqual('Merchant', instance.merchant)
        self.assertEqual('Time', instance.time)

if __name__ == '__main__':
    unittest.main()