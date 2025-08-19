import os

# Configuración de seguridad
SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-segura'

# Configuración de usuario administrador por defecto
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'