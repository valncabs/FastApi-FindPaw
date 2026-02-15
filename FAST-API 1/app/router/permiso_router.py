from fastapi import APIRouter
from controllers.permisos_controller import PermisoController
from models.permiso_model import Permiso

router = APIRouter()
nuevo_permiso = PermisoController()

# Crear permiso
@router.post("/create_permiso")
async def create_permiso(permiso: Permiso):
    return nuevo_permiso.create(
        permiso.rol_id,
        permiso.modulo_id,
        permiso.puede_ver,
        permiso.puede_crear,
        permiso.puede_editar,
        permiso.puede_eliminar
    )

# Obtener permiso por ID
@router.get("/get_permiso/{permiso_id}", response_model=Permiso)
async def get_permiso(permiso_id: int):
    return nuevo_permiso.get_by_id(permiso_id)

# Obtener todos los permisos
@router.get("/get_permisos/", response_model=list[Permiso])
async def get_permisos():
    return nuevo_permiso.get_all()

# Actualizar permiso
@router.put("/update_permiso/{permiso_id}")
async def update_permiso(permiso_id: int, permiso: Permiso):
    return nuevo_permiso.update(
        permiso_id,
        permiso.rol_id,
        permiso.modulo_id,
        permiso.puede_ver,
        permiso.puede_crear,
        permiso.puede_editar,
        permiso.puede_eliminar
    )

# Eliminar permiso (soft delete)
@router.delete("/delete_permiso/{permiso_id}")
async def delete_permiso(permiso_id: int):
    return nuevo_permiso.delete(permiso_id)
