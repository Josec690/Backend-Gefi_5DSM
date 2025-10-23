from . import BaseModel, EmailStr
from pydantic import constr, Field
from typing import Annotated


class UserCreate(BaseModel):
    cpf_user: Annotated[str, constr(regex=r'^\d{11}$')]
    full_name: Annotated[str, constr(min_length=3, max_length=100)]
    email: EmailStr
    password: Annotated[str, constr(min_length=6, max_length=100)]

class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=6, max_length=100)]

class PasswordReset(BaseModel):
    email: EmailStr
class PasswordChange(BaseModel):
    old_password: Annotated[str, constr(min_length=6, max_length=100)]
    new_password: Annotated[str, constr(min_length=6, max_length=100)]