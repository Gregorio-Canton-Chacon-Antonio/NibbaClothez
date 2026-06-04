import bcrypt
import base64
from models.databaseModel import Database

class UsuarioModel:
    def __init__(self):
        self.db = Database()

    def registrar(self, usuario_data):
        hashed_pw = bcrypt.hashpw(usuario_data.password.encode('utf-8'), bcrypt.gensalt())
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuario (nombre, email, password) VALUES (%s, %s, %s)",
                (usuario_data.nombre, usuario_data.email, hashed_pw.decode('utf-8'))
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()

    def validar_login(self, email, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            if user.get("foto_perfil") and isinstance(user["foto_perfil"], (bytes, bytearray)):
                user["foto_perfil"] = "data:image/jpeg;base64," + base64.b64encode(user["foto_perfil"]).decode()
            return user
        return None

    def buscar_por_email(self, email):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nombre, email FROM usuario WHERE email=%s AND activo=1", (email,))
        user = cursor.fetchone()
        conn.close()
        return user

    def buscar_por_id(self, id_usuario):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario, nombre, email, foto_perfil FROM usuario WHERE id_usuario=%s", (id_usuario,))
        user = cursor.fetchone()
        conn.close()
        if user and user.get("foto_perfil"):
            fp = user["foto_perfil"]
            if isinstance(fp, (bytes, bytearray)):
                user["foto_perfil"] = "data:image/jpeg;base64," + base64.b64encode(fp).decode()
            else:
                user["foto_perfil"] = None
        return user

    def guardar_foto_perfil(self, id_usuario, foto_bytes):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuario SET foto_perfil=%s WHERE id_usuario=%s", (foto_bytes, id_usuario))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()

    def guardar_token(self, id_usuario, token):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM password_resets WHERE id_usuario=%s", (id_usuario,))
            cursor.execute(
                "INSERT INTO password_resets (id_usuario, token, expires_at) VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 15 MINUTE))",
                (id_usuario, token)
            )
            conn.commit()
        finally:
            conn.close()

    def verificar_token(self, id_usuario, token):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM password_resets WHERE id_usuario=%s AND token=%s AND expires_at > NOW()",
            (id_usuario, token)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def actualizar_password(self, id_usuario, nueva_password):
        hashed = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt())
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuario SET password=%s WHERE id_usuario=%s", (hashed.decode('utf-8'), id_usuario))
            cursor.execute("DELETE FROM password_resets WHERE id_usuario=%s", (id_usuario,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()