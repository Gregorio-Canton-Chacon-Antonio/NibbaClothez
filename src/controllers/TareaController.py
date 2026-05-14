from models.TareasModel import TareaModel

class TareaController:
    def __init__(self):
        self.model = TareaModel()

    def obtener_lista(self, id_usuario):
        return self.model.listar_por_usuario(id_usuario)

    def guardar_nueva(self, id_usuario, titulo, descripcion, prioridad, clasificacion, estado):
        if not titulo:
            return False, "El título es obligatorio"
        self.model.crear(id_usuario, titulo, descripcion, prioridad, clasificacion, estado)
        return True, "Tarea guardada"

    def eliminar_tarea(self, id_tarea):
        try:
            self.model.eliminar(id_tarea)
            return True, "Tarea eliminada"
        except Exception as e:
            return False, str(e)