from fastapi import APIRouter
from controllers.modulo_controller import ModuloController
from models.modulo_model import Modulo

router = APIRouter()
nuevo_modulo = ModuloController()

@router.post("/create_modulo")
async def create_modulo(modulo: Modulo):
    return nuevo_modulo.create_modulo(modulo)

@router.get("/get_modulo/{modulo_id}", response_model=Modulo)
async def get_modulo(modulo_id: int):
    return nuevo_modulo.get_modulo(modulo_id)

@router.get("/get_modulos/", response_model=list[Modulo])
async def get_modulos():
    return nuevo_modulo.get_modulos()

@router.put("/update_modulo/{modulo_id}")
async def update_modulo(modulo_id: int, modulo: Modulo):
    return nuevo_modulo.update_modulo(modulo_id, modulo)

@router.delete("/delete_modulo/{modulo_id}")
async def delete_modulo(modulo_id: int):
    return nuevo_modulo.delete_modulo(modulo_id)
