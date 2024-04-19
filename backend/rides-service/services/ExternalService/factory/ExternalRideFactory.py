

import sys

sys.path.append('/Users/zaid/Downloads/Software Engineering/SE-Project/se-project-3--_19/backend/rides-service/services/ExternalService/')

from OLARideAPI import OLARideAPI
from UberRideAPI import UberRideAPI

class ExternalRideFactory : 
    
    def __init__(self, TOKEN):
        self.UBERTOKEN = TOKEN
        self.OLATOKEN = TOKEN

    def get_ride_service(self, service):
        if service == 'OLA':
            return OLARideAPI(self.OLATOKEN)
        elif service == 'UBER':
            return UberRideAPI(self.UBERTOKEN)
        else:
            return Exception("Service not found")
