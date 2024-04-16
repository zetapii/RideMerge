from abc import ABC, abstractmethod


class JSONFactoryInterface(ABC):

    @abstractmethod
    def convertToJSON(self, object):
        pass

    @abstractmethod
    def convertToObject(self, json):
        pass 