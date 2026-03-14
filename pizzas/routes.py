from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .forms import PizzaForm
from models import db, Cliente, Pedido, DetallePedido, Pizza
from datetime import datetime, date

pizzas_bp = Blueprint('pizzas', __name__)

@pizzas_bp.route('/pedido', methods=['GET', 'POST'])
def registro_pedido():
    form = PizzaForm()
    if 'carrito' not in session:
        session['carrito'] = []

    if request.method == 'POST':
        # --- BOTÓN AGREGAR ---
        if "btn_agregar" in request.form:
            if form.validate_on_submit():
                # Guardamos datos del cliente incluyendo la FECHA en la sesión
                session['cliente_temp'] = {
                    'nombre': form.nombre.data,
                    'direccion': form.direccion.data,
                    'telefono': form.telefono.data,
                    'fecha': form.fecha_pedido.data.strftime('%Y-%m-%d') # Guardar como texto
                }

                precios = {'Chica': 40, 'Mediana': 80, 'Grande': 120}
                precio_base = precios.get(form.tamano.data, 0)
                costo_ing = len(form.ingredientes.data) * 10
                subtotal = (precio_base + costo_ing) * form.num_pizzas.data

                nueva_pizza_temp = {
                    'tamano': form.tamano.data,
                    'ingredientes': ", ".join(form.ingredientes.data),
                    'cantidad': form.num_pizzas.data,
                    'subtotal': subtotal
                }
                
                carrito = session['carrito']
                carrito.append(nueva_pizza_temp)
                session['carrito'] = carrito
                return redirect(url_for('pizzas.registro_pedido'))
            else:
                flash("Por favor, llena los datos de la pizza correctamente.")

        # --- BOTÓN TERMINAR ---
        elif "btn_terminar" in request.form:
            nombre_cli = request.form.get('nombre')
            fecha_sel = request.form.get('fecha_pedido') # Obtenemos fecha del input
            carrito = session.get('carrito', [])

            if not nombre_cli or not carrito:
                flash("Faltan datos o el carrito está vacío.")
                return redirect(url_for('pizzas.registro_pedido'))

            try:
                cli = Cliente(
                    nombre=nombre_cli, 
                    direccion=request.form.get('direccion'), 
                    telefono=request.form.get('telefono')
                )
                db.session.add(cli)
                db.session.flush() 

                # CREAMOS EL PEDIDO CON LA FECHA DEL CALENDARIO
                ped = Pedido(
                    id_cliente=cli.id_cliente, 
                    fecha=datetime.strptime(fecha_sel, '%Y-%m-%d'), 
                    total=sum(p['subtotal'] for p in carrito)
                )
                db.session.add(ped)
                db.session.flush() 

                for p in carrito:
                    nueva_piz_db = Pizza(
                        tamano=p['tamano'],
                        ingredientes=p['ingredientes'],
                        precio=p['subtotal'] / p['cantidad']
                    )
                    db.session.add(nueva_piz_db)
                    db.session.flush() 

                    det = DetallePedido(
                        id_pedido=ped.id_pedido, 
                        id_pizza=nueva_piz_db.id_pizza,
                        cantidad=p['cantidad'], 
                        subtotal=p['subtotal']
                    )
                    db.session.add(det)

                db.session.commit()
                session.pop('carrito', None)
                session.pop('cliente_temp', None)
                flash(f"Venta registrada para el día {fecha_sel}")
                
            except Exception as e:
                db.session.rollback()
                flash(f"Error: {str(e)}")
            
            return redirect(url_for('pizzas.registro_pedido'))

    # --- PERSISTENCIA (GET) ---
    if 'cliente_temp' in session:
        form.nombre.data = session['cliente_temp'].get('nombre')
        form.direccion.data = session['cliente_temp'].get('direccion')
        form.telefono.data = session['cliente_temp'].get('telefono')
        # Recuperamos la fecha guardada
        form.fecha_pedido.data = date.fromisoformat(session['cliente_temp'].get('fecha'))

    # Ventas del día actual
    hoy = date.today()
    ventas_hoy = db.session.query(Cliente.nombre, Pedido.total)\
        .join(Pedido, Cliente.id_cliente == Pedido.id_cliente)\
        .filter(db.func.date(Pedido.fecha) == hoy).all()
    
    return render_template('pizzas/index.html', 
                           form=form, 
                           carrito=session.get('carrito', []), 
                           ventas_dia=ventas_hoy, 
                           total_dia=sum(v.total for v in ventas_hoy))

@pizzas_bp.route('/quitar/<int:index>')
def quitar_pizza(index):
    carrito = session.get('carrito', [])
    if 0 <= index < len(carrito):
        carrito.pop(index)
        session['carrito'] = carrito
        flash("Pizza eliminada de la lista.")
    return redirect(url_for('pizzas.registro_pedido'))