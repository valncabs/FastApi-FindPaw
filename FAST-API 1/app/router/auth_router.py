from fastapi import APIRouter, HTTPException
from config.db_config import get_db_connection
from utils.password_handler import verify_password
from utils.jwt_handler import create_access_token
from schemas.auth_schema import LoginSchema, TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, usuario, contrasena
        FROM usuarios
        WHERE usuario = %s AND status = TRUE
    """, (data.usuario,))

    user = cur.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    user_id = user[0]
    username = user[1]
    hashed_password = user[2]

    if not verify_password(data.contrasena, hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token({
        "sub": username,
        "user_id": user_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
