from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MascotaCreate(BaseModel):
    usuario_id: int
    nombre: str
    raza: str
    color: str
    tamano: str
    edad_aprox: str
    descripcion: Optional[str] = None
    ubicacion: str
    recompensa: Optional[float] = 0.0

class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    raza: Optional[str] = None
    color: Optional[str] = None
    tamano: Optional[str] = None
    edad_aprox: Optional[str] = None
    descripcion: Optional[str] = None
    ubicacion: Optional[str] = None
    recompensa: Optional[float] = None
