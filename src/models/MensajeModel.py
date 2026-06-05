from models.databaseModel import Database

class MensajeModel:
    def __init__(self):
        self.db = Database()

    def enviar(self, id_emisor, id_receptor, contenido):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mensaje (id_emisor, id_receptor, contenido) VALUES (%s, %s, %s)",
            (id_emisor, id_receptor, contenido)
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

    def obtener_conversaciones(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT u.id_usuario, u.nombre, u.foto_perfil,
                      m.contenido AS ultimo_mensaje, m.fecha
               FROM mensaje m
               JOIN usuario u ON u.id_usuario = IF(m.id_emisor=%s, m.id_receptor, m.id_emisor)
               WHERE m.id IN (
                   SELECT MAX(id_mensaje) FROM mensaje
                   WHERE id_emisor=%s OR id_receptor=%s
                   GROUP BY LEAST(id_emisor, id_receptor), GREATEST(id_emisor, id_receptor)
               )
               ORDER BY m.fecha DESC""",
            (id_usuario, id_usuario, id_usuario)
        )
        convs = cursor.fetchall()
        conn.close()
        return convs
