import datetime

class Account:
    def __init__(self, limit):
        self.__active = True
        self.__availablelimit = limit
        self.__history = []

    @property
    def active(self):
        return self.__active
    @property
    def availablelimit(self):
        return self.__availablelimit
    @property
    def history(self):
        return self.__history
    
    @active.setter
    def active(self, value):
        self.__active = value
    @availablelimit.setter
    def availablelimit(self, value):
        self.__availablelimit = value
    @history.setter
    def history(self, value):
        self.__history = value

    @active.deleter
    def active(self):
        del self.__active
    @availablelimit.deleter
    def availablelimit(self):
        del self.__availablelimit
    @history.deleter
    def history(self):
        self.__history


class Transaction:
    def __init__(self, value, merchant):
        self.__ammount = value
        self.__merchant = merchant
        self.__time = datetime.datetime.now()

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

if __name__ == '__main__':
    pass