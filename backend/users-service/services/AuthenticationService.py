
import DAO.UserDAO as UserDAO

class AuthenticationService : 

    def __init__(self):
        self.dao = UserDAO() 

    def authenticate(self, username, password):
        user = UserDAO.get_user_by_username(username)
        if user is None:
            return False
        return user.password == password
    
