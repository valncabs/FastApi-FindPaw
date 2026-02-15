import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from config.db_config import get_db_connection
from utils.password_handler import hash_password, verify_password


class UsuarioController:

    # =========================
    # CREATE
    # =========================
    def create(
        self,
        nombre: str,
        apellido: str,
        cedula: str,
        edad: int,
        usuario: str,
        correo: str,
        contrasena: str
    ):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            hashed_password = hash_password(contrasena)

            cur.execute("""
                INSERT INTO usuarios (
                    nombre,
                    apellido,
                    cedula,
                    edad,
                    usuario,
                    correo,
                    contrasena
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                nombre,
                apellido,
                cedula,
                edad,
                usuario,
                correo,
                hashed_password
            ))

            result = cur.fetchone()
            conn.commit()

            return {
                "id": result["id"],
                "mensaje": "Usuario creado correctamente"
            }

        except psycopg2.errors.UniqueViolation:
            if conn:
                conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="El usuario, correo o cédula ya existe"
            )

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear usuario: {str(e)}"
            )

        finally:
            if conn:
                conn.close()


    # =========================
    # GET BY ID
    # =========================
    def get_by_id(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute("""
                SELECT
                    id,
                    nombre,
                    apellido,
                    cedula,
                    edad,
                    usuario,
                    correo,
                    created_at,
                    updated_at,
                    status
                FROM usuarios
                WHERE id = %s AND status = TRUE
            """, (user_id,))

            usuario = cur.fetchone()

            if not usuario:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )

            return jsonable_encoder(usuario)

        finally:
            if conn:
                conn.close()


    # =========================
    # GET ALL
    # =========================
    def get_all(self):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute("""
                SELECT
                    id,
                    nombre,
                    apellido,
                    cedula,
                    edad,
                    usuario,
                    correo,
                    created_at,
                    updated_at,
                    status
                FROM usuarios
                WHERE status = TRUE
            """)

            usuarios = cur.fetchall()
            return jsonable_encoder(usuarios)

        finally:
            if conn:
                conn.close()


    # =========================
    # UPDATE
    # =========================
    def update(
        self,
        user_id: int,
        nombre: str,
        apellido: str,
        cedula: str,
        edad: int,
        usuario: str,
        correo: str,
        contrasena: str
    ):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute(
                "SELECT id FROM usuarios WHERE id = %s AND status = TRUE",
                (user_id,)
            )

            if not cur.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )

            hashed_password = hash_password(contrasena)

            cur.execute("""
                UPDATE usuarios
                SET nombre = %s,
                    apellido = %s,
                    cedula = %s,
                    edad = %s,
                    usuario = %s,
                    correo = %s,
                    contrasena = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (
                nombre,
                apellido,
                cedula,
                edad,
                usuario,
                correo,
                hashed_password,
                user_id
            ))

            conn.commit()

            return {"mensaje": "Usuario actualizado correctamente"}

        finally:
            if conn:
                conn.close()


    # =========================
    # DELETE (SOFT DELETE)
    # =========================
    def delete(self, user_id: int):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute(
                "SELECT id FROM usuarios WHERE id = %s AND status = TRUE",
                (user_id,)
            )

            if not cur.fetchone():
                raise HTTPException(
                    status_code=404,
                    detail="Usuario no encontrado"
                )

            cur.execute("""
                UPDATE usuarios
                SET status = FALSE,
                    updated_at = NOW()
                WHERE id = %s
            """, (user_id,))

            conn.commit()

            return {"mensaje": "Usuario eliminado correctamente"}

        finally:
            if conn:
                conn.close()


    # =========================
    # LOGIN
    # =========================
    def login(self, usuario: str, contrasena: str):
        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)

            cur.execute("""
                SELECT id, usuario, contrasena
                FROM usuarios
                WHERE usuario = %s AND status = TRUE
            """, (usuario,))

            user = cur.fetchone()

            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Credenciales incorrectas"
                )

            if not verify_password(contrasena, user["contrasena"]):
                raise HTTPException(
                    status_code=401,
                    detail="Credenciales incorrectas"
                )

            return {
                "mensaje": "Login correcto",
                "usuario": user["usuario"],
                "user_id": user["id"]
            }

        finally:
            if conn:
                conn.close()
