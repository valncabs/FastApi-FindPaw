from fastapi import HTTPException
from config.db_config import get_db_connection
from datetime import datetime

class ModuloController:

    def create_modulo(self, modulo):
        conn = get_db_connection()
        cur = conn.cursor()

        now = datetime.now()
        cur.execute("""
            INSERT INTO modulos (nombre, descripcion, status, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
        """, (modulo.nombre, modulo.descripcion, modulo.status, now, now))

        modulo_id = cur.fetchone()[0]
        conn.commit()
        conn.close()

        return {
            "id": modulo_id,
            "nombre": modulo.nombre,
            "descripcion": modulo.descripcion,
            "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "status": modulo.status,
            "message": "Módulo creado correctamente"
        }

    def get_modulo(self, modulo_id: int):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, descripcion, created_at, updated_at, status
            FROM modulos
            WHERE id = %s AND status = TRUE
        """, (modulo_id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")

        return {
            "id": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "created_at": row[3].strftime("%Y-%m-%d %H:%M:%S") if row[3] else None,
            "updated_at": row[4].strftime("%Y-%m-%d %H:%M:%S") if row[4] else None,
            "status": row[5]
        }

    def get_modulos(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nombre, descripcion, created_at, updated_at, status
            FROM modulos
            WHERE status = TRUE
        """)
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "nombre": r[1],
                "descripcion": r[2],
                "created_at": r[3].strftime("%Y-%m-%d %H:%M:%S") if r[3] else None,
                "updated_at": r[4].strftime("%Y-%m-%d %H:%M:%S") if r[4] else None,
                "status": r[5]
            } for r in rows
        ]

    def update_modulo(self, modulo_id: int, modulo):
        conn = get_db_connection()
        cur = conn.cursor()
        now = datetime.now()
        cur.execute("""
            UPDATE modulos
            SET nombre = %s,
                descripcion = %s,
                updated_at = %s
            WHERE id = %s AND status = TRUE
            RETURNING id, nombre, descripcion
        """, (modulo.nombre, modulo.descripcion, now, modulo_id))
        updated = cur.fetchone()
        conn.commit()
        conn.close()

        if not updated:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")

        return {
            "id": updated[0],
            "nombre": updated[1],
            "descripcion": updated[2],
            "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
            "message": "Módulo actualizado correctamente"
        }

    def delete_modulo(self, modulo_id: int):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE modulos
            SET status = FALSE,
                updated_at = %s
            WHERE id = %s AND status = TRUE
            RETURNING id
        """, (datetime.now(), modulo_id))
        deleted = cur.fetchone()
        conn.commit()
        conn.close()

        if not deleted:
            raise HTTPException(status_code=404, detail="Módulo no encontrado")

        return {
            "id": deleted[0],
            "message": "Módulo eliminado correctamente"
        }
