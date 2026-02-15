from pydantic import BaseModel


class LoginSchema(BaseModel):
    usuario: str
    contrasena: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
