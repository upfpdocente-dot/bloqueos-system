# 🚦 Sistema de Registro de Bloqueos

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-2.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-purple)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Render](https://img.shields.io/badge/Deploy-Render-black)
![License](https://img.shields.io/badge/License-MIT-yellow)

Sistema web completo para registro y administración de bloqueos vehiculares con interfaz moderna y panel administrativo.

## 🌐 Demo en Vivo
**[👉 Ver aplicación funcionando](https://bloqueos-system.onrender.com)**

## 📸 Capturas de Pantalla

### Interfaz de Usuario
![Formulario de Registro](https://via.placeholder.com/800x400/4A90E2/FFFFFF?text=Formulario+de+Registro+de+Bloqueos)

### Panel de Administración  
![Panel Admin](https://via.placeholder.com/800x400/50C878/FFFFFF?text=Panel+de+Administración)

### Reportes Gráficos
![Gráficos Estadísticos](https://via.placeholder.com/800x400/FF6B6B/FFFFFF?text=Reportes+Gráficos+Interactivos)

## 🚀 Características Principales

### Para Usuarios
- ✨ **Formulario intuitivo** para registro de bloqueos
- 📱 **Interfaz responsive** que funciona en móviles
- ✅ **Validaciones en tiempo real**
- 💾 **Guardado automático** de datos

### Para Administradores
- 📊 **Dashboard completo** con todos los registros
- 📈 **Gráficos interactivos** con Chart.js
- 👥 **Gestión de usuarios** y permisos
- 🔍 **Búsqueda y filtros** avanzados

## 🛠️ Tecnologías Utilizadas

| Frontend | Backend | Base de Datos | Deployment |
|----------|---------|---------------|------------|
| Bootstrap 5 | Python Flask | SQLite | Render.com |
| Chart.js | Flask-SQLAlchemy |  |  |
| JavaScript | Gunicorn |  |  |
| HTML5/CSS3 | Werkzeug |  |  |

## 📦 Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/upfpdocente-dot/bloqueos-system.git
cd bloqueos-system

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python app.py
