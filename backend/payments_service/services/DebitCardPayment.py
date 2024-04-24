from interfaces.PaymentInterface import PaymentInterface

class DebitCardPayment(PaymentInterface):
    def __init__(self, card_number, expiration_date, cvv):
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.balance = 100000  # Assuming a default balance for demonstration

    def check_valid(self):
        # Implement logic to check if debit card is valid
        return True

    def pay(self, amount):
        if not self.check_valid():
            return False
        
        # Implement logic to deduct amount from debit card balance
        if self.balance < amount:
            return False
        
        self.balance -= amount
        return True
