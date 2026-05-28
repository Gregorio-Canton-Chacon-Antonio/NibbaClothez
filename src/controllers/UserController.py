import secrets
import os
import yagmail
from dotenv import load_dotenv
from models.UsersModel import UsuarioModel
from models.schemasModel import UsuarioShema
from pydantic import ValidationError

load_dotenv()

class AuthController:
    def __init__(self):
        self.model = UsuarioModel()

    def registrar_Usuario(self, nombre, email, contrasena):
        try:
            nuevo = UsuarioShema(nombre=nombre, email=email, password=contrasena)
            if self.model.registrar(nuevo):
                return True, "Usuario creado correctamente"
            return False, "El correo ya está registrado o hubo un error en el servidor"
        except ValidationError as e:
            return False, e.errors()[0]['msg']
        except Exception as e:
            return False, str(e)

    def login(self, email, password):
        try:
            user = self.model.validar_login(email, password)
            return (user, "Login correcto") if user else (False, "Credenciales incorrectas")
        except Exception as e:
            return False, str(e)

    def solicitar_recuperacion(self, email):
        try:
            user = self.model.buscar_por_email(email)
            if not user:
                return False, None, "No existe una cuenta con ese correo"
            token = str(secrets.randbelow(900000) + 100000)
            self.model.guardar_token(user['id_usuario'], token)
            yag = yagmail.SMTP(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
            yag.send(
                to=email,
                subject="Recuperación de contraseña - Nibba Clothez",
                contents=f"Hola {user['nombre']},\n\nTu código de recuperación es: {token}\n\nEste código expira en 15 minutos.\n\nSi no solicitaste esto, ignora este correo."
            )
            return True, user['id_usuario'], "Código enviado"
        except Exception as e:
            return False, None, str(e)

    def verificar_token(self, id_usuario, token):
        try:
            valido = self.model.verificar_token(id_usuario, token)
            return valido, "Token válido" if valido else "Código incorrecto o expirado"
        except Exception as e:
            return False, str(e)

    def cambiar_password(self, id_usuario, nueva_password):
        try:
            ok = self.model.actualizar_password(id_usuario, nueva_password)
            return ok, "Contraseña actualizada" if ok else "Error al actualizar"
        except Exception as e:
            return False, str(e)