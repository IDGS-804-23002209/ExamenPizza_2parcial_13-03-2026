from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from models import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pizzaria_secret_key_123'
# Cambia 'usuario:password' por tus credenciales de MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/examePizzas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)
db.init_app(app)

# Registro de Blueprints según tu estructura de carpetas
from pizzas.routes import pizzas_bp
from ventas.routes import ventas_bp

app.register_blueprint(pizzas_bp, url_prefix='/pizzas')
app.register_blueprint(ventas_bp, url_prefix='/ventas')

@app.route('/')
def index():
    return render_template('layout.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Crea las tablas automáticamente
    app.run(debug=True, port=5000)