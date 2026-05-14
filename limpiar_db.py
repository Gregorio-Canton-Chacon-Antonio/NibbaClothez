import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydbmane"
)

cursor = conn.cursor(dictionary=True)

# Ver usuarios
print("=== USUARIOS REGISTRADOS ===")
cursor.execute("SELECT * FROM usuario")
usuarios = cursor.fetchall()

if usuarios:
    for u in usuarios:
        print(f"\nID: {u.get('id_usuario')}")
        print(f"Nombre: {u.get('nombre')} {u.get('apellido') or ''}")
        print(f"Email: {u.get('email')}")
        print(f"Teléfono: {u.get('telefono') or 'N/A'}")
        print(f"Registro: {u.get('fecha_registro')}")
        print("-" * 40)
else:
    print("No hay usuarios registrados")

# Preguntar si quiere limpiar
print("\n¿Deseas eliminar todos los usuarios? (s/n): ", end="")
respuesta = input().lower()

if respuesta == 's':
    cursor.execute("DELETE FROM tareas")
    cursor.execute("DELETE FROM usuario")
    conn.commit()
    print("✓ Base de datos limpiada")
else:
    print("Operación cancelada")

conn.close()
