

from interfaces import PaymentInterface


### Crux of the payment microservice
### This will receive instruction to store all the payment related things only
### Only one controller will be needed 
### have separate routes for different payment strategies


### One route fors each payment strategy
### input taken by controller -> ride_id , amount , user_id , payment method and any other attribute if needed
class PaymentController : 
    pass 