'''This is an interface'''



class ExternalRideAPI:


    def fetch_rides(self,source,destination):
        raise NotImplementedError
