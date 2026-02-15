from pydantic import BaseModel
from typing import Optional

class Modulo(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    status: bool = True
