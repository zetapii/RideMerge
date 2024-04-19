# '''This will store the payment object that will be saved in the Database.'''

# class Payment:

#     def __init__(self, amount, payment_method, date, ride_id, user_id, driver_id):
        
#         self.id = self.generate_id()
#         self.ride_id = ride_id
#         self.user_id = user_id
#         self.driver_id = driver_id
#         self.amount = amount
#         self.payment_method = payment_method
#         self.date = date
#         self.__status = "pending"

#     def set_status(self, status):
#         self.__status = status

#     def generate_id(self):
#         self.id = self.user_id + self.ride_id