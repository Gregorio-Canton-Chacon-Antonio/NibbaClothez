import base64
from models.databaseModel import Database

class PrendaModel:
    def __init__(self):
        self.db = Database()

    def _adjuntar_fotos(self, cursor, prendas):
        if not prendas:
            return prendas
        ids = [p["id_prenda"] for p in prendas]
        fmt = ",".join(["%s"] * len(ids))
        cursor.execute(f"SELECT id_prenda, imagen FROM prenda_foto WHERE id_prenda IN ({fmt}) ORDER BY orden", ids)
        fotos_map = {}
        for row in cursor.fetchall():
            fotos_map.setdefault(row["id_prenda"], []).append(
                "data:image/jpeg;base64," + base64.b64encode(row["imagen"]).decode()
            )
        for p in prendas:
            p["foto"] = "|".join(fotos_map.get(p["id_prenda"], []))
        return prendas

    def listar_por_usuario(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prenda WHERE id_usuario = %s ORDER BY fecha_subida DESC", (id_usuario,))
        prendas = cursor.fetchall()
        self._adjuntar_fotos(cursor, prendas)
        conn.close()
        return prendas

    def listar_todas(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prenda ORDER BY fecha_subida DESC")
        prendas = cursor.fetchall()
        self._adjuntar_fotos(cursor, prendas)
        conn.close()
        return prendas

    def crear(self, id_usuario, titulo, precio, talla, condicion, marca, descripcion, fotos_bytes=None, genero="Unisex", categoria="Ropa Superior"):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prenda (id_usuario, foto, titulo, precio, talla, condicion, marca, descripcion, genero, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (id_usuario, "", titulo, precio, talla, condicion, marca, descripcion, genero, categoria)
        )
        id_prenda = cursor.lastrowid
        if fotos_bytes:
            for i, fb in enumerate(fotos_bytes):
                cursor.execute("INSERT INTO prenda_foto (id_prenda, imagen, orden) VALUES (%s, %s, %s)", (id_prenda, fb, i))
        conn.commit()
        conn.close()

    def actualizar(self, id_prenda, titulo, precio, talla, condicion, marca, descripcion, fotos_bytes=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE prenda SET titulo=%s, precio=%s, talla=%s, condicion=%s, marca=%s, descripcion=%s WHERE id_prenda=%s",
            (titulo, precio, talla, condicion, marca, descripcion, id_prenda)
        )
        if fotos_bytes is not None:
            cursor.execute("DELETE FROM prenda_foto WHERE id_prenda=%s", (id_prenda,))
            for i, fb in enumerate(fotos_bytes):
                cursor.execute("INSERT INTO prenda_foto (id_prenda, imagen, orden) VALUES (%s, %s, %s)", (id_prenda, fb, i))
        conn.commit()
        conn.close()

    def eliminar(self, id_prenda):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prenda_foto WHERE id_prenda = %s", (id_prenda,))
        cursor.execute("DELETE FROM prenda WHERE id_prenda = %s", (id_prenda,))
        conn.commit()
        conn.close()
