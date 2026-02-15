from pydantic import BaseModel
from datetime import datetime

class Rol(BaseModel):
    nombre: str


class RolResponse(BaseModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime
    status: bool
