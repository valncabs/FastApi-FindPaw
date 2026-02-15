from utils.password_handler import verify_password
from utils.jwt_handler import create_access_token
from config.db_config import get_db_connection
from fastapi import HTTPException

def login(self, usuario: str, contrasena: str):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, usuario, contrasena
        FROM usuarios
        WHERE usuario = %s AND status = true
    """, (usuario,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user_id, username, hashed_password = user

    if not verify_password(contrasena, hashed_password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token({
        "id": user_id,
        "usuario": username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
