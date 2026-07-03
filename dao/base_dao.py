from abc import ABC, abstractmethod

from Database.Connexion import DatabaseConnection


class BaseDAO(ABC):
    def __init__(self):
        self.bd=DatabaseConnection()
    @abstractmethod
    def get_all(self):
        pass
    @abstractmethod
    def get_by_id(self,id):
        pass
    @abstractmethod
    def get_delete_by(self):
        pass
    