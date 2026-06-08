"""
Script de datos de prueba — ejecutar una sola vez después de init_db.
Crea un usuario vendedor y 4 prendas con 2 fotos cada una.
"""
import os
import sys
import bcrypt
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "img")

USUARIO = {
    "nombre": "Vendedor Demo",
    "email": "demo@nibba.com",
    "password": "Demo1234!",
}

PRENDAS = [
    {
        "titulo": "Chamarra de Cuero Negra",
        "precio": 850.00,
        "talla": "XL",
        "condicion": "como_nuevo",
        "marca": "NASCAR",
        "descripcion": "Chamarra de cuero genuino negro, corte ancho, perfecta para el otoño. Con cierre frontal y bolsillos laterales.",
        "genero": "Hombres",
        "categoria": "Ropa Exterior",
        "fotos": ["prenda1.jpeg", "prenda1.1.jpeg"],
    },
    {
        "titulo": "Chamarra de Poliester negra",
        "precio": 320.00,
        "talla": "M",
        "condicion": "usado_buen_estado",
        "marca": "JH Design",
        "descripcion": "Chamarra de poliester negro, corte recto, comodo y duradero. Ideal para uso diario.",
        "genero": "Hombres",
        "categoria": "Ropa Inferior",
        "fotos": ["prenda2.jpeg", "prenda2.2.jpeg"],
    },
    {
        "titulo": "Chamarra de Cuero sintetico",
        "precio": 180.00,
        "talla": "M",
        "condicion": "nuevo",
        "marca": "Stilo's",
        "descripcion": "Chamarra de cuero sintetico, color rojo y negro, perfecta para el invierno. Sin uso.",
        "genero": "Mujeres",
        "categoria": "Ropa Superior",
        "fotos": ["prenda3.jpeg", "prenda3.3.jpeg"],
    },
    {
        "titulo": "Jersey Azul marino",
        "precio": 240.00,
        "talla": "XL",
        "condicion": "como_nuevo",
        "marca": "Reebok",
        "descripcion": "Jersey azul marino de la nfl. Perfecto para el verano.",
        "genero": "Mujeres",
        "categoria": "Ropa Inferior",
        "fotos": ["prenda4.jpeg", "prenda4.4.jpeg"],
    },
]


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database="nibba_clothez",
    )


def leer_imagen(nombre):
    path = os.path.join(IMG_DIR, nombre)
    if not os.path.exists(path):
        print(f"  ADVERTENCIA: imagen no encontrada — {path}")
        return None
    with open(path, "rb") as f:
        return f.read()


def main():
    conn = conectar()
    cursor = conn.cursor()

    # Usuario de prueba
    cursor.execute("SELECT id_usuario FROM usuario WHERE email = %s", (USUARIO["email"],))
    row = cursor.fetchone()
    if row:
        id_usuario = row[0]
        print(f"Usuario demo ya existe (id={id_usuario}), se omite creación.")
    else:
        hashed = bcrypt.hashpw(USUARIO["password"].encode(), bcrypt.gensalt()).decode()
        foto_path = os.path.join(IMG_DIR, "Nibbaz.jpeg")
        foto_b64 = None
        if os.path.exists(foto_path):
            import base64
            with open(foto_path, "rb") as f:
                foto_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
        cursor.execute(
            "INSERT INTO usuario (nombre, email, password, foto_perfil) VALUES (%s, %s, %s, %s)",
            (USUARIO["nombre"], USUARIO["email"], hashed, foto_b64),
        )
        id_usuario = cursor.lastrowid
        print(f"Usuario demo creado (id={id_usuario})  email={USUARIO['email']}  pass={USUARIO['password']}")

    # Prendas de prueba
    for p in PRENDAS:
        cursor.execute("SELECT id_prenda FROM prenda WHERE titulo = %s AND id_usuario = %s", (p["titulo"], id_usuario))
        if cursor.fetchone():
            print(f"  Prenda '{p['titulo']}' ya existe, se omite.")
            continue

        cursor.execute(
            "INSERT INTO prenda (id_usuario, foto, titulo, precio, talla, condicion, marca, descripcion, genero, categoria) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (id_usuario, "", p["titulo"], p["precio"], p["talla"], p["condicion"],
             p["marca"], p["descripcion"], p["genero"], p["categoria"]),
        )
        id_prenda = cursor.lastrowid

        for orden, nombre_foto in enumerate(p["fotos"]):
            data = leer_imagen(nombre_foto)
            if data:
                cursor.execute(
                    "INSERT INTO prenda_foto (id_prenda, imagen, orden) VALUES (%s, %s, %s)",
                    (id_prenda, data, orden),
                )

        print(f"  Prenda insertada: '{p['titulo']}' — {p['genero']} / {p['categoria']} — ${p['precio']}")

    conn.commit()
    conn.close()
    print("\nDatos de prueba cargados correctamente.")


if __name__ == "__main__":
    main()
