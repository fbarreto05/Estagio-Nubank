import unittest
import nubank

class test_auth(unittest.TestCase):
    def setUp(self):
        self.account = nubank.Account(0)

    def test_auth_transaction(self):
        if __name__ == "__main__": print("Testing regular case...")
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time, exceptions = self.account.maketransaction(200, "Nubank")
        #tudo está como previsto com esse caso de transação, então ele pode ser validado sem nenhuma exceção

        self.assertEqual(self.account.history[0].amount, 200)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual([], exceptions)
        
        self.assertEqual(self.account.availablelimit, 300)

    def test_auth_transaction_invalid_amount(self):
        if __name__ == "__main__": print("Testing invalid amount case...")
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time, exceptions = self.account.maketransaction(0, "Nubank")
        #a transação não foi feita, pois o valor é inválido

        self.assertEqual(self.account.history, [])
        self.assertEqual(["invalid-amount"], exceptions)
        
        self.assertEqual(self.account.availablelimit, 500)

    def test_auth_transaction_not_active(self):
        if __name__ == "__main__": print("Testing inactive account case...")
        self.account.availablelimit = 500 
        self.account.active = False
        self.account.history.clear()

        _, exceptions = self.account.maketransaction(200, "Nubank")
        #a transação não foi feita, pois a conta está inativa

        self.assertEqual(self.account.history, [])
        self.assertEqual(exceptions, ["account-not-activate"])
        
        self.assertEqual(self.account.availablelimit, 500)

    def test_auth_transaction_first_transaction(self):
        if __name__ == "__main__": print("Testing first transaction threshold case...")
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        _, exceptions = self.account.maketransaction(475, "Nubank")
        #a transação não foi feita, pois o valor da primeira operação não pode exceder 90% do limite disponível

        self.assertEqual(self.account.history, [])
        self.assertEqual(exceptions, ["first-transaction-above-threshold"])
        
        self.assertEqual(self.account.availablelimit, 500)

        time1, exceptions1 = self.account.maketransaction(25, "Nubank")
        time, exceptions = self.account.maketransaction(475, "Nubank")
        #agora a transação pode ser feita, pois ela não é mais a primeira operação

        #current operation                                            #first operation
        self.assertEqual(self.account.history[0].amount, 475);        self.assertEqual(self.account.history[1].amount, 25)
        self.assertEqual(self.account.history[0].merchant, "Nubank"); self.assertEqual(self.account.history[1].merchant, 'Nubank')
        self.assertEqual(self.account.history[0].time, time);         self.assertEqual(self.account.history[1].time, time1) 
        self.assertEqual(exceptions, []);                             self.assertEqual(exceptions1, [])
        
        self.assertEqual(self.account.availablelimit, 0)

    def test_auth_transaction_limit(self):
        if __name__ == "__main__": print("Testing unsufficient limit case...")
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        _, exceptions = self.account.maketransaction(700, "Nubank")
         #a transação não foi feita, pois o valor da transação excede o limite

        self.assertEqual(self.account.history, []) 
        self.assertEqual(exceptions, ["insuffcient-limit"])
        
        self.assertEqual(self.account.availablelimit, 500)

    def test_auth_transaction_highfrequency(self):
        if __name__ == "__main__": print("Testing high frequency case...")
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time1, exceptions1 = self.account.maketransaction(25, "Nubank")
        time2, exceptions2 = self.account.maketransaction(50, "Nubank")
        time, exceptions = self.account.maketransaction(100, "Nubank")
        #as transações foram feitas, pois o limite de transações no intervalo analisado continua admissível

        #primeira transação                                           segunda transação                                             última transação
        self.assertEqual(self.account.history[2].amount, 25);         self.assertEqual(self.account.history[1].amount, 50);         self.assertEqual(self.account.history[0].amount, 100)
        self.assertEqual(self.account.history[2].merchant, "Nubank"); self.assertEqual(self.account.history[1].merchant, "Nubank"); self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[2].time, time1);        self.assertEqual(self.account.history[1].time, time2);        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual([], exceptions1);                            self.assertEqual([], exceptions2);                            self.assertEqual([], exceptions)

        self.assertEqual(self.account.availablelimit, 325)

        _, exceptions = self.account.maketransaction(150, "Nubank")
        #a transação não foi feita, pois o limite de transações no intervalo analisado foi excedido

        self.assertEqual(self.account.history[0].amount, 100)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 325)
        self.assertEqual(["high-frequency-small-interval"], exceptions)


    def test_auth_transaction_doubledtransaction(self):
        if __name__ == "__main__": print("Testing doubled transaction case...")
        self.account.availablelimit = 500 
        self.account.active = True
        self.account.history.clear()

        time, exceptions = self.account.maketransaction(200, "Nubank")
        #tudo está como previsto com esse caso de transação, então ele pode ser validado sem nenhuma exceção

        self.assertEqual(self.account.history[0].amount, 200)
        self.assertEqual(self.account.history[0].merchant, "Nubank")
        self.assertEqual(self.account.history[0].time, time)
        self.assertEqual(self.account.availablelimit, 300)
        self.assertEqual([], exceptions)

        _, exceptions = self.account.maketransaction(200, "Nubank")
        #a transação não foi feita, pois existe outra transação idêntica no intervalo analisado

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