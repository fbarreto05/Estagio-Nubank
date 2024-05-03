import datetime

class Account:
    def __init__(self, limit=0):
        self.__active = True #define se a conta está ativa ou não
        self.__availablelimit = limit #define o limite disponível na conta
        self.__history = [] #lista de transações realizadas
    
    #getters
    @property
    def active(self):
        return self.__active
    @property
    def availablelimit(self):
        return self.__availablelimit
    @property
    def history(self):
        return self.__history
    
    #setters
    @active.setter
    def active(self, value):
        self.__active = value
    @availablelimit.setter
    def availablelimit(self, value):
        self.__availablelimit = value
    @history.setter
    def history(self, value):
        self.__history = value

    #ativa a conta
    def activateORinactivate(self):
        if not self.active:
            self.active = True
            if __name__ == "__main__": print("This account is now active.")
        else:
            self.active = False
            if __name__ == "__main__": print("This account is now inactive.")

    #define um novo limite para a conta
    def setlimit(self, limit):
        if limit <= 0:
            if __name__ == "__main__": print("Can't set a negative or nule limit.")
        elif limit > 5000:
            if __name__ == "__main__": print("Can't set a limit above R$5000.")
        else:
            self.availablelimit = limit
            if __name__ == "__main__": print(f"The limit for this account is now ${limit}.")

    #verifica se há violações na transação
    def authtransaction(self, transaction):
        violations = [] #lista que irá armazenar violações das regras de negócio
        
        if transaction.amount <= 0: #a conta deve estar ativa
            violations.append("invalid-amount")

        if not self.active: #a conta deve estar ativa
            violations.append("account-not-activate")

        if not self.history: #o valor da primeira transação não pode estar acima de 90% do limite disponível
            if transaction.amount > self.availablelimit * 0.9 and transaction.amount < self.availablelimit:
                violations.append("first-transaction-above-threshold")
        
        #o valor da transação não pode ser maior que o limite disponível
        if transaction.amount > self.availablelimit:
            violations.append("insuffcient-limit")

        limittime = transaction.time - datetime.timedelta(minutes=2) #define o intervalo de busca no histórico de transferências (até 2 minutos atrás da transferência atual)
        counttime = 0 #conta quantas transações foram feitas nesse intervalo
        countequal = 0 #conta quantas transações idênticas foram feitas nesse intervalo
        for transfer in self.history: #começa a verificar o histórico de transferências
            if transfer.time >= limittime: #se está no intervalo:
                counttime += 1
                if transfer.amount == transaction.amount and transfer.merchant == transaction.merchant: #se é idêntica à transferência atual
                    countequal += 1
            else: break #quebra quando houver uma transferência fora do intervalo

        if counttime == 3: #o número de transferências feitas no intervalo não deve ser maior que 3
            violations.append("high-frequency-small-interval")
        if countequal == 1: #não devem haver duas transferências idênticas no intervalo
            violations.append("doubled-transaction")
        return violations

    #realizes a transaction
    def maketransaction(self, value, merchant):
        transaction = Transaction(value, merchant)
        exceptions = self.authtransaction(transaction) #faz a verificação na transação atual e capta suas exceções
        #se não houverem exceções, a transação pode ser concluída
        if not exceptions:
            self.history.insert(0, transaction)
            self.availablelimit -= value
            if __name__ == "__main__": print("Transaction completed successfully.")
        #se houverem, a transação não é realizada
        else:
            if __name__ == "__main__": print("Transaction could not be completed.")
        return transaction.time, exceptions

    #mostra o histórico de transações
    def showtransactions(self):
        if self.history:
            for transaction in self.history:
                if __name__ == "__main__": print( "Amount:", transaction.amount, "| Merchant:", transaction.merchant, "| Time:", transaction.time.strftime("%b/%d/%Y - %I:%M:%S %p\n"))
        else:
            if __name__ == "__main__": print("\nNo transactions recorded.")

    #mostra detalhes da conta
    def showaccount(self):
        yesno = 'Yes' if self.active else 'No'
        if __name__ == "__main__": print("Active:", yesno, "\nAvailable limit:", self.availablelimit)
        return f'{yesno} {self.availablelimit}'

class Transaction:
    def __init__(self, value, merchant):
        self.__amount = value #valor da transação
        self.__merchant = merchant #destinatário da transação
        self.__time = datetime.datetime.now() #horário da transação

    #getters
    @property
    def amount(self):
        return self.__amount
    @property
    def merchant(self):
        return self.__merchant
    @property
    def time(self):
        return self.__time
    
    #setters
    @amount.setter
    def amount(self, value):
        self.__amount = value
    @merchant.setter
    def merchant(self, value):
        self.__merchant = value
    @time.setter
    def time(self, value):
        self.__time = value

class Interact:
    @staticmethod
    def menu(client):
        user_input = 1
        while user_input!=0:
            if __name__ == "__main__": print("\nNubank transaction system\n"
                                             "----------------------------------------\n"
                                             "Enter an option: \n"
                                             "1 - Show account data\n"
                                             "2 - Show transactions history\n"
                                             "3 - Make transaction\n"
                                             "4 - Change the available limit\n"
                                             "5 - Active/Inactive the account\n"
                                             "0 - Shut down the system\n")
            user_input = input()
            print()
            match user_input:
                case '1':
                    if __name__ == "__main__": print("Account: ")
                    client.showaccount()

                case '2':
                    if __name__ == "__main__": print("Transactions: ")
                    client.showtransactions()

                case '3':
                    while True:
                        transaction_value = input("Enter the transaction amount: ")
                        try:
                            transaction_value = int(transaction_value)
                            break
                        except ValueError: 
                            if __name__ == "__main__": print("Transaction amount must be an integer")
                    transaction_merchant = input("Enter the transaction merchant: ")
                    print()
                    _, exceptions = client.maketransaction(transaction_value, transaction_merchant)
                    if __name__ == "__main__": print("Account: ")
                    client.showaccount()
                    if exceptions:
                        if __name__ == "__main__": print("Exceptions: ")
                        for i in exceptions:
                            if __name__ == "__main__": print(i)

                case '4':
                    while True:
                        limit_value = input("Enter the limit amount: ")
                        try:
                            limit_value = int(limit_value)
                            print()
                            break
                        except:
                            if __name__ == "__main__": print("Limit amount must be an integer")
                    client.setlimit(limit_value)

                case '5':
                    client.activateORinactivate()

                case '0':
                    if __name__ == "__main__": print("Shutting down the system...")

                case _:
                    if __name__ == "__main__": print("Invalid option, enter again")
    
if __name__ == "__main__":
    user = Account()
    Interact.menu(user)