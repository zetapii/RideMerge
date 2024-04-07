

class SubsBenefitDao : 
    def __init__(self, db) :
        self.benefit_list = []
        self.subscription_list = []

    def add_benefit(self, benefit):
        self.benefit_list.append(benefit)
    
    def add_subscription(self, subscription):
        self.subscription_list.append(subscription)

    def get_benefit_by_id(self, id):
        for benefit in self.benefit_list:
            if benefit.getId() == id:
                return benefit
        return None
    
    def get_subscription_by_id(self, id):
        for subscription in self.subscription_list:
            if subscription.getId() == id:
                return subscription
        return None
    
    def get_all_benefits(self):
        return self.benefit_list
    
    def get_all_subscriptions(self):
        return self.subscription_list
    
    def __str__(self):
        return f'SubsBenefitDao [benefit_list={self.benefit_list}, subscription_list={self.subscription_list}]'