import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder

class ReporteController:

    def create(self, mascota_id: int, usuario_id: int, mensaje: str):
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO reportes_informacion (mascota_id, usuario_id, mensaje)
                VALUES (%s, %s, %s)
                RETURNING id, mascota_id, usuario_id, mensaje, created_at, updated_at, status
            """, (mascota_id, usuario_id, mensaje))

            row = cur.fetchone()
            conn.commit()

            return jsonable_encoder({
                "id": row[0],
                "mascota_id": row[1],
                "usuario_id": row[2],
                "mensaje": row[3],
                "created_at": row[4],
                "updated_at": row[5],
                "status": row[6]
            })

        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            conn.close()

    def get_reporte(self, reporte_id: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, mascota_id, usuario_id, mensaje, created_at, updated_at, status
            FROM reportes_informacion
            WHERE id = %s AND status = TRUE
        """, (reporte_id,))

        row = cur.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")

        return jsonable_encoder({
            "id": row[0],
            "mascota_id": row[1],
            "usuario_id": row[2],
            "mensaje": row[3],
            "created_at": row[4],
            "updated_at": row[5],
            "status": row[6]
        })

    def get_reportes(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, mascota_id, usuario_id, mensaje, created_at, updated_at, status
            FROM reportes_informacion
            WHERE status = TRUE
        """)

        rows = cur.fetchall()
        conn.close()

        return jsonable_encoder([
            {
                "id": r[0],
                "mascota_id": r[1],
                "usuario_id": r[2],
                "mensaje": r[3],
                "created_at": r[4],
                "updated_at": r[5],
                "status": r[6]
            } for r in rows
        ])

    def update_reporte(self, reporte_id: int, mensaje: str):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE reportes_informacion
            SET mensaje = %s
            WHERE id = %s AND status = TRUE
            RETURNING id
        """, (mensaje, reporte_id))

        if not cur.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Reporte no encontrado")

        conn.commit()
        conn.close()

        return {"mensaje": "Reporte actualizado correctamente"}

    def delete_reporte(self, reporte_id: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE reportes_informacion
            SET status = FALSE
            WHERE id = %s AND status = TRUE
            RETURNING id
        """, (reporte_id,))

        if not cur.fetchone():
            conn.close()
            raise HTTPException(status_code=404, detail="Reporte no encontrado")

        conn.commit()
        conn.close()

        return {"mensaje": "Reporte eliminado correctamente"}
