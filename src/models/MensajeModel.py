from models.databaseModel import Database

class MensajeModel:
    def __init__(self):
        self.db = Database()

    def enviar(self, id_emisor, id_receptor, contenido, prenda_titulo=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mensaje (id_emisor, id_receptor, contenido, prenda_titulo) VALUES (%s, %s, %s, %s)",
            (id_emisor, id_receptor, contenido, prenda_titulo)
        )
        conn.commit()
        conn.close()

    def obtener_conversacion(self, id_usuario1, id_usuario2):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT * FROM mensaje
               WHERE (id_emisor=%s AND id_receptor=%s) OR (id_emisor=%s AND id_receptor=%s)
               ORDER BY fecha ASC""",
            (id_usuario1, id_usuario2, id_usuario2, id_usuario1)
        )
        msgs = cursor.fetchall()
        conn.close()
        return msgs

    def eliminar_conversacion(self, id_usuario1, id_usuario2):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM mensaje WHERE (id_emisor=%s AND id_receptor=%s) OR (id_emisor=%s AND id_receptor=%s)",
            (id_usuario1, id_usuario2, id_usuario2, id_usuario1)
        )
        conn.commit()
        conn.close()

    def obtener_conversaciones(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT u.id_usuario, u.nombre, u.foto_perfil,
                      ultimo.contenido AS ultimo_mensaje, ultimo.fecha,
                      primero.prenda_titulo
               FROM (
                   SELECT LEAST(id_emisor, id_receptor) AS u1,
                          GREATEST(id_emisor, id_receptor) AS u2,
                          MAX(id_mensaje) AS ultimo_id,
                          MIN(id_mensaje) AS primer_id
                   FROM mensaje
                   WHERE id_emisor=%s OR id_receptor=%s
                   GROUP BY u1, u2
               ) conv
               JOIN mensaje ultimo ON ultimo.id_mensaje = conv.ultimo_id
               JOIN mensaje primero ON primero.id_mensaje = conv.primer_id
               JOIN usuario u ON u.id_usuario = IF(ultimo.id_emisor=%s, ultimo.id_receptor, ultimo.id_emisor)
               ORDER BY ultimo.fecha DESC""",
            (id_usuario, id_usuario, id_usuario)
        )
        convs = cursor.fetchall()
        conn.close()
        return convs
