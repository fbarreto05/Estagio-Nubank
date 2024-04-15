import datetime

class Account:
    def __init__(limit):
        __active = True
        __availablelimit = limit
        __history = []

class Transaction:
    def __init__(value, merchant):
        __ammount = value
        __merchant = merchant
        __time = datetime.datetime.now()
