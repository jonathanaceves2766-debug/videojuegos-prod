from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bd import obtener_conexion, is_mysql

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = str(id)
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_user(username, password):
        pw_hash = generate_password_hash(password)
        ph = '%s' if is_mysql() else '?'
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(f'INSERT INTO usuarios (username, password_hash) VALUES ({ph}, {ph})', (username, pw_hash))
        conn.commit()
        uid = cur.lastrowid
        cur.close()
        conn.close()
        return User(uid, username, pw_hash)

    @staticmethod
    def get_by_username(username):
        ph = '%s' if is_mysql() else '?'
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(f'SELECT id, username, password_hash FROM usuarios WHERE username = {ph}', (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return User(row[0], row[1], row[2]) if row else None

    @staticmethod
    def get_by_id(user_id):
        ph = '%s' if is_mysql() else '?'
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute(f'SELECT id, username, password_hash FROM usuarios WHERE id = {ph}', (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return User(row[0], row[1], row[2]) if row else None
