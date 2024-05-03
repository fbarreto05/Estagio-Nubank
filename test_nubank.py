import unittest
import nubank

class test_auth(unittest.TestCase):
    def setUp(self):
        self.account = nubank.Account(0)

    def test_auth_transaction(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time, exceptions = self.account.maketransaction(200, "Nubank")
        #everything's right with this transaction case, so it can be validated without exceptions

        self.assertEqual(self.account.history[0].amount, 200)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual([], exceptions)
        
        self.assertEqual(self.account.availablelimit, 300)

    def test_auth_transaction_not_active(self):
        self.account.availablelimit = 500 
        self.account.active = False
        self.account.history.clear()

        _, exceptions = self.account.maketransaction(200, "Nubank")
        #the account is inactive, so the transaction can't be validated and a exception is capted

        self.assertEqual(self.account.history, [])
        self.assertEqual(exceptions, ["account-not-activate"])
        
        self.assertEqual(self.account.availablelimit, 500)

    def test_auth_transaction_first_transaction(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        _, exceptions = self.account.maketransaction(475, "Nubank")
        #the first transaction exceds 90% of the limit, so the transaction can't be validated and a exception is capted

        self.assertEqual(self.account.history, [])
        self.assertEqual(exceptions, ["first-transaction-above-threshold"])
        
        self.assertEqual(self.account.availablelimit, 500)

        time1, exceptions1 = self.account.maketransaction(25, "Nubank")
        time, exceptions = self.account.maketransaction(475, "Nubank")
        #now the operation can be completed, because it's isn't the first operation anymore

        #current operation                                            #first operation
        self.assertEqual(self.account.history[0].amount, 475);        self.assertEqual(self.account.history[1].amount, 25)
        self.assertEqual(self.account.history[0].merchant, "Nubank"); self.assertEqual(self.account.history[1].merchant, 'Nubank')
        self.assertEqual(self.account.history[0].time, time);         self.assertEqual(self.account.history[1].time, time1) 
        self.assertEqual(exceptions, []);                             self.assertEqual(exceptions1, [])
        
        self.assertEqual(self.account.availablelimit, 0)

    def test_auth_transaction_limit(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        _, exceptions = self.account.maketransaction(700, "Nubank")
         #the transaction exceds the limit, so the transaction can't be validated and a exception is capted

        self.assertEqual(self.account.history, []) 
        self.assertEqual(exceptions, ["insuffcient-limit"])
        
        self.assertEqual(self.account.availablelimit, 500)

    def test_auth_transaction_highfrequency(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time1, exceptions1 = self.account.maketransaction(25, "Nubank")
        time2, exceptions2 = self.account.maketransaction(50, "Nubank")
        time, exceptions = self.account.maketransaction(100, "Nubank")
        #the transactions have been done, because it still in the limit admissed

        #first transaction                                            second transaction                                            last transaction
        self.assertEqual(self.account.history[2].amount, 25);         self.assertEqual(self.account.history[1].amount, 50);         self.assertEqual(self.account.history[0].amount, 100)
        self.assertEqual(self.account.history[2].merchant, "Nubank"); self.assertEqual(self.account.history[1].merchant, "Nubank"); self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[2].time, time1);        self.assertEqual(self.account.history[1].time, time2);        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual([], exceptions1);                            self.assertEqual([], exceptions2);                            self.assertEqual([], exceptions)

        self.assertEqual(self.account.availablelimit, 325)

        _, exceptions = self.account.maketransaction(150, "Nubank")
        #the transaction haven't been done, because it exceds the limit admissed

        self.assertEqual(self.account.history[0].amount, 100)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 325)
        self.assertEqual(["high-frequency-small-interval"], exceptions)


    def test_auth_transaction_doubledtransaction(self):
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time, exceptions = self.account.maketransaction(200, "Nubank")
        #everything's right with this transaction case, so it can be validated without exceptions

        self.assertEqual(self.account.history[0].amount, 200)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 300)
        self.assertEqual([], exceptions)

        _, exceptions = self.account.maketransaction(200, "Nubank")
        #everything's right with this transaction case, so it can be validated without exceptions

        self.assertEqual(self.account.history[0].amount, 200)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 300)
        self.assertEqual(['doubled-transaction'], exceptions)

        with self.assertRaises(IndexError):
            if self.account.history[1]:
                pass

if __name__ == "__main__":
    unittest.main()