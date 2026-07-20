from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: int
    email: EmailStr

    class Config:
        from_attributes = True
