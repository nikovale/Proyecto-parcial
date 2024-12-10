from pydantic import BaseModel # type: ignore
from typing import Optional

class UsersSchema(BaseModel):
    full_name: str
    password: str
    correo: str


# Modelo para la solicitud de inicio de sesión
class LoginRequest(BaseModel):
    correo: str  
    password: str