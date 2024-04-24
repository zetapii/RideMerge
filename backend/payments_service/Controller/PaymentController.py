import sys
import os
import sqlite3

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../payments_service"))
sys.path.append(parent_dir)

# from interfaces.PaymentInterface import PaymentInterface
# from services import CreditCardPayment
# from services import DebitCardPayment
# from services import UPIPayment
# # from Entities import Payment, Wallet
# from DAO import PaymentsDAO, WalletDAO
# import datetime

# from flask import Flask, request, json


# ### Crux of the payment microservice
# ### This will receive instruction to store all the payment related things only
# ### Only one controller will be needed 
# ### have separate routes for different payment strategies


# ### One route fors each payment strategy
# ### input taken by controller -> ride_id , amount , user_id , payment method and any other attribute if needed

# class PaymentController : 

#     def __init__(self) :
#         self.app = Flask(__name__)

#         self.app.add_url_rule('/creditcard', view_func=self.pay_with_creditcard, methods=['POST'])
#         self.app.add_url_rule('/debitcard', view_func=self.pay_with_debitcard, methods=['POST'])
#         self.app.add_url_rule('/upi', view_func=self.pay_with_upi, methods=['POST'])
#         self.payments_dao = PaymentsDAO()
#     # for payment to be made:
#     # different services
#     # accessing and modifying database objects

#     def run(self):
#         self.app.run()

#     def pay_with_creditcard(self):
#         amount = request.json['amount']
#         card_number = request.json['card_number']
#         expiration_date = request.json['expiration_date']
#         cvv = request.json['cvv']
#         credit_card_payment = CreditCardPayment(card_number, expiration_date, cvv)
#         payment_details = {
#             "user_id": request.json['user_id'],
#             "ride_id": request.json['ride_id'],
#             "driver_id": request.json['driver_id'],
#             "amount": amount,
#             "payment_method": "credit_card",
#             "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "status": "successful"
#         }
#         success = credit_card_payment.pay(amount)
#         if success :
#             self.save_payment_to_database(payment_details)
#             return True
        
#         return False

#     def pay_with_debitcard(self):
#         # Initialize DebitCardPayment and call pay method
#         card_number = request.json['card_number']
#         expiration_date = request.json['expiration_date']
#         cvv = request.json['cvv']
#         amount = request.json['amount']
#         debit_card_payment = DebitCardPayment(card_number, expiration_date, cvv)
#         payment_details = {
#             "user_id": request.json['user_id'],
#             "ride_id": request.json['ride_id'],
#             "driver_id": request.json['driver_id'],
#             "amount": amount,
#             "payment_method": "credit_card",
#             "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "status": "successful"
#         }
#         success = debit_card_payment.pay(amount)
#         if success :
#             self.save_payment_to_database(payment_details)
#             return True
#         return False


#     def pay_with_upi(self):
#         # Initialize UPIPayment and call pay method
#         upi_id = request.json['upi_id']
#         pin = request.json['pin']
#         amount = request.json['amount']
#         upi_payment = UPIPayment(upi_id, pin)
#         payment_details = {
#             "user_id": request.json['user_id'],
#             "ride_id": request.json['ride_id'],
#             "driver_id": request.json['driver_id'],
#             "amount": request.json['amount'],
#             "payment_method": "credit_card",
#             "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "status": "successful"
#         }
#         success = upi_payment.pay(amount)
#         if success :
#             self.save_payment_to_database(payment_details)
#             return True
#         return False
    
#     def save_payment_to_database(self, payment_details):
#         # Save payment details to database
#         driver_wallet_dao = WalletDAO()
#         driver_wallet_dao.add_amount(payment_details)
#         payments_dao = PaymentsDAO()
#         payments_dao.add_payment_record(payment_details)

#     def get_payment_history(self):
#         # Retrieve payment history from database
#         user_id = request.json['user_id']
#         return self.payments_dao.get_payments_of_user(user_id)

# if __name__ == "__main__":
#     controller = PaymentController()
#     controller.run()

# import sys
# sys.path.append('../../payments-service')

from flask import Flask, jsonify, request
import datetime
from DAO.PaymentsDAO import PaymentsDAO
from DAO.WalletDAO import WalletDAO
# from services import CreditCardPayment, DebitCardPayment, UPIPayment
from services.CreditCardPayment import CreditCardPayment
from services.DebitCardPayment import DebitCardPayment
from services.UPIPayment import UPIPayment

app = Flask(__name__)


@app.route('/creditcard', methods=['POST'])
def pay_with_creditcard():
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
    if success:
        save_payment_to_database(payment_details)
        return jsonify({"status": "success"})
    return jsonify({"error": "error"})

@app.route('/debitcard', methods=['POST'])
def pay_with_debitcard():
    card_number = request.json['card_number']
    expiration_date = request.json['expiration_date']
    cvv = request.json['cvv']
    amount = request.json['amount']
    debit_card_payment = DebitCardPayment(card_number, expiration_date, cvv)
    payment_details = {
        "user_id": request.json['user_id'],
        "ride_id": request.json['ride_id'],
        "driver_id": request.json['driver_id'],
        "amount": amount,
        "payment_method": "debit_card",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "successful"
    }
    success = debit_card_payment.pay(amount)
    if success:
        save_payment_to_database(payment_details)
        return jsonify({"status": "success"})
    return jsonify({"error": "error"})

@app.route('/upi', methods=['POST'])
def pay_with_upi():
    upi_id = request.json['upi_id']
    pin = request.json['pin']
    amount = request.json['amount']
    upi_payment = UPIPayment(upi_id, pin)
    payment_details = {
        "user_id": request.json['user_id'],
        "ride_id": request.json['ride_id'],
        "driver_id": request.json['driver_id'],
        "amount": request.json['amount'],
        "payment_method": "upi",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "successful"
    }
    success = upi_payment.pay(amount)
    if success:
        save_payment_to_database(payment_details)
        return jsonify({"status": "success"})
    return jsonify({"error": "error"})

def save_payment_to_database(payment_details):
    mydb = sqlite3.connect("payment_management.db")
    cursor = mydb.cursor()
    driver_wallet_dao = WalletDAO(mydb, cursor)
    driver_wallet_dao.add_amount(payment_details)
    payment_dao = PaymentsDAO(mydb, cursor)
    payment_dao.add_payment_record(payment_details)

@app.route('/hello_world', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello World!"})

@app.route('/user_history/<user_id>', methods=['GET'])
def get_payment_history(user_id):
    try:        
        mydb = sqlite3.connect("payment_management.db")
        cursor = mydb.cursor()
        payment_dao = PaymentsDAO(mydb, cursor)
        data = payment_dao.get_payments_of_user(str(user_id))
        if data:
            print(data)
            return jsonify({
                "status": "success",
                "data": data
            })
        else:
            print(data)
            return jsonify({
                "status": "success",
                "message": "No payment history found for the user.",
                "data": []
            })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/wallet_history/<driver_id>', methods=['GET'])
def get_wallet_history(driver_id):
    try:
        mydb = sqlite3.connect("payment_management.db")
        cursor = mydb.cursor()
        payment_dao = PaymentsDAO(mydb, cursor)
        data = payment_dao.get_payment_of_wallet(str(driver_id))
        if data:
            return jsonify({
                "status": "success",
                "data": data
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No wallet history found for the driver.",
                "data": []
            })
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/wallet_amount/<driver_id>', methods=['GET'])
def get_wallet_amount(driver_id):
    try:
        history = get_wallet_history(driver_id)

        # for each history, get the amount and add it to the total
        total_amount = 0
        for entry in history.data:
            total_amount += entry

        return jsonify({
            "status": "success",
            "data": total_amount
        })
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
# def create_wallet():
#     mydb = sqlite3.connect("payment_management.db")
#     cursor = mydb.cursor()
#     wallet_dao = WalletDAO(mydb, cursor)
#     wallet_dao.create_wallet("1")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5014, debug=True)
