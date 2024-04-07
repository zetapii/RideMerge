
class SubscriptionPlan:
    def __init__(self, id, name, price, duration,benefit):
        self.id = id
        self.name = name
        self.price = price
        self.duration = duration
        self.benefit = benefit

    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id

    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name

    def getPrice(self):
        return self.price
    
    def setPrice(self, price):
        self.price = price
    
    def getDuration(self):
        return self.duration
    
    def setDuration(self, duration):
        self.duration = duration

    def getBenefit(self):
        return self.benefit
    
    def setBenefit(self, benefit):
        self.benefit = benefit

    def __str__(self):
        return f'SubscriptionPlan [id={self.id}, name={self.name}, price={self.price}, duration={self.duration}, benefit={self.benefit}]'