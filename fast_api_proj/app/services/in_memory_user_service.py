
from app.models.user import User, AdminUser, RegularUser
from app.services.interfaces import IUserCreation, IUserProfileUpdate, IUserRetrieval

class InMemoryUserService(IUserCreation, IUserProfileUpdate, IUserRetrieval):
    def __init__(self):
        self.users = {}

    def create_user(self, user: User):
        if user.username in self.users:
            raise ValueError("Username already exists")
        self.users[user.username] = user.dict()
        return {"message": "User created successfully", "user": user}

    def update_user(self, username: str, updates: dict):
        if username not in self.users:
            raise ValueError("User not found")
        self.users[username].update(updates)
        return {"message": "User updated successfully", "user": self.users[username]}

    def get_user(self, username: str):
        if username in self.users:
            return self.users[username]
        else:
            raise ValueError("User not found")

    def delete_user(self, username: str):
        if username not in self.users:
            raise ValueError("User not found")
        del self.users[username]
        return {"message": "User deleted successfully"}
