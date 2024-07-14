
from app.config import config
from app.services.user_services import UserService, AdminUserService, RegularUserService
from app.services.in_memory_user_service import InMemoryUserService
import redis


class ServiceFactory:
    def __init__(self):
        if config.DB_TYPE == 'redis':

            self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
            self.user_service = UserService(self.redis_client)
            self.admin_user_service = AdminUserService(self.redis_client)
            self.regular_user_service = RegularUserService(self.redis_client)
        else:
            self.user_service = InMemoryUserService()
            self.admin_user_service = InMemoryUserService()
            self.regular_user_service = InMemoryUserService()

    def get_user_service(self):
        return self.user_service

    def get_admin_user_service(self):
        return self.admin_user_service

    def get_regular_user_service(self):
        return self.regular_user_service

    def get_user_retrieval_service(self):
        return self.user_service

    def get_user_profile_update_service(self):
        return self.user_service

    def delete_user(self, username: str):
        if config.DB_TYPE == 'redis':
            if not self.redis_client.exists(username):
                raise ValueError("User not found")
            self.redis_client.delete(username)
        else:
            self.user_service.delete_user(username)
