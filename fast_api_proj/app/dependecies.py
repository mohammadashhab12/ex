from app.services.service_factory import ServiceFactory

service_factory = ServiceFactory()

def get_user_service():
    return service_factory.get_user_service()

def get_admin_user_service():
    return service_factory.get_admin_user_service()

def get_regular_user_service():
    return service_factory.get_regular_user_service()

def get_user_retrieval_service():
    return service_factory.get_user_retrieval_service()

def get_user_profile_update_service():
    return service_factory.get_user_profile_update_service()

def delete_user_service():
    return service_factory.delete_user
