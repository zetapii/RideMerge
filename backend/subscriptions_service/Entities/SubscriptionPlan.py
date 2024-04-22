from datetime import date, timedelta

class SubscriptionPlan(object):
    """
    DTO Object for Subscription Plan of the User
    
    Parameters
    -------
    userid : ID of the User who has purchased subscription
    price  : Price of the Subscription for the user 
    duration : Duration of the Subscription for the user (in days)
    
    Other Parameters 
    --------
    id : Mongo ID of the Subscription Plan 
    benefit_id : Mongo ID of the benefit object corresponding to
    the Subscription Plan
    """
    def __init__(self, 
                 userid : str, 
                 duration : int,
                 benefit_id : str,
                 start_date = None,
                 id = None):
        self.__id = id
        self.__name = userid
        self.__duration = duration
        self.__benefit = benefit_id
        
        self.__start_date = start_date 
        if self.__start_date == None:
            self.__start_date = date.today()

    def getId(self):
        return self.__id
    
    def setId(self, id):
        self.__id = id

    def getUserID(self):
        return self.__name
    
    def setUserID(self, name):
        self.__name = name
    
    def getDuration(self):
        return self.__duration
    
    def setDuration(self, duration):
        self.__duration = duration

    def getBenefit(self):
        return self.__benefit
    
    def setBenefit(self, benefit):
        self.__benefit = benefit
    
    def getStartDate(self):
        return self.__start_date
    
    def getExpireDate(self):
        return self.__start_date + timedelta(days = self.__duration)
    
    def setStartDate(self, new_start_date : date):
        self.__start_date = new_start_date 
    
    def checkExpired(self):
        current_date = date.today()
        
        expiry_date = self.__start_date + timedelta(days = self.__duration)

        
        return current_date > expiry_date

    def __str__(self):
        return f'SubscriptionPlan [id={self.__id}, name={self.__name}, price={self.__price}, duration={self.__duration}, benefit={self.__benefit}, date={self.__start_date}]'