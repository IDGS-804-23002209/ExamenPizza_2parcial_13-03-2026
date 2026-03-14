from flask import Blueprint, render_template, request
from models import db, Pedido, Cliente, DetallePedido
from sqlalchemy import extract

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/reporte', methods=['GET', 'POST'])
def reporte_ventas():
    resultados = []
    gran_total = 0
    
    if request.method == 'POST':
        # Limpiamos los inputs (minúsculas y sin espacios)
        filtro_dia = request.form.get('dia_nombre', '').lower().strip()
        filtro_mes = request.form.get('mes_nombre', '').lower().strip()

        query = db.session.query(Pedido, Cliente).join(Cliente)

        # Diccionario de Días (Python usa 0 para Lunes)
        dias = {
            'lunes': 0, 'martes': 1, 'miercoles': 2, 'jueves': 3, 
            'viernes': 4, 'sabado': 5, 'domingo': 6
        }

        # Diccionario de Meses (SQL usa 1 para Enero)
        meses = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
            'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }

        # LÓGICA DE FILTRADO
        if filtro_dia in dias:
            num_dia = dias[filtro_dia]
            todas = query.all()
            resultados = [r for r in todas if r.Pedido.fecha.weekday() == num_dia]

        elif filtro_mes in meses:
            num_mes = meses[filtro_mes]
            # Filtra directamente en la BD por el número del mes extraído de la fecha
            resultados = query.filter(extract('month', Pedido.fecha) == num_mes).all()
        
        else:
            # Si no hay filtros válidos, muestra todo
            resultados = query.all()

        gran_total = sum(r.Pedido.total for r in resultados)

    return render_template('ventas/reporte.html', ventas=resultados, total=gran_total)

@ventas_bp.route('/detalle/<int:id_pedido>')
def detalle_venta(id_pedido):
    detalles = DetallePedido.query.filter_by(id_pedido=id_pedido).all()
    return render_template('ventas/detalle.html', detalles=detalles, id_pedido=id_pedido)