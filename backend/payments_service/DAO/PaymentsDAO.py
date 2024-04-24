'''Accessing the Payment Object in the Database'''

import sqlite3
import datetime
mydb = sqlite3.connect("payment_management.db")
 
cursor = mydb.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS payment (
    user_id varchar(255),
    ride_id varchar(255),
    driver_id varchar(255),
    amount double,
    payment_method varchar(255),
    date varchar(255),
    status varchar(255)
)''')

mydb.commit()


class PaymentsDAO:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def get_payments_of_user(self, user_id):
        self.cursor.execute("SELECT ride_id, driver_id, amount, payment_method, date, status FROM payment WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    # def get_payment_by_id(self, id):
    #     self.cursor.execute("SELECT * FROM payment WHERE id = ?", (id,))
    #     return self.cursor.fetchone()
    
    def get_payment_of_wallet(self, driver_id):
        self.cursor.execute("SELECT user_id, ride_id, amount, payment_method, date, status FROM payment WHERE driver_id = ?", (driver_id,))
        return self.cursor.fetchall()

    def add_payment_record(self, payment_details):
        values = tuple(payment_details.values())
        self.cursor.execute("INSERT INTO payment (user_id, ride_id, driver_id, amount, payment_method, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
        # self.id += 1
        self.connection.commit()

        # Number of inserted records should be one
        if self.cursor.rowcount == 1:
            return True
        
        return False

    def update_payment_record(self, payment_details):
        pass


# payment.add_payment_record({
#     "user_id": 1,
#     "ride_id": 1,
#     "driver_id": 1,
#     "amount": 100,
#     "payment_method": "credit_card",
#     "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     "status": "successful"
# })
# mydb = sqlite3.connect("payment_management.db")
# cursor = mydb.cursor()
# payment = PaymentsDAO(mydb, cursor)
# print(payment.get_payments_of_user("1"))
# print(payment.get_payment_by_id("1"))
