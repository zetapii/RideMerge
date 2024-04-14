'''Access and manipulate data in the database'''

class RideDAO : 

    @staticmethod
    def fetch_rides_user(source, destination, is_safe) : 
        '''Fetch rides from the database'''
        pass 

    @staticmethod
    def match_ride(source , destination , is_safe , car_model) : 
        '''Match a ride with the given parameters'''
        '''Just Set some attribute of the ride metadata to 1 , showing the interest of the user in the ride , and the frontend should show its matching until driver accepts'''
        pass 

    @staticmethod
    def fetch_rides_driver(source , destination ) : 
        '''Fetch rides for a driver'''
        '''This will just fetch all the rides without any filtering'''
        pass 

    @staticmethod
    def accept_ride_driver(ride_id) :
        '''Accept a ride for a driver'''
        '''Just set the status of the ride to accepted'''

        '''When a driver accepts the ride'''
        '''Just notify the passenger that the ride has been accepted'''
        pass 

    '''Write methods for car pooling'''