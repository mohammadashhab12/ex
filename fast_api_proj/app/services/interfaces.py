from abc import ABC, abstractmethod
from app.models.user import User

class IUserCreation(ABC):
    @abstractmethod
    def create_user(self, user: User):
        pass

class IUserProfileUpdate(ABC):
    @abstractmethod
    def update_user(self, username: str, updates: dict):
        pass

class IUserRetrieval(ABC):
    @abstractmethod
    def get_user(self, username: str):
        pass
