from fastapi import APIRouter
from controllers.rol_controller import RolController
from models.rol_model import Rol, RolResponse

router = APIRouter(prefix="/roles", tags=["Roles"])
controller = RolController()

@router.post("/", response_model=RolResponse)
async def create_rol(data: Rol):
    return controller.create(data.nombre)

@router.get("/{rol_id}", response_model=RolResponse)
async def get_rol(rol_id: int):
    return controller.get_by_id(rol_id)

@router.get("/", response_model=list[RolResponse])
async def get_roles():
    return controller.get_all()

@router.put("/{rol_id}")
async def update_rol(rol_id: int, data: Rol):
    return controller.update(rol_id, data.nombre)

@router.delete("/{rol_id}")
async def delete_rol(rol_id: int):
    return controller.delete(rol_id)
