'''Accessing the Payment Object in the Database'''

import sqlite3
import datetime
mydb = sqlite3.connect("payment_management.db")
 
cursor = mydb.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS payment (
    id varchar(255),
    user_id varchar(255),
    ride_id varchar(255),
    driver_id varchar(255),
    amount int,
    payment_method varchar(255),
    date varchar(255),
    status varchar(255)
)''')

mydb.commit()


class PaymentsDAO:
    def __init__(self):
        self.id = 1

    def get_payments_of_user(self, user_id):
        cursor.execute("SELECT * FROM payment WHERE user_id = ?", 
                       (user_id))
        
        return cursor.fetchall()

    def get_payment_by_id(self, id):
        cursor.execute("SELECT * FROM payment WHERE id = ?",
                       (id))

        return cursor.fetchone()
        pass

    def add_payment_record(self, payment_details):
        print(type(payment_details))

        values = (self.id,) + tuple(payment_details.values())
        
        cursor.execute("INSERT INTO payment (id, user_id, ride_id, driver_id, amount, payment_method, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       values)
        
        self.id += 1
        mydb.commit()

        # Number of inserted records should be one
        if cursor.rowcount == 1:
            return True
        
        return False

    def update_payment_record(self, payment_details):
        pass

payment = PaymentsDAO()

# payment.add_payment_record({
#     "user_id": 1,
#     "ride_id": 1,
#     "driver_id": 1,
#     "amount": 100,
#     "payment_method": "credit_card",
#     "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     "status": "successful"
# })

print(payment.get_payment_by_id("1"))
