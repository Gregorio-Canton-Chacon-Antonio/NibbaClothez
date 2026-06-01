from models.PrendaModel import PrendaModel

class PrendaController:
    def __init__(self):
        self.model = PrendaModel()

    def obtener_lista(self, id_usuario):
        return self.model.listar_por_usuario(id_usuario)

    def obtener_todas(self):
        return self.model.listar_todas()

    def guardar_nueva(self, id_usuario, titulo, precio, talla, condicion, marca, descripcion, foto=""):
        if not titulo:
            return False, "El título es obligatorio"
        if not precio:
            return False, "El precio es obligatorio"
        try:
            self.model.crear(id_usuario, titulo, float(precio), talla, condicion, marca, descripcion, foto)
            return True, "Prenda guardada"
        except ValueError:
            return False, "El precio debe ser un número válido"

    def editar_prenda(self, id_usuario, id_prenda, titulo, precio, talla, condicion, marca, descripcion, foto=None):
        if not titulo:
            return False, "El título es obligatorio"
        try:
            self.model.actualizar(id_prenda, titulo, float(precio), talla, condicion, marca, descripcion, foto)
            return True, "Prenda actualizada"
        except ValueError:
            return False, "El precio debe ser un número válido"

    def eliminar_prenda(self, id_usuario, id_prenda):
        try:
            self.model.eliminar(id_prenda)
            return True, "Prenda eliminada"
        except Exception as e:
            return False, str(e)
