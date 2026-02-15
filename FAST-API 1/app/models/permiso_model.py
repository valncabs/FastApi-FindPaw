from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PermisoCreate(BaseModel):
    rol_id: int
    modulo_id: int
    puede_ver: bool = True
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False

class Permiso(PermisoCreate):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: Optional[bool] = True
