from abc import ABC, abstractmethod
from DAO import PaymentsDAO

class PaymentInterface(ABC) :  

    @abstractmethod
    def pay(self, amount):
        # PaymentsDAO.add_payment_record(payment_details)
        pass
