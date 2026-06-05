from models.MensajeModel import MensajeModel

class MensajeController:
    def __init__(self):
        self.model = MensajeModel()

    def enviar(self, id_emisor, id_receptor, contenido, prenda_titulo=None):
        try:
            self.model.enviar(id_emisor, id_receptor, contenido, prenda_titulo)
            return True
        except Exception as e:
            print(f"[ERROR] enviar mensaje: {e}")
            return False

    def obtener_conversacion(self, id_usuario1, id_usuario2):
        try:
            return self.model.obtener_conversacion(id_usuario1, id_usuario2)
        except Exception as e:
            print(f"[ERROR] obtener_conversacion: {e}")
            return []

    def eliminar_conversacion(self, id_usuario1, id_usuario2):
        try:
            self.model.eliminar_conversacion(id_usuario1, id_usuario2)
            return True
        except Exception as e:
            print(f"[ERROR] eliminar_conversacion: {e}")
            return False

    def obtener_conversaciones(self, id_usuario):
        try:
            return self.model.obtener_conversaciones(id_usuario)
        except Exception as e:
            print(f"[ERROR] obtener_conversaciones: {e}")
            return []
