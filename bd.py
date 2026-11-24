import os, sqlite3
from urllib.parse import urlparse
import pymysql

def obtener_conexion():
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///videojuegos_local.db')
    if db_url.startswith('mysql'):
        parsed = urlparse(db_url.replace('mysql+pymysql://', 'mysql://'))
        return pymysql.connect(
            host=parsed.hostname or 'db',
            port=parsed.port or 3306,
            user=parsed.username or 'root',
            password=parsed.password or '',
            database=(parsed.path or '/juegos').lstrip('/'),
            charset='utf8mb4'
        )
    db_path = db_url.replace('sqlite:///', '') or 'videojuegos_local.db'
    return sqlite3.connect(db_path)

def is_mysql():
    return os.environ.get('DATABASE_URL', '').startswith('mysql')

def init_db():
    conn = obtener_conexion()
    cur = conn.cursor()
    if is_mysql():
        cur.execute('CREATE TABLE IF NOT EXISTS usuarios (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL)')
        cur.execute('CREATE TABLE IF NOT EXISTS juegos (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, descripcion VARCHAR(255) NOT NULL, precio DECIMAL(10,2) NOT NULL)')
    else:
        cur.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL)')
        cur.execute('CREATE TABLE IF NOT EXISTS juegos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, descripcion TEXT NOT NULL, precio REAL NOT NULL)')
    conn.commit()
    cur.close()
    conn.close()
