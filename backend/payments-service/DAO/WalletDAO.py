'''Accessing the Wallet Object in the Database'''

import sqlite3
mydb = sqlite3.connect("payment_management.db")
 
cursor = mydb.cursor()

# Create wallet table
cursor.execute('''CREATE TABLE IF NOT EXISTS driver_wallet (
    driver_id varchar(255),
    balance int,
    date_created varchar(255),
)''')

# Commit changes
mydb.commit()


class WalletDAO:
    def __init__(self):
        pass

    def add_amount(self, payment_details):
        cursor.execute("UPDATE driver_wallet SET balance = balance + ? WHERE driver_id = ?", (payment_details.amount, payment_details.driver_id) )
        mydb.commit()

        # Number of inserted records should be one
        if cursor.rowcount == 1:
            return True
        
        return False

