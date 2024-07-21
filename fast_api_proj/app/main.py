from fastapi import FastAPI, HTTPException, Depends
from app.models.user import User, AdminUser, RegularUser
from app.dependecies import (
    get_user_service,
    get_admin_user_service,
    get_regular_user_service,
    get_user_retrieval_service,
    get_user_profile_update_service
)
from app.pycommon.app_config.config import ConfigSingleton
from app.pycommon.api_exception.exceptions import UserAlreadyExistsException, UserNotFoundException, MaxAdminUsersReachedException

app = FastAPI()
config = ConfigSingleton.get_instance()


@app.post("/user/")
def create_user(user: User, service=Depends(get_user_service)):
    try:
        return service.create_user(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=f"User with username '{e.username}' already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/admin_user/")
def create_admin_user(user: AdminUser, service=Depends(get_admin_user_service)):
    # if service.get_admin_user_count() >= ConfigSingleton.get_instance().MAX_ADMIN_USERS:
    try:
        if service.get_admin_user_count() >= ConfigSingleton.get_instance().MAX_ADMIN_USERS:
            raise MaxAdminUsersReachedException()
        return service.create_user(user)
    except MaxAdminUsersReachedException:
        raise HTTPException(status_code=400, detail="Maximum number of admin users reached")
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=f"User with username '{e.username}' already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/regular_user/")
def create_regular_user(user: RegularUser, service=Depends(get_regular_user_service)):
    try:
        return service.create_user(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=f"User with username '{e.username}' already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user/{username}")
def get_user(username: str, service=Depends(get_user_retrieval_service)):
    try:
        return service.get_user(username)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"User with username '{e.username}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/user/{username}")
def update_user(username: str, updates: dict, service=Depends(get_user_profile_update_service)):
    try:
        return service.update_user(username, updates)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"User with username '{e.username}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/user/{username}")
def delete_user(username: str, service=Depends(get_user_service)):
    try:
        return service.delete_user(username)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=f"User with username '{e.username}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"Hello": "World"}
