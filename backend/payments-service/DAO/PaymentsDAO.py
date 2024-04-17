'''Accessing the Payment Object in the Database'''

import sqlite3
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
        pass

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
        cursor.execute("INSERT INTO payment (id, user_id, ride_id, driver_id, amount, payment_method, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       tuple(vars(payment_details).values()))
        mydb.commit()

        # Number of inserted records should be one
        if cursor.rowcount == 1:
            return True
        
        return False

    def update_payment_record(self, payment_details):
        pass
