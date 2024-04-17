'''Accessing the Payment Object in the Database'''

import sqlite3
mydb = sqlite3.connect("payment_management.db")
 
cursor = mydb.cursor()

# Create payments table
cursor.execute('''CREATE TABLE IF NOT EXISTS driver_wallet (
    driver_id varchar(255),
    balance int,
    date_created varchar(255),
)''')

# Insert data into the table
# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))

# Commit changes
mydb.commit()


class WalletDAO:
    def __init__(self):
        pass

    # def add_payment_record

    # def get_payments_of_user(self, user_id):
    #     cursor.execute("SELECT * FROM payment WHERE user_id = ?", 
    #                    (user_id))
        
    #     return cursor.fetchall()

    # def get_payment_by_id(self, id):
    #     cursor.execute("SELECT * FROM payment WHERE id = ?",
    #                    (id))

    #     return cursor.fetchone()
    #     pass

    def add_amount(self, payment_details):
        cursor.execute("UPDATE driver_wallet SET balance = balance + ? WHERE driver_id = ?", (payment_details.amount, payment_details.driver_id) )
        # cursor.execute("INSERT INTO driver_wallet (driver_id, amount, payment_method, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        #                tuple(vars(payment_details).values()))
        mydb.commit()

        # Number of inserted records should be one
        if cursor.rowcount == 1:
            return True
        
        return False

