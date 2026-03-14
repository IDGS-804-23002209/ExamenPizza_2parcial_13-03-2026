from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    # Relación para acceder a pedidos desde el cliente
    pedidos = db.relationship('Pedido', backref='cliente', lazy=True)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'))
    fecha = db.Column(db.Date, default=datetime.utcnow)
    total = db.Column(db.Numeric(10, 2))
    # Relación para acceder a los detalles del pedido
    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id_pizza = db.Column(db.Integer, primary_key=True)
    tamano = db.Column(db.String(20), nullable=False)
    ingredientes = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)

class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'))
    id_pizza = db.Column(db.Integer, db.ForeignKey('pizzas.id_pizza')) # Esta FK es vital
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Numeric(10, 2))
    
    # ESTA LÍNEA ES LA QUE HACE QUE TU HTML FUNCIONE:
    pizza = db.relationship('Pizza', backref='detalles')