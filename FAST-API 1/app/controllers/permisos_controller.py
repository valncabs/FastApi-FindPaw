import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder


class PermisoController:

    # GET BY ID
    def get_by_id(self, permiso_id: int):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, rol_id, modulo_id,
                   puede_ver, puede_crear, puede_editar, puede_eliminar,
                   created_at, updated_at, status
            FROM permisos
            WHERE id = %s AND status = TRUE
        """, (permiso_id,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Permiso no encontrado")

        return {
            "id": row[0],
            "rol_id": row[1],
            "modulo_id": row[2],
            "puede_ver": row[3],
            "puede_crear": row[4],
            "puede_editar": row[5],
            "puede_eliminar": row[6],
            "created_at": row[7],
            "updated_at": row[8],
            "status": row[9]
        }

    # GET ALL
    def get_all(self):
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, rol_id, modulo_id,
                   puede_ver, puede_crear, puede_editar, puede_eliminar,
                   created_at, updated_at, status
            FROM permisos
            WHERE status = TRUE
            ORDER BY id
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        permisos = []
        for row in rows:
            permisos.append({
                "id": row[0],
                "rol_id": row[1],
                "modulo_id": row[2],
                "puede_ver": row[3],
                "puede_crear": row[4],
                "puede_editar": row[5],
                "puede_eliminar": row[6],
                "created_at": row[7],
                "updated_at": row[8],
                "status": row[9]
            })

        return permisos

    # CREATE
    def create(self, rol_id: int, modulo_id: int, puede_ver: bool, puede_crear: bool, puede_editar: bool, puede_eliminar: bool):
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO permisos (
                    rol_id, modulo_id, puede_ver, puede_crear, puede_editar, puede_eliminar
                ) VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (rol_id, modulo_id, puede_ver, puede_crear, puede_editar, puede_eliminar))

            permiso_id = cur.fetchone()[0]
            conn.commit()

            return {"id": permiso_id, "mensaje": "Permiso creado correctamente"}

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear permiso: {str(e)}")

        finally:
            if conn:
                conn.close()

    # UPDATE
    def update(self, permiso_id: int, rol_id: int, modulo_id: int, puede_ver: bool, puede_crear: bool, puede_editar: bool, puede_eliminar: bool):
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Verificar que el permiso existe y está activo
            cur.execute("SELECT id FROM permisos WHERE id = %s AND status = TRUE", (permiso_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Permiso no encontrado")

            # Actualizar
            cur.execute("""
                UPDATE permisos
                SET rol_id = %s,
                    modulo_id = %s,
                    puede_ver = %s,
                    puede_crear = %s,
                    puede_editar = %s,
                    puede_eliminar = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (rol_id, modulo_id, puede_ver, puede_crear, puede_editar, puede_eliminar, permiso_id))

            conn.commit()
            return {"mensaje": "Permiso actualizado correctamente"}

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar permiso: {str(e)}")

        finally:
            if conn:
                conn.close()

    # DELETE (soft delete)
    def delete(self, permiso_id: int):
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Verificar que el permiso existe y está activo
            cur.execute("SELECT id FROM permisos WHERE id = %s AND status = TRUE", (permiso_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="Permiso no encontrado")

            # Soft delete
            cur.execute("""
                UPDATE permisos
                SET status = FALSE,
                    updated_at = NOW()
                WHERE id = %s
            """, (permiso_id,))

            conn.commit()
            return {"mensaje": "Permiso eliminado correctamente"}

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar permiso: {str(e)}")

        finally:
            if conn:
                conn.close()
