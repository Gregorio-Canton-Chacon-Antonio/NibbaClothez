import mysql.connector
import bcrypt

conn = mysql.connector.connect(host="localhost", user="root", password="", database="registro")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(150),
    contrasena VARCHAR(300),
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_ingreso TIMESTAMP NULL,
    activo TINYINT DEFAULT 1,
    foto VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tareas (
    id_tarea INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    titulo VARCHAR(200),
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prioridad VARCHAR(50),
    clasificacion VARCHAR(100),
    estado VARCHAR(50),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
)
""")

hashed = bcrypt.hashpw("Admin#19".encode(), bcrypt.gensalt()).decode()
cursor.execute("DELETE FROM usuario WHERE email = 'Admin@gmail.com'")
cursor.execute("""
    INSERT INTO usuario (nombre, apellido, email, contrasena, telefono, activo)
    VALUES ('Admin', 'Admins', 'Admin@gmail.com', %s, '6562321212', 1)
""", (hashed,))

conn.commit()
conn.close()
print("Listo — tablas creadas y usuario Admin insertado")