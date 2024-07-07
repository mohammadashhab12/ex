from fastapi import FastAPI, HTTPException, Depends
from app.models.user import User, AdminUser, RegularUser
from app.services.user_service import UserService, AdminUserService, RegularUserService
from app.services.interfaces import IUserCreation, IUserRetrieval, IUserProfileUpdate
import redis

app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

user_service = UserService(redis_client)
admin_user_service = AdminUserService(redis_client)
regular_user_service = RegularUserService(redis_client)


def get_user_service() -> IUserCreation:
    return user_service


def get_admin_user_service() -> IUserCreation:
    return admin_user_service


def get_regular_user_service() -> IUserCreation:
    return regular_user_service


def get_user_retrieval_service() -> IUserRetrieval:
    return user_service


def get_user_profile_update_service() -> IUserProfileUpdate:
    return user_service


@app.post("/user/")
def create_user(user: User, service: IUserCreation = Depends(get_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/admin_user/")
def create_admin_user(user: AdminUser, service: IUserCreation = Depends(get_admin_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/regular_user/")
def create_regular_user(user: RegularUser, service: IUserCreation = Depends(get_regular_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/user/{username}")
def get_user(username: str, service: IUserRetrieval = Depends(get_user_retrieval_service)):
    try:
        return service.get_user(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/user/{username}")
def update_user(username: str, updates: dict, service: IUserProfileUpdate = Depends(get_user_profile_update_service)):
    try:
        return service.update_user(username, updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/user/{username}")
def delete_user(username: str):
    if not redis_client.exists(username):
        raise HTTPException(status_code=404, detail="User not found")

    redis_client.delete(username)
    return {"message": "User deleted successfully"}



@app.get("/")
def read_root():
    return {"Hello": "World"}
