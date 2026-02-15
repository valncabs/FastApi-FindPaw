from fastapi import HTTPException
from config.db_config import get_db_connection
from datetime import datetime

class MascotaController:

    def create(self, mascota):
        conn = get_db_connection()
        cur = conn.cursor()
        now = datetime.now()

        cur.execute("""
            INSERT INTO mascotas_perdidas (
                usuario_id, nombre, raza, color, tamano, edad_aprox,
                descripcion, ubicacion, fecha_desaparicion, recompensa,
                estado, created_at, updated_at, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            mascota.usuario_id, mascota.nombre, mascota.raza, mascota.color,
            mascota.tamano, mascota.edad_aprox, mascota.descripcion,
            mascota.ubicacion, now, mascota.recompensa,
            "activo", now, now, True
        ))

        mascota_id = cur.fetchone()[0]
        conn.commit()
        conn.close()

        return {
            "id": mascota_id,
            "message": "Mascota registrada correctamente"
        }

    def get_by_id(self, mascota_id: int):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, usuario_id, nombre, raza, color, tamano, edad_aprox,
                   descripcion, ubicacion, fecha_desaparicion, recompensa,
                   estado, created_at, updated_at, status
            FROM mascotas_perdidas
            WHERE id = %s AND status = TRUE
        """, (mascota_id,))

        row = cur.fetchone()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")

        return {
            "id": row[0],
            "usuario_id": row[1],
            "nombre": row[2],
            "raza": row[3],
            "color": row[4],
            "tamano": row[5],
            "edad_aprox": row[6],
            "descripcion": row[7],
            "ubicacion": row[8],
            "fecha_desaparicion": row[9].strftime("%Y-%m-%d %H:%M:%S") if row[9] else None,
            "recompensa": float(row[10]) if row[10] else None,
            "estado": row[11],
            "created_at": row[12].strftime("%Y-%m-%d %H:%M:%S") if row[12] else None,
            "updated_at": row[13].strftime("%Y-%m-%d %H:%M:%S") if row[13] else None,
            "status": row[14]
        }

    def get_all(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, usuario_id, nombre, raza, color, tamano, edad_aprox,
                   descripcion, ubicacion, fecha_desaparicion, recompensa,
                   estado, created_at, updated_at, status
            FROM mascotas_perdidas
            WHERE status = TRUE
        """)
        rows = cur.fetchall()
        conn.close()

        mascotas = []
        for r in rows:
            mascotas.append({
                "id": r[0],
                "usuario_id": r[1],
                "nombre": r[2],
                "raza": r[3],
                "color": r[4],
                "tamano": r[5],
                "edad_aprox": r[6],
                "descripcion": r[7],
                "ubicacion": r[8],
                "fecha_desaparicion": r[9].strftime("%Y-%m-%d %H:%M:%S") if r[9] else None,
                "recompensa": float(r[10]) if r[10] else None,
                "estado": r[11],
                "created_at": r[12].strftime("%Y-%m-%d %H:%M:%S") if r[12] else None,
                "updated_at": r[13].strftime("%Y-%m-%d %H:%M:%S") if r[13] else None,
                "status": r[14]
            })
        return mascotas

    def update(self, mascota_id: int, mascota):
        conn = get_db_connection()
        cur = conn.cursor()
        now = datetime.now()

        cur.execute("""
            UPDATE mascotas_perdidas
            SET nombre=%s, raza=%s, color=%s, tamano=%s, edad_aprox=%s,
                descripcion=%s, ubicacion=%s, recompensa=%s, estado=%s,
                updated_at=%s
            WHERE id=%s AND status=TRUE
            RETURNING id
        """, (
            mascota.nombre, mascota.raza, mascota.color, mascota.tamano, mascota.edad_aprox,
            mascota.descripcion, mascota.ubicacion, mascota.recompensa, "activo",
            now, mascota_id
        ))

        updated = cur.fetchone()
        conn.commit()
        conn.close()

        if not updated:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")

        return {"id": updated[0], "message": "Mascota actualizada correctamente"}

    def delete(self, mascota_id: int):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE mascotas_perdidas
            SET status=FALSE, updated_at=%s
            WHERE id=%s AND status=TRUE
            RETURNING id
        """, (datetime.now(), mascota_id))

        deleted = cur.fetchone()
        conn.commit()
        conn.close()

        if not deleted:
            raise HTTPException(status_code=404, detail="Mascota no encontrada")

        return {"id": deleted[0], "message": "Mascota eliminada correctamente"}
