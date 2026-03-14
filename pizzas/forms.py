from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectMultipleField, IntegerField, widgets, DateField
from wtforms.validators import DataRequired
from datetime import date

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PizzaForm(FlaskForm):
    # Datos del Cliente y Fecha
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    fecha_pedido = DateField('Fecha de Venta', default=date.today, validators=[DataRequired()])
    
    # Datos de la Pizza
    tamano = RadioField('Tamaño Pizza', choices=[
        ('Chica', 'Chica $40'), 
        ('Mediana', 'Mediana $80'), 
        ('Grande', 'Grande $120')
    ], validators=[DataRequired()])
    
    ingredientes = MultiCheckboxField('Ingredientes', choices=[
        ('Jamon', 'Jamón $10'), 
        ('Piña', 'Piña $10'), 
        ('Champiñones', 'Champiñones $10')
    ])
    
    num_pizzas = IntegerField('Número de Pizzas', validators=[DataRequired()], default=1)