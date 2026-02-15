from fastapi import APIRouter
from controllers.usuario_controller import UsuarioController
from models.usuario_model import Usuario
from pydantic import BaseModel

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

controller = UsuarioController()



class LoginRequest(BaseModel):
    usuario: str
    contrasena: str


@router.post("/login")
async def login(data: LoginRequest):
    return controller.login(data.usuario, data.contrasena)


# =========================
# CREATE
# =========================
@router.post("/")
async def create_usuario(user: Usuario):
    return controller.create(
        user.nombre,
        user.apellido,
        user.cedula,
        user.edad,
        user.usuario,
        user.correo,
        user.contrasena
    )


# =========================
# GET ALL
# =========================
@router.get("/")
async def get_usuarios():
    return controller.get_all()


# =========================
# GET BY ID
# =========================
@router.get("/{user_id}")
async def get_usuario(user_id: int):
    return controller.get_by_id(user_id)


# =========================
# UPDATE
# =========================
@router.put("/{user_id}")
async def update_usuario(user_id: int, user: Usuario):
    return controller.update(
        user_id,
        user.nombre,
        user.apellido,
        user.cedula,
        user.edad,
        user.usuario,
        user.correo,
        user.contrasena
    )


# =========================
# DELETE (SOFT DELETE)
# =========================
@router.delete("/{user_id}")
async def delete_usuario(user_id: int):
    return controller.delete(user_id)
