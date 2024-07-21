
from typing import Dict, Any
from app.models.user import User
from app.services.interfaces import IUserCreation, IUserProfileUpdate, IUserRetrieval
from app.pycommon.api_exception.exceptions import UserAlreadyExistsException, UserNotFoundException

class InMemoryUserService(IUserCreation, IUserProfileUpdate, IUserRetrieval):
    # should it only contain strings ?
    users: Dict[str, Dict[str, Any]]
    def __init__(self):
        self.users = {}

    def create_user(self, user: User):
        if user.username in self.users:
            raise UserAlreadyExistsException(user.username)
        self.users[user.username] = user.dict()
        return {"message": "User created successfully", "user": user}

    def update_user(self, username: str, updates: dict):
        if username not in self.users:
            raise UserNotFoundException(username)
        self.users[username].update(updates)
        return {"message": "User updated successfully", "user": self.users[username]}

    def get_user(self, username: str):
        if username in self.users:
            return self.users[username]
        else:
            raise UserNotFoundException(username)

    def delete_user(self, username: str):
        if username not in self.users:
            raise UserNotFoundException(username)
        del self.users[username]
        return {"message": "User deleted successfully"}

    def get_admin_user_count(self) -> int:
        admin_users = [user for user in self.users.values() if user['username'].startswith('admin')]
        return len(admin_users)