import datetime

class Account:
    def __init__(self, limit=0):
        self.__active = True #defines if this account is active or not
        self.__availablelimit = limit #limit of this account in integer
        self.__history = [] #list of transactions
    
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

    #turns the account active
    def activate(self):
        if not self.active:
            self.active = True
            print("This account is now active.")
        else:
            print("This account is alreadly active.")

    #turns the account inactive
    def inactivate(self):
        if self.active:
            self.active = False
            self.limit = 0
            print("This account is now inactive.")
        else:
            print("This account is alreadly inactive.")

    #sets a brand new limit to the account
    def setlimit(self, limit):
        if self.active:
            if limit <= 0:
                print("Can't set negative or nule limit.")
            elif limit > 5000:
                print("Can't set a limit over R$5000.")
            else:
                self.availablelimit = limit
                print(f"The limit for this account is now R${limit}.")
        else:
            print("This account is inactive, so it can't have a limit.")

    #verify if there's violations in a transaction
    def authtransaction(self, transaction):
        violations = [] #list that will store violations of business rules
        
        if not self.active: #the account must be active
            violations.append("account-not-activate")

        if not self.history: #the first transaction value can't take over 90% of the available limit
            if transaction.amount > self.availablelimit * 0.9 and transaction.amount < self.availablelimit:
                violations.append("first-transaction-above-threshold")
        
        #the transaction value can't be higher than the available limit
        if transaction.amount > self.availablelimit:
            violations.append("insuffcient-limit")

        limittime = transaction.time - datetime.timedelta(minutes=2) #defines a time interval
        counttime = 0 #counts how much transactions were made in this time interval
        countequal = 0 #counts how much equals transactions where made in this time interval
        for transfer in self.history: #starts verifying the transactions in the interval
            if transfer.time >= limittime: #if it's in the interval
                counttime += 1
                if transfer.amount == transaction.amount and transfer.merchant == transaction.merchant: #if it's equal the current transactios
                    countequal += 1
            else: break

        if counttime == 3: #the number of transactions made in the interval must not be greater than 3
            violations.append("high-frequency-small-interval")
        if countequal == 1: #there's must not have two identical transactions in the interval 
            violations.append("doubled-transaction")
        return violations

    #realizes a transaction
    def maketransaction(self, value, merchant):
        transaction = Transaction(value, merchant)
        exceptions = self.authtransaction(transaction) #make the verification in the current transaction
        #if there is no exceptions, the transaction can be done, else, it can't
        if not exceptions:
            self.history.insert(0, transaction)
            self.availablelimit -= value
            print("Transaction completed successfully.")
        else:
            for i in exceptions:
                print(i)
        return transaction.time, exceptions

    #shows transactions history in console
    def showtransactions(self):
        if self.history:
            for transaction in self.history:
                print( "Amount:", transaction.amount, "| Merchant:", transaction.merchant, "| Time:", transaction.time.strftime("%b/%d/%Y - %I:%M:%S %p\n"))
                return "printed transaction(s)"
        else:
            print("No transactions recorded.")
            return "no transaction to print"

    #shows account data in console
    def showaccount(self):
        yesno = 'Yes' if self.active else 'No'
        print("Active:", yesno)
        print("Available limit:", self.availablelimit)
        return f'{yesno} {self.availablelimit}'

class Transaction:
    def __init__(self, value, merchant):
        self.__amount = value #transaction value in integer
        self.__merchant = merchant #transaction destination merchant
        self.__time = datetime.datetime.now() #current time

    @property
    def amount(self):
        return self.__amount
    @property
    def merchant(self):
        return self.__merchant
    @property
    def time(self):
        return self.__time
    
    @amount.setter
    def amount(self, value):
        self.__amount = value
    @merchant.setter
    def merchant(self, value):
        self.__merchant = value
    @time.setter
    def time(self, value):
        self.__time = value