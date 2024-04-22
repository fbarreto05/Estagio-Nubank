import unittest
import nubank
from unittest.mock import patch
from nubank import Transaction

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = nubank.Account()
    
    def test_activate_inactive(self):
        self.account.active = False
        self.assertFalse(self.account.active)
        self.account.activate()
        self.assertTrue(self.account.active)

    def test_activate_active(self):
        self.account.active = True
        self.assertTrue(self.account.active)
        self.account.activate()
        self.assertTrue(self.account.active)

    def test_inactivate_active(self):
        self.account.active = True
        self.assertTrue(self.account.active)
        self.account.inactivate()
        self.assertFalse(self.account.active)

    def test_inactivate_inactive(self):
        self.account.active = False
        self.assertFalse(self.account.active)
        self.account.inactivate()
        self.assertFalse(self.account.active)

    def test_set_limit(self):
        self.account.availablelimit = 0
        self.assertEqual(0, self.account.availablelimit)
        self.account.setlimit(2500)
        self.assertEqual(2500, self.account.availablelimit)

    def test_set_limit_out_of_range(self):
        self.account.availablelimit = 0
        self.assertEqual(0, self.account.availablelimit)
        self.account.setlimit(7500)
        self.assertEqual(0, self.account.availablelimit)
        self.account.setlimit(-2500)
        self.assertEqual(0, self.account.availablelimit)

    @patch("nubank.Transaction")
    def test_maketransaction(self, transaction_mock):
        self.account.active = True
        self.account.availablelimit = 2500
        self.account.history.clear()

        self.account.maketransaction(500, "Merchant")
        
        transaction_mock.assert_called_once_with(500, "Merchant")
        self.assertEqual(transaction_mock.return_value.amount, self.account.history[0].amount)
        self.assertEqual(transaction_mock.return_value.merchant, self.account.history[0].merchant)
        self.assertEqual(transaction_mock.return_value.time, self.account.history[0].time)
        self.assertEqual(2000, self.account.availablelimit)

    @patch("nubank.Transaction")
    def test_maketransacation_unavailablelimit(self, transaction_mock):
        self.account.active = True
        self.account.availablelimit = 2500
        self.account.history.clear()

        self.account.maketransaction(3000, "Merchant")
        
        transaction_mock.assert_not_called()
        self.assertEqual([], self.account.history)
        self.assertEqual([], self.account.history)
        self.assertEqual([], self.account.history)
        self.assertEqual(2500, self.account.availablelimit)

    @patch("nubank.Transaction")
    def test_maketransacation_inactive(self, transaction_mock):
        self.account.active = False
        self.account.availablelimit = 2500
        self.account.history.clear()

        ret = self.account.maketransaction(500, "Merchant")
        
        transaction_mock.assert_not_called()
        self.assertEqual([], self.account.history)
        self.assertEqual([], self.account.history)
        self.assertEqual([], self.account.history)
        self.assertEqual(2500, self.account.availablelimit)
        self.assertEqual("inactive account", ret)

    @patch("nubank.Transaction")
    def test_showTransactions(self, transaction_mock):
        self.account.active = True
        self.account.availablelimit = 2500
        self.account.history.insert(0, transaction_mock.return_value)

        ret = self.account.showtransactions()

        self.assertEqual('printed transaction(s)', ret)

    @patch("nubank.Transaction")
    def test_dontshowTransactions(self, transaction_mock):
        self.account.active = True
        self.account.availablelimit = 2500
        self.account.history.clear()

        ret = self.account.showtransactions()

        self.assertEqual('no transaction to print', ret)

    def test_showAccount(self):
        self.account.active = True
        self.account.availablelimit = 2500
        
        ret = self.account.showaccount()

        self.assertEqual('Yes 2500', ret)

        self.account.active = False
        self.account.availablelimit = 2500

        ret = self.account.showaccount()

        self.assertEqual('No 2500', ret)
    

        
if __name__ == '__main__':
    unittest.main()
