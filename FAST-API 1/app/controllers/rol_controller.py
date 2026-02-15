import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder

class RolController:

    # CREATE
    def create(self, nombre: str):
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO roles (nombre)
                VALUES (%s)
                RETURNING id, nombre, created_at, updated_at, status
            """, (nombre,))

            row = cur.fetchone()
            conn.commit()

            return jsonable_encoder({
                "id": row[0],
                "nombre": row[1],
                "created_at": row[2],
                "updated_at": row[3],
                "status": row[4]
            })

        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()

    # GET BY ID
    def get_by_id(self, rol_id: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nombre, created_at, updated_at, status
            FROM roles
            WHERE id = %s AND status = TRUE
        """, (rol_id,))

        row = cur.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        return jsonable_encoder({
            "id": row[0],
            "nombre": row[1],
            "created_at": row[2],
            "updated_at": row[3],
            "status": row[4]
        })

    # GET ALL
    def get_all(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nombre, created_at, updated_at, status
            FROM roles
            WHERE status = TRUE
        """)

        rows = cur.fetchall()
        conn.close()

        return jsonable_encoder([
            {
                "id": r[0],
                "nombre": r[1],
                "created_at": r[2],
                "updated_at": r[3],
                "status": r[4]
            } for r in rows
        ])

    # UPDATE
    def update(self, rol_id: int, nombre: str):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE roles
            SET nombre = %s
            WHERE id = %s AND status = TRUE
            RETURNING id
        """, (nombre, rol_id))

        if not cur.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        conn.commit()
        conn.close()

        return {"mensaje": "Rol actualizado correctamente"}

    # DELETE LÓGICO
    def delete(self, rol_id: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE roles
            SET status = FALSE
            WHERE id = %s AND status = TRUE
            RETURNING id
        """, (rol_id,))

        if not cur.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Rol no encontrado")

        conn.commit()
        conn.close()

        return {"mensaje": "Rol eliminado correctamente"}
