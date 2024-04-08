from abc import ABC, abstractmethod

class PaymentInterface(ABC) :  

    @abstractmethod
    def pay(amount):
        pass