import unittest
import nubank

class tests(unittest.TestCase):
    def setUp(self):
        self.account = nubank.Account(0)

    def test_auth_transaction(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time, exceptions = self.account.maketransaction(200, "Nubank")

        self.assertEqual(self.account.history[0].amount, 200)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 300)
        self.assertEqual([], exceptions)

    def test_auth_transaction_notactive(self):
        self.account.availablelimit = 500 
        self.account.active = False
        self.account.history.clear()

        time, exceptions = self.account.maketransaction(200, "Nubank")

        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.availablelimit, 500)
        self.assertEqual(exceptions, ["account-not-activate"])

    def test_auth_transaction_first_transaction(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        _, exceptions = self.account.maketransaction(475, "Nubank")

        #operaction could not be completed, because the first transaction can't excede 90% of the available limit
        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.availablelimit, 500)
        self.assertEqual(exceptions, ["first-transaction-above-threshold"])

        self.account.maketransaction(25, "Nubank")
        time, exceptions = self.account.maketransaction(475, "Nubank")
        
        #now the operation can be completed, because it's isn't the first operation anymore
        self.assertEqual(self.account.history[0].amount, 475)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 0)
        self.assertEqual(exceptions, [])

    def test_auth_transaction_limit(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        _, exceptions = self.account.maketransaction(700, "Nubank")

        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.history, [])
        self.assertEqual(self.account.availablelimit, 500)
        self.assertEqual(exceptions, ["insuffcient-limit"])

    def test_auth_transaction_highfrequency(self):
        self.account.availablelimit = 2000 
        self.account.active = True
        self.account.history.clear()

        self.account.maketransaction(100, "Nubank")
        self.account.maketransaction(200, "Nubank2")
        time, exceptions = self.account.maketransaction(300, "Nubank3")

        self.assertEqual(self.account.history[0].amount, 300)
        self.assertEqual(self.account.history[0].merchant, "Nubank3")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 1400)
        self.assertEqual([], exceptions)

        _, exceptions = self.account.maketransaction(400, "Nubank4")

        self.assertEqual(self.account.history[0].amount, 300)
        self.assertEqual(self.account.history[0].merchant, "Nubank3")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 1400)
        self.assertEqual(["high-frequency-small-interval"], exceptions)


    def test_auth_transaction_doubledtransaction(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time, exceptions = self.account.maketransaction(200, "Nubank")

        self.assertEqual(self.account.history[0].amount, 200)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 300)
        self.assertEqual([], exceptions)

        _, exceptions = self.account.maketransaction(200, "Nubank")

        self.assertEqual(self.account.history[0].amount, 200)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 300)
        self.assertEqual(['doubled-transaction'], exceptions)

if __name__ == "__main__":
    unittest.main()