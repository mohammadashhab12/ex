from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class AdminUser(User):
    # different admin levels ?
    # admin_level: int = Field(..., ge=1, le=5)
    pass

class RegularUser(User):
    # different subscription levels ?
    # subscription_level: int = Field(..., ge=1, le=3)
    pass
