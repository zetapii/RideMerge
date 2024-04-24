'''Accessing the Wallet Object in the Database'''
import datetime
import sqlite3
mydb = sqlite3.connect("payment_management.db")
 
cursor = mydb.cursor()

# Create wallet table
cursor.execute('''CREATE TABLE IF NOT EXISTS driver_wallet (
    driver_id varchar(255),
    balance int,
    date_created varchar(255)
)''')

# Commit changes
mydb.commit()


class WalletDAO:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    def add_amount(self, payment_details):
        self.cursor.execute("UPDATE driver_wallet SET balance = balance + ? WHERE driver_id = ?", (payment_details['amount'], payment_details['driver_id']) )
        self.connection.commit()

        # Number of inserted records should be one
        if self.cursor.rowcount == 1:
            return True
        
        return False
    
    def get_amount(self, driver_id):
        self.cursor.execute("SELECT balance FROM driver_wallet WHERE driver_id = ?", (driver_id,))
        return self.cursor.fetchone()
    
    def create_wallet(self, driver_id):
        self.cursor.execute("INSERT INTO driver_wallet (driver_id, balance, date_created) VALUES (?, ?, ?)", (driver_id, 100, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.connection.commit()

# wallet = WalletDAO()
# wallet.create_wallet("1")
# wallet.add_amount({
#     "driver_id": "1",
#     "amount": 100
# })