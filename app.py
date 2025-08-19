from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# Configuración de la aplicación
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Configuración de la base de datos
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'bloqueos.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'una-clave-secreta-muy-segura'

db = SQLAlchemy(app)

# Modelos de la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bloqueos = db.relationship('Bloqueo', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Bloqueo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    departamento = db.Column(db.String(100), nullable=False)
    placa = db.Column(db.String(20), nullable=False)
    barcode = db.Column(db.String(50), nullable=False)
    pin = db.Column(db.String(10), nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Bloqueo {self.placa}>'

# Crear la base de datos y usuario admin
with app.app_context():
    db.create_all()
    
    # Crear usuario administrador por defecto si no existe
    if not User.query.filter_by(username='admin').first():
        admin_user = User(
            username='admin',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Usuario administrador creado: admin / admin123")

    # Después de crear el usuario admin, agrega:
    if not User.query.filter_by(username='usuario1').first():
        usuario1 = User(
            username='usuario1',
            password=generate_password_hash('password123'),
            is_admin=False
        )
        db.session.add(usuario1)
        db.session.commit()
        print("Usuario normal creado: usuario1 / password123")

if not User.query.filter_by(username='operador').first():
    operador = User(
        username='operador',
        password=generate_password_hash('operador123'),
        is_admin=False
    )
    db.session.add(operador)
    db.session.commit()
    print("Usuario normal creado: operador / operador123")

# Rutas de la aplicación
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('is_admin'):
        return redirect(url_for('admin'))
    return redirect(url_for('registro'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
            departamento = request.form['departamento']
            placa = request.form['placa']
            barcode = request.form['barcode']
            pin = request.form['pin']
            motivo = request.form['motivo']
            
            nuevo_bloqueo = Bloqueo(
                fecha=fecha,
                departamento=departamento,
                placa=placa,
                barcode=barcode,
                pin=pin,
                motivo=motivo,
                user_id=session['user_id']
            )
            
            db.session.add(nuevo_bloqueo)
            db.session.commit()
            
            flash('Registro de bloqueo guardado exitosamente', 'success')
            return redirect(url_for('registro'))
        except Exception as e:
            flash(f'Error al guardar el registro: {str(e)}', 'danger')
    
    return render_template('registro.html')

@app.route('/admin')
def admin():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    bloqueos = Bloqueo.query.all()
    return render_template('admin.html', bloqueos=bloqueos)

@app.route('/admin/graficos')
def graficos():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    # Datos para gráficos
    departamentos_data = db.session.query(
        Bloqueo.departamento,
        db.func.count(Bloqueo.id)
    ).group_by(Bloqueo.departamento).all()
    
    fechas_data = db.session.query(
        db.func.date(Bloqueo.fecha),
        db.func.count(Bloqueo.id)
    ).group_by(db.func.date(Bloqueo.fecha)).all()
    
    placas_data = db.session.query(
        Bloqueo.placa,
        db.func.count(Bloqueo.id)
    ).group_by(Bloqueo.placa).order_by(db.func.count(Bloqueo.id).desc()).limit(10).all()
    
    # Convertir a formatos simples para JSON
    departamentos = [[dept, count] for dept, count in departamentos_data]
    fechas = [[fecha.strftime('%Y-%m-%d') if hasattr(fecha, 'strftime') else str(fecha), count] for fecha, count in fechas_data]
    placas = [[placa, count] for placa, count in placas_data]
    
    return render_template('graficos.html',
                         departamentos=departamentos,
                         fechas=fechas,
                         placas=placas)

if __name__ == '__main__':
    # Forzar configuración específica
    app.run(
        debug=True, 
        host='127.0.0.1', 
        port=5000, 
        threaded=True,
        use_reloader=False  # Desactivar reloader que a veces causa problemas
    )