

from interfaces import PaymentInterface
from services import CreditCardPayment, DebitCardPayment, UPIPayment
# from Entities import Payment, Wallet
from DAO import PaymentsDAO, WalletDAO
import datetime

from flask import Flask, request, json


### Crux of the payment microservice
### This will receive instruction to store all the payment related things only
### Only one controller will be needed 
### have separate routes for different payment strategies


### One route fors each payment strategy
### input taken by controller -> ride_id , amount , user_id , payment method and any other attribute if needed

class PaymentController : 

    def __init__(self) :
        self.__app = Flask(__name__)

        self.__app.add_url_rule('/creditcard', view_func=self.pay_with_creditcard, methods=['POST'])
        self.__app.add_url_rule('/debitcard', view_func=self.pay_with_debitcard, methods=['POST'])
        self.__app.add_url_rule('/upi', view_func=self.pay_with_upi, methods=['POST'])
    
    # for payment to be made:
    # different services
    # accessing and modifying database objects

    def pay_with_creditcard(self):
        amount = request.json['amount']
        card_number = request.json['card_number']
        expiration_date = request.json['expiration_date']
        cvv = request.json['cvv']
        credit_card_payment = CreditCardPayment(card_number, expiration_date, cvv)
        payment_details = {
            "user_id": request.json['user_id'],
            "ride_id": request.json['ride_id'],
            "driver_id": request.json['driver_id'],
            "amount": amount,
            "payment_method": "credit_card",
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "successful"
        }
        success = credit_card_payment.pay(amount)
        if success :
            self.save_payment_to_database(payment_details)
            return True
        return False

    def pay_with_debitcard(self):
        card_number = request.json['card_number']
        expiration_date = request.json['expiration_date']
        cvv = request.json['cvv']
        amount = request.json['amount']
        # Initialize DebitCardPayment and call pay method
        debit_card_payment = DebitCardPayment(card_number, expiration_date, cvv)
        payment_details = {
            "user_id": request.json['user_id'],
            "ride_id": request.json['ride_id'],
            "driver_id": request.json['driver_id'],
            "amount": amount,
            "payment_method": "credit_card",
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "successful"
        }
        success = debit_card_payment.pay(amount)
        if success :
            self.save_payment_to_database(payment_details)
            return True
        return False


    def pay_with_upi(self):
        upi_id = request.json['upi_id']
        pin = request.json['pin']
        amount = request.json['amount']
        # Initialize UPIPayment and call pay method
        upi_payment = UPIPayment(upi_id, pin)
        payment_details = {
            "user_id": request.json['user_id'],
            "ride_id": request.json['ride_id'],
            "driver_id": request.json['driver_id'],
            "amount": request.json['amount'],
            "payment_method": "credit_card",
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "successful"
        }
        success = upi_payment.pay(amount)
        if success :
            self.save_payment_to_database(payment_details)
            return True
        return False

    
    def save_payment_to_database(self, payment_details):
        # Save payment details to database
        driver_wallet_dao = WalletDAO()
        driver_wallet_dao.add_amount(payment_details)
        payments_dao = PaymentsDAO()
        payments_dao.add_payment_record(payment_details)
        
    # def set_payment_method(self, payment_method, details_in_tuple) :
        
    #     if payment_method == 'CreditCard':
    #         return CreditCardPayment(*details_in_tuple)
        
    #     elif payment_method == 'DebitCard':
    #         return DebitCardPayment(*details_in_tuple)
        
    #     elif payment_method == 'UPI':
    #         return UPIPayment(*details_in_tuple)
    

    # def execute(self, ride_id, amount, user_id, payment_method, date, driver_id, details) :

    #     payment_details = Payment(amount, payment_method, date, ride_id, user_id, driver_id)
        
    #     self.set_payment_method(payment_method, details).pay(self.amount)

    #     success = PaymentsDAO.add_payment_record(self.payment_details)

    #     if(success):
    #         self.payment_details.set_status("completed")

    # def creditcard(self, ) :

    #     CreditCardPayment(details)