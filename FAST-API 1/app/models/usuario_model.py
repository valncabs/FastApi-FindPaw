from pydantic import BaseModel, Field

class Usuario(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    edad: int
    usuario: str
    correo: str
    contrasena: str = Field(..., min_length=6, max_length=60)


