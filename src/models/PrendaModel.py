from models.databaseModel import Database

class PrendaModel:
    def __init__(self):
        self.db = Database()

    def listar_por_usuario(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM prenda WHERE id_usuario = %s ORDER BY fecha_subida DESC", (id_usuario,))
        resultado = cursor.fetchall()
        conn.close()
        return resultado

    def crear(self, id_usuario, titulo, precio, talla, condicion, marca, descripcion, foto=""):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prenda (id_usuario, foto, titulo, precio, talla, condicion, marca, descripcion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (id_usuario, foto, titulo, precio, talla, condicion, marca, descripcion)
        )
        conn.commit()
        conn.close()

    def actualizar(self, id_prenda, titulo, precio, talla, condicion, marca, descripcion, foto=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        if foto is not None:
            cursor.execute(
                "UPDATE prenda SET titulo=%s, precio=%s, talla=%s, condicion=%s, marca=%s, descripcion=%s, foto=%s WHERE id_prenda=%s",
                (titulo, precio, talla, condicion, marca, descripcion, foto, id_prenda)
            )
        else:
            cursor.execute(
                "UPDATE prenda SET titulo=%s, precio=%s, talla=%s, condicion=%s, marca=%s, descripcion=%s WHERE id_prenda=%s",
                (titulo, precio, talla, condicion, marca, descripcion, id_prenda)
            )
        conn.commit()
        conn.close()

    def eliminar(self, id_prenda):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prenda WHERE id_prenda = %s", (id_prenda,))
        conn.commit()
        conn.close()
