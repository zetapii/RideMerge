from abc import ABC, abstractmethod


class SubsBenefitDAOInterface(ABC):
    @abstractmethod
    def add(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def find(self):
        pass 