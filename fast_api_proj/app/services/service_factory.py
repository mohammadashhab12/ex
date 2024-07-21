from typing import Union
import redis
from app.pycommon.app_config.config import ConfigSingleton
from app.services.redis_services import UserService, AdminUserService, RegularUserService
from app.services.in_memory_user_service import InMemoryUserService


class ServiceFactory:
    config: ConfigSingleton
    user_service: Union[UserService, InMemoryUserService]
    admin_user_service: Union[AdminUserService, InMemoryUserService]
    regular_user_service: Union[RegularUserService, InMemoryUserService]

    def __init__(self):
        self.config = ConfigSingleton.get_instance()

        if self.config.DB_TYPE == 'redis':
            redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
            self.user_service = UserService(redis_client)
            self.admin_user_service = AdminUserService(redis_client)
            self.regular_user_service = RegularUserService(redis_client)
        else:
            self.user_service = InMemoryUserService()
            self.admin_user_service = InMemoryUserService()
            self.regular_user_service = InMemoryUserService()

    def get_user_service(self) -> Union[UserService, InMemoryUserService]:
        return self.user_service

    def get_admin_user_service(self) -> Union[AdminUserService, InMemoryUserService]:
        return self.admin_user_service

    def get_regular_user_service(self) -> Union[RegularUserService, InMemoryUserService]:
        return self.regular_user_service

    def get_user_retrieval_service(self) -> Union[UserService, InMemoryUserService]:
        return self.user_service

    def get_user_profile_update_service(self) -> Union[UserService, InMemoryUserService]:
        return self.user_service

