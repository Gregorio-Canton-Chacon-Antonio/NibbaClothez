import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

TABLAS = [
    """CREATE TABLE IF NOT EXISTS `usuario` (
        `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
        `nombre` varchar(100) NOT NULL,
        `email` varchar(150) NOT NULL,
        `password` varchar(255) NOT NULL,
        `foto_perfil` MEDIUMTEXT DEFAULT NULL,
        `fecha_registro` timestamp NULL DEFAULT current_timestamp(),
        `ultimo_acceso` timestamp NULL DEFAULT NULL,
        `activo` tinyint(1) DEFAULT 1,
        PRIMARY KEY (`id_usuario`),
        UNIQUE KEY `email` (`email`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",

    """CREATE TABLE IF NOT EXISTS `password_resets` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `id_usuario` int(11) NOT NULL,
        `token` varchar(6) NOT NULL,
        `expires_at` datetime NOT NULL,
        PRIMARY KEY (`id`),
        KEY `id_usuario` (`id_usuario`),
        CONSTRAINT `password_resets_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",

    """CREATE TABLE IF NOT EXISTS `prenda` (
        `id_prenda` int(11) NOT NULL AUTO_INCREMENT,
        `id_usuario` int(11) NOT NULL,
        `foto` longtext DEFAULT NULL,
        `titulo` varchar(200) NOT NULL,
        `precio` decimal(10,2) NOT NULL,
        `talla` varchar(50) NOT NULL,
        `condicion` enum('nuevo','como_nuevo','usado_excelente','usado_buen_estado','usado_aceptable') NOT NULL,
        `marca` varchar(100) DEFAULT 'Sin marca',
        `descripcion` text DEFAULT NULL,
        `tags` text DEFAULT NULL,
        `fecha_subida` timestamp NULL DEFAULT current_timestamp(),
        `vendido` tinyint(1) DEFAULT 0,
        `genero` varchar(20) NOT NULL DEFAULT 'Unisex',
        `categoria` varchar(50) NOT NULL DEFAULT 'Ropa Superior',
        PRIMARY KEY (`id_prenda`),
        KEY `fk_vendedor` (`id_usuario`),
        CONSTRAINT `fk_vendedor_prenda` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",

    """CREATE TABLE IF NOT EXISTS `prenda_foto` (
        `id_foto` int(11) NOT NULL AUTO_INCREMENT,
        `id_prenda` int(11) NOT NULL,
        `imagen` MEDIUMBLOB NOT NULL,
        `orden` int(11) DEFAULT 0,
        PRIMARY KEY (`id_foto`),
        KEY `id_prenda` (`id_prenda`),
        CONSTRAINT `fk_prenda_foto` FOREIGN KEY (`id_prenda`) REFERENCES `prenda` (`id_prenda`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",

    """CREATE TABLE IF NOT EXISTS `mensaje` (
        `id_mensaje` int(11) NOT NULL AUTO_INCREMENT,
        `id_emisor` int(11) NOT NULL,
        `id_receptor` int(11) NOT NULL,
        `contenido` text NOT NULL,
        `prenda_titulo` varchar(200) DEFAULT NULL,
        `fecha` timestamp NULL DEFAULT current_timestamp(),
        `leido` tinyint(1) DEFAULT 0,
        PRIMARY KEY (`id_mensaje`),
        KEY `id_emisor` (`id_emisor`),
        KEY `id_receptor` (`id_receptor`),
        CONSTRAINT `fk_mensaje_emisor` FOREIGN KEY (`id_emisor`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE,
        CONSTRAINT `fk_mensaje_receptor` FOREIGN KEY (`id_receptor`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""",
]

MIGRACIONES = [
    "ALTER TABLE usuario MODIFY COLUMN foto_perfil MEDIUMTEXT DEFAULT NULL",
    "ALTER TABLE mensaje ADD COLUMN IF NOT EXISTS prenda_titulo varchar(200) DEFAULT NULL",
]

def init_db():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS `nibba_clothez` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute("USE `nibba_clothez`")
    for sql in TABLAS:
        cursor.execute(sql)
    for sql in MIGRACIONES:
        try:
            cursor.execute(sql)
        except Exception:
            pass
    conn.commit()
    conn.close()
