from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReporteInformacion(BaseModel):
    id: Optional[int] = None
    mascota_id: int
    usuario_id: int
    mensaje: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: Optional[bool] = None
