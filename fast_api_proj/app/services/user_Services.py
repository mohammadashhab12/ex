import redis
import json
from app.models.user import User, AdminUser, RegularUser
from app.services.interfaces import IUserCreation, IUserProfileUpdate, IUserRetrieval


class UserService(IUserCreation, IUserProfileUpdate, IUserRetrieval):
    def __init__(self, redis_client: redis.StrictRedis):
        self.redis_client = redis_client

    def create_user(self, user: User):
        if self.redis_client.exists(user.username):
            raise ValueError("Username already exists")
        self.redis_client.set(user.username, user.json())
        return {"message": "User created successfully", "user": user}

    def update_user(self, username: str, updates: dict):
        if not self.redis_client.exists(username):
            raise ValueError("User not found")
        user_data = self.redis_client.get(username)
        user_obj = json.loads(user_data)
        user_obj.update(updates)
        self.redis_client.set(username, json.dumps(user_obj))
        return {"message": "User updated successfully", "user": user_obj}

    def get_user(self, username: str):
        user_data = self.redis_client.get(username)
        if user_data:
            return json.loads(user_data)
        else:
            raise ValueError("User not found")


class AdminUserService(UserService):
    def create_user(self, user: AdminUser):
        return super().create_user(user)


class RegularUserService(UserService):
    def create_user(self, user: RegularUser):
        return super().create_user(user)
