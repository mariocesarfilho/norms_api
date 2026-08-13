from pydantic import BaseModel

class UserBase(BaseModel):
    emal: str
    password_hash: str

class UserCreate(UserBase):
    pass

class UserData(BaseModel):
    id: int
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    success: bool
    message: str
    data: UserData