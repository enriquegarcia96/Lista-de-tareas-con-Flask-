#-> hara que interprete esta carpeta de todo como fuese un modulo

import os ##nos permite acceder a ciertas cosas del sistema operativo
from flask import Flask, app

def create_app():
    app = Flask(__name__)

    #me permite definir variables de configuracion
    app.config.from_mapping(
        SECRET_KEY = 'mikey',

        # defino la base de datos para conectarme (valores de variables de entorno)
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE') 
    ) 

    #importo la funcion que cree en db.py
    from . import db    
    db.init_app(app)
    

    @app.route('/hola')
    def hola():
        return 'Hola mundo 2'

    return app 