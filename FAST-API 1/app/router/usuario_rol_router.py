from fastapi import APIRouter
from controllers.usuario_rol_controller import UsuarioRolController
from models.usuario_rol_model import UsuarioRol, UsuarioRolResponse

router = APIRouter(prefix="/usuario_rol", tags=["Usuario-Rol"])
controller = UsuarioRolController()

@router.post("/", response_model=UsuarioRolResponse)
async def create_usuario_rol(data: UsuarioRol):
    return controller.create(data.usuario_id, data.rol_id)

@router.get("/{ur_id}", response_model=UsuarioRolResponse)
async def get_usuario_rol(ur_id: int):
    return controller.get_by_id(ur_id)

@router.get("/", response_model=list[UsuarioRolResponse])
async def get_usuario_roles():
    return controller.get_all()

@router.delete("/{ur_id}")
async def delete_usuario_rol(ur_id: int):
    return controller.delete(ur_id)
