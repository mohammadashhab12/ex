from fastapi import FastAPI, HTTPException, Depends
from app.models.user import User, AdminUser, RegularUser
from app.dependecies import (
    get_user_service,
    get_admin_user_service,
    get_regular_user_service,
    get_user_retrieval_service,
    get_user_profile_update_service,
    delete_user_service
)
from app.config import config
from app.services.in_memory_user_service import InMemoryUserService

app = FastAPI()


@app.post("/user/")
def create_user(user: User, service=Depends(get_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/admin_user/")
def create_admin_user(user: AdminUser, service=Depends(get_admin_user_service)):
    # Check max admin users limit
    if isinstance(service, InMemoryUserService):
        current_admins = [key for key in service.users if isinstance(service.users[key], AdminUser)]
    else:
        current_admins = [key for key in service.redis_client.keys() if key.startswith('admin')]

    if len(current_admins) >= config.MAX_ADMIN_USERS:
        raise HTTPException(status_code=400, detail="Maximum number of admin users reached")

    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/regular_user/")
def create_regular_user(user: RegularUser, service=Depends(get_regular_user_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/user/{username}")
def get_user(username: str, service=Depends(get_user_retrieval_service)):
    try:
        return service.get_user(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/user/{username}")
def update_user(username: str, updates: dict, service=Depends(get_user_profile_update_service)):
    try:
        return service.update_user(username, updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/user/{username}")
def delete_user(username: str, delete_user_service=Depends(delete_user_service)):
    try:
        delete_user_service(username)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"message": "User deleted successfully"}


@app.get("/")
def read_root():
    return {"Hello": "World"}
