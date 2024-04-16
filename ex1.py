import datetime

class Account:
    def __init__(self, limit):
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

    #deleters
    @active.deleter
    def active(self):
        del self.__active
    @availablelimit.deleter
    def availablelimit(self):
        del self.__availablelimit
    @history.deleter
    def history(self):
        self.__history

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
            print("This account is inactive, so it can not have a limit.")

    #realizes a transaction
    def maketransaction(self, value, merchant):
        if self.active:
            if self.availablelimit < value:
                print("Insufficient limit to make the transaction.")
            transaction = Transaction(value, merchant)
            self.history.insert(0, transaction)
            self.availablelimit -= value
            print("Transaction completed successfully.")
        else:
            print("This account is inactive, so it can not make transactions.")

    #show transactions history
    def showtransactions(self):
        if self.history:
            for transaction in self.history:
                print( "Ammount:", transaction.ammount, "| Merchant:", transaction.merchant, "| Time:", transaction.time.strftime("%b/%d/%Y - %I:%M:%S %p\n"))
        else:
            print("No transactions recorded.")

    #show account data
    def showaccount(self):
        yesno = 'Yes' if self.active else 'No'
        print("Active:", yesno)
        print("Available limit:", self.availablelimit)

class Transaction:
    def __init__(self, value, merchant):
        self.__ammount = value #transaction value in integer
        self.__merchant = merchant #transaction destination merchant
        self.__time = datetime.datetime.now() #current time

    @property
    def ammount(self):
        return self.__ammount
    @property
    def merchant(self):
        return self.__merchant
    @property
    def time(self):
        return self.__time
    
    @ammount.setter
    def ammount(self, value):
        self.__ammount = value
    @merchant.setter
    def merchant(self, value):
        self.__merchant = value
    @time.setter
    def time(self, value):
        self.__time = value

    @ammount.deleter
    def ammount(self, value):
        del self.__ammount
    @merchant.deleter
    def merchant(self, value):
        del self.__merchant
    @time.deleter
    def time(self, value):
        del self.__time

#main()
if __name__ == '__main__':
    pass