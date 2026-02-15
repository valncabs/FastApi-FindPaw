from fastapi import APIRouter
from controllers.imagen_controller import ImagenController
from models.imagen_mascota_model import ImagenMascota

router = APIRouter()
imagen_ctrl = ImagenController()

@router.post("/create_imagen")
async def create_imagen(imagen: ImagenMascota):
    return imagen_ctrl.create_imagen(imagen)

@router.get("/get_imagen/{imagen_id}")
async def get_imagen(imagen_id: int):
    return imagen_ctrl.get_imagen(imagen_id)

@router.get("/get_imagenes/")
async def get_imagenes():
    return imagen_ctrl.get_imagenes()

@router.put("/update_imagen/{imagen_id}")
async def update_imagen(imagen_id: int, imagen: ImagenMascota):
    return imagen_ctrl.update_imagen(imagen_id, imagen)

@router.delete("/delete_imagen/{imagen_id}")
async def delete_imagen(imagen_id: int):
    return imagen_ctrl.delete_imagen(imagen_id)
