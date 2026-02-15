from fastapi import HTTPException
from config.db_config import get_db_connection
from datetime import datetime

class ImagenController:

    def create_imagen(self, imagen):
        conn = get_db_connection()
        cur = conn.cursor()
        now = datetime.now()

        cur.execute("""
            INSERT INTO imagenes_mascota (mascota_id, url_imagen, created_at, updated_at, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            imagen.mascota_id, imagen.url_imagen, now, now, True
        ))

        imagen_id = cur.fetchone()[0]
        conn.commit()
        conn.close()

        return {"id": imagen_id, "message": "Imagen registrada correctamente"}

    def get_imagen(self, imagen_id: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, mascota_id, url_imagen, created_at, updated_at, status
            FROM imagenes_mascota
            WHERE id = %s AND status = TRUE
        """, (imagen_id,))

        row = cur.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")

        return {
            "id": row[0],
            "mascota_id": row[1],
            "url_imagen": row[2],
            "created_at": row[3].strftime("%Y-%m-%d %H:%M:%S") if row[3] else None,
            "updated_at": row[4].strftime("%Y-%m-%d %H:%M:%S") if row[4] else None,
            "status": row[5]
        }

    def get_imagenes(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, mascota_id, url_imagen, created_at, updated_at, status
            FROM imagenes_mascota
            WHERE status = TRUE
        """)

        rows = cur.fetchall()
        conn.close()

        imagenes = []
        for r in rows:
            imagenes.append({
                "id": r[0],
                "mascota_id": r[1],
                "url_imagen": r[2],
                "created_at": r[3].strftime("%Y-%m-%d %H:%M:%S") if r[3] else None,
                "updated_at": r[4].strftime("%Y-%m-%d %H:%M:%S") if r[4] else None,
                "status": r[5]
            })
        return imagenes

    def update_imagen(self, imagen_id: int, imagen):
        conn = get_db_connection()
        cur = conn.cursor()
        now = datetime.now()

        cur.execute("""
            UPDATE imagenes_mascota
            SET url_imagen=%s, updated_at=%s
            WHERE id=%s AND status=TRUE
            RETURNING id
        """, (imagen.url_imagen, now, imagen_id))

        updated = cur.fetchone()
        conn.commit()
        conn.close()

        if not updated:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")

        return {"id": updated[0], "message": "Imagen actualizada correctamente"}

    def delete_imagen(self, imagen_id: int):
        conn = get_db_connection()
        cur = conn.cursor()
        now = datetime.now()

        cur.execute("""
            UPDATE imagenes_mascota
            SET status=FALSE, updated_at=%s
            WHERE id=%s AND status=TRUE
            RETURNING id
        """, (now, imagen_id))

        deleted = cur.fetchone()
        conn.commit()
        conn.close()

        if not deleted:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")

        return {"id": deleted[0], "message": "Imagen eliminada correctamente"}