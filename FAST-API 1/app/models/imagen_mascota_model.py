from pydantic import BaseModel
from typing import Optional

class ImagenMascota(BaseModel):
    id: Optional[int] = None
    mascota_id: int
    url_imagen: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    status: bool = True
