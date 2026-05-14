from models.databaseModel import Database

class TareaModel:
    def __init__(self):
        self.db = Database()

    def listar_por_usuario(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tareas WHERE id_usuario = %s", (id_usuario,))
        resultado = cursor.fetchall()
        conn.close()
        return resultado

    def crear(self, id_usuario, titulo, descripcion, prioridad, clasificacion, estado):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tareas (id_usuario, titulo, descripcion, prioridad, clasificacion, estado) VALUES (%s, %s, %s, %s, %s, %s)",
            (id_usuario, titulo, descripcion, prioridad, clasificacion, estado)
        )
        conn.commit()
        conn.close()

    def eliminar(self, id_tarea):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id_tarea = %s", (id_tarea,))
        conn.commit()
        conn.close()