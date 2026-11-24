import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-produccion-videojuegos-2026')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///videojuegos_local.db')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
