from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id_user: Optional[str]
    user_names: str
    user_last_names: str
    email: str
    password: str
    

class AuthUser(BaseModel):
    email: str
    password: str