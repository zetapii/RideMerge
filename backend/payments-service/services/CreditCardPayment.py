
from interfaces import PaymentInterface
from DAO import PaymentsDAO
from Entities import Payment

class CreditCardPayment(PaymentInterface) : 
    
    def __init__(self, card_number, expiration_date, cvv):
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.balance = 100000

    def check_valid(self):
        return True

    def pay(self, amount, driver_wallet):
        if self.check_valid() == False:
           return False
        
        # add to wallet of driver
        # remove from credit card balance
        if self.balance < amount:
            return False
        
        self.balance -= amount    
        return True
        
        # dao = PaymentsDAO()
        # payment_details = Payment()
        # return dao.add_payment_record(self, payment_details)