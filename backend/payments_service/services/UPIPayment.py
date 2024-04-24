from interfaces.PaymentInterface import PaymentInterface

class UPIPayment(PaymentInterface):
    def __init__(self, upi_id, pin):
        self.upi_id = upi_id
        self.pin = pin
        self.balance = 100000  # Assuming a default balance for demonstration

    def check_valid(self):
        # Implement logic to check if UPI credentials are valid
        return True

    def pay(self, amount):
        if not self.check_valid():
            return False
        
        # Implement lgic to deduct amount from UPI balance
        if self.balance < amount:
            return False
        
        self.balance -= amount
        return True
