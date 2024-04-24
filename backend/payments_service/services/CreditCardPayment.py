
from interfaces.PaymentInterface import PaymentInterface

class CreditCardPayment(PaymentInterface) : 
    
    def __init__(self, card_number, expiration_date, cvv):
        self.__card_number = card_number
        self.__expiration_date = expiration_date
        self.__cvv = cvv
        self.__balance = 100000

    def check_valid(self):
        return True

    def pay(self, amount):
        if self.check_valid() == False:
           return False
        
        # remove from credit card balance
        if self.__balance < amount:
            return False
        
        self.__balance -= amount    
        return True
        