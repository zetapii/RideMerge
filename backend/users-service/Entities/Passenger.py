from interfaces import User

class Passenger(User):
    def __init__(self, id, passsword, name, dob , mobile, email, subcription_status, subscription_plan):
        super().__init__(id, passsword, name, dob , mobile, email)
        self.subscription_status =  subcription_status
        self.subscription_plan = subscription_plan

    def getSubscriptionStatus(self):
        return self.subscription_status
    
    def setSubscriptionStatus(self, status):
        self.subscription_status = status

    def getSubscriptionPlan(self):
        return self.subscription_plan
    
    def setSubscriptionPlan(self, plan):
        self.subscription_plan = plan
    
    def __str__(self):
        return f'Passenger [id={self.id}, name={self.name}, dob={self.dob}, mobile={self.mobile}, email={self.email}, subscription_status={self.subscription_status}, subscription_plan={self.subscription_plan}]'