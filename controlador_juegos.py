from bd import obtener_conexion, is_mysql

def _ph():
    return '%s' if is_mysql() else '?'

def insertar_juego(nombre, descripcion, precio):
    conn = obtener_conexion()
    cur = conn.cursor()
    p = _ph()
    cur.execute(f'INSERT INTO juegos(nombre, descripcion, precio) VALUES ({p}, {p}, {p})', (nombre, descripcion, precio))
    conn.commit()
    cur.close()
    conn.close()

def obtener_juegos():
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute('SELECT id, nombre, descripcion, precio FROM juegos')
    juegos = cur.fetchall()
    cur.close()
    conn.close()
    return juegos

def eliminar_juego(id):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute(f'DELETE FROM juegos WHERE id = {_ph()}', (id,))
    conn.commit()
    cur.close()
    conn.close()

def obtener_juego_por_id(id):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute(f'SELECT id, nombre, descripcion, precio FROM juegos WHERE id = {_ph()}', (id,))
    juego = cur.fetchone()
    cur.close()
    conn.close()
    return juego

def actualizar_juego(nombre, descripcion, precio, id):
    conn = obtener_conexion()
    cur = conn.cursor()
    p = _ph()
    cur.execute(f'UPDATE juegos SET nombre = {p}, descripcion = {p}, precio = {p} WHERE id = {p}', (nombre, descripcion, precio, id))
    conn.commit()
    cur.close()
    conn.close()
