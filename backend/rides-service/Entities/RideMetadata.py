'''This will also store the speed of the vehicle maybe in ridemetadata'''


class RideMetadata :

    ##Ride Metadata is created once the ride is accepted by the driver and otp is sent
    def __init__(self, id , ride_id , src_loc , ride_otp , status, vehicle_id):
        self.id = id
        self.ride_id = ride_id
        self.ride_otp = ride_otp
        self.status = status 
        self.ride_rating = None
        self.vehicle_id = vehicle_id
