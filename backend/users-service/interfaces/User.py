from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, id, passsword, name, dob , mobile, email):
        self.id = id
        self.password = passsword
        self.name = name
        self.dob = dob 
        self.mobile = mobile
        self.email = email

    def getId(self):
        return self.id
    
    def setId(self, id):
        self.id = id
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name

    def getDob(self):
        return self.dob
    
    def setDob(self, dob):
        self.dob = dob
    
    def getMobile(self):
        return self.mobile
    
    def setMobile(self, mobile):
        self.mobile = mobile
    
    def getEmail(self):
        return self.email
    
    def setEmail(self, email):
        self.email = email 

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password    

    def __str__(self):
        return f'User [id={self.id}, name={self.name}, dob={self.dob}, mobile={self.mobile}, email={self.email}]'