from fastapi import APIRouter, HTTPException
from typing import List
from controllers.mascota_controller import MascotaController
from models.mascota_perdida_model import MascotaCreate, MascotaUpdate

router = APIRouter()
mascota_ctrl = MascotaController()

# Crear mascota
@router.post("/create_mascota")
def create_mascota(mascota: MascotaCreate):
    return mascota_ctrl.create(mascota)

# Obtener mascota por id
@router.get("/get_mascota/{mascota_id}")
def get_mascota(mascota_id: int):
    return mascota_ctrl.get_by_id(mascota_id)

# Obtener todas las mascotas
@router.get("/get_mascotas/", response_model=List[dict])
def get_mascotas():
    return mascota_ctrl.get_all()

# Actualizar mascota
@router.put("/update_mascota/{mascota_id}")
def update_mascota(mascota_id: int, mascota: MascotaUpdate):
    return mascota_ctrl.update(mascota_id, mascota)

# Eliminar mascota (soft delete)
@router.delete("/delete_mascota/{mascota_id}")
def delete_mascota(mascota_id: int):
    return mascota_ctrl.delete(mascota_id)
