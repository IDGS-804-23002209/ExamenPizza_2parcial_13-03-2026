from flask import Blueprint

pizzas=Blueprint(
    'pizzas',
    __name__,
    template_folder='templates',
    static_folder='static')
from . import routes
