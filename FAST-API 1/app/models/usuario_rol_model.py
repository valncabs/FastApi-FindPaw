from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuarioRol(BaseModel):
    usuario_id: int
    rol_id: int


class UsuarioRolResponse(BaseModel):
    id: int
    usuario_id: int
    rol_id: int
    created_at: datetime
    updated_at: datetime
    status: bool
