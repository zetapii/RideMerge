
class SubscriptionPlan:
    def __init__(self, 
                 userid : str, 
                 price : float, 
                 duration : int,
                 benefit_id : str,
                 id = None):
        self.__id = id
        self.__name = userid
        self.__price = price
        self.__duration = duration
        self.__benefit = benefit_id

    def getId(self):
        return self.__id
    
    def setId(self, id):
        self.__id = id

    def getUserID(self):
        return self.__name
    
    def setUserID(self, name):
        self.__name = name

    def getPrice(self):
        return self.__price
    
    def setPrice(self, price):
        self.__price = price
    
    def getDuration(self):
        return self.__duration
    
    def setDuration(self, duration):
        self.__duration = duration

    def getBenefit(self):
        return self.__benefit
    
    def setBenefit(self, benefit):
        self.__benefit = benefit

    def __str__(self):
        return f'SubscriptionPlan [id={self.__id}, name={self.__name}, price={self.__price}, duration={self.__duration}, benefit={self.__benefit}]'