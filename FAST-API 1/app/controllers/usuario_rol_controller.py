import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder

class UsuarioRolController:

    # CREATE
    def create(self, usuario_id: int, rol_id: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO usuario_rol (usuario_id, rol_id)
                VALUES (%s, %s)
                RETURNING id, usuario_id, rol_id, created_at, updated_at, status
            """, (usuario_id, rol_id))

            row = cur.fetchone()
            conn.commit()

            return jsonable_encoder({
                "id": row[0],
                "usuario_id": row[1],
                "rol_id": row[2],
                "created_at": row[3],
                "updated_at": row[4],
                "status": row[5]
            })

        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()

    # GET BY ID
    def get_by_id(self, ur_id: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, usuario_id, rol_id, created_at, updated_at, status
            FROM usuario_rol
            WHERE id = %s AND status = TRUE
        """, (ur_id,))

        row = cur.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Usuario-Rol no encontrado")

        return jsonable_encoder({
            "id": row[0],
            "usuario_id": row[1],
            "rol_id": row[2],
            "created_at": row[3],
            "updated_at": row[4],
            "status": row[5]
        })

    # GET ALL
    def get_all(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, usuario_id, rol_id, created_at, updated_at, status
            FROM usuario_rol
            WHERE status = TRUE
        """)

        rows = cur.fetchall()
        conn.close()

        return jsonable_encoder([
            {
                "id": r[0],
                "usuario_id": r[1],
                "rol_id": r[2],
                "created_at": r[3],
                "updated_at": r[4],
                "status": r[5]
            } for r in rows
        ])

    # DELETE LÓGICO
    def delete(self, ur_id: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE usuario_rol
            SET status = FALSE
            WHERE id = %s AND status = TRUE
            RETURNING id
        """, (ur_id,))

        if not cur.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Usuario-Rol no encontrado")

        conn.commit()
        conn.close()

        return {"mensaje": "Relación eliminada correctamente"}
