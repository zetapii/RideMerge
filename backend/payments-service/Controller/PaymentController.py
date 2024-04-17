

from interfaces import PaymentInterface
from services import CreditCardPayment, DebitCardPayment, UPIPayment
from Entities import Payment, Wallet
from DAO import PaymentsDAO


### Crux of the payment microservice
### This will receive instruction to store all the payment related things only
### Only one controller will be needed 
### have separate routes for different payment strategies


### One route fors each payment strategy
### input taken by controller -> ride_id , amount , user_id , payment method and any other attribute if needed
class PaymentController : 

    def __init__(self, ride_id, amount, user_id, payment_method, date, driver_id) :
        self.payment_details = Payment(amount, payment_method, date, ride_id, user_id, driver_id)
        # payment_method_instance should have CreditCardPayment() etc
        # self.payment_method = self.set_payment_method(payment_method)

    # for payment to be made:
    # different services
    # accessing and modifying database objects

    def set_payment_method(self, payment_method, details_in_tuple) :
        
        if payment_method == 'CreditCard':
            return CreditCardPayment(*details_in_tuple)
        
        elif payment_method == 'DebitCard':
            return DebitCardPayment(*details_in_tuple)
        
        elif payment_method == 'UPI':
            return UPIPayment(*details_in_tuple)
    

    def execute(self) :
        self.payment_method.pay(self.amount)
        success = PaymentsDAO.add_payment_record(self.payment_details)
        if(success):
            self.payment_details.set_status("completed")