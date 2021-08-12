import mysql.connector
import click
from flask import current_app, g
from flask.cli import with_appcontext # ayuda a ejecutar el script de la base de datos 
from .schema import instructions


#obtiene la base de daos y el cursor
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            password=current_app.config['DATABASE_PASSWORD'],
            user=current_app.config['DATABASE_USER'],
            database=current_app.config['DATABASE']
        )
        #creo una nueva propiedad a g
        #acedo al cursor para ejecutar las consultas de SQL
        g.c = g.db.cursor(dictionary=True)  
    return g.db, g.c



#permite cerrar la conexion de la base de datos cada vez que haga una peticion
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    #traigo la base de datos 
    db, c = get_db()

    for i in instructions:
        c.execute(i)
    db.commit()


@click.command('init-db')#ejecuta e script para conectar ala base de datos
@with_appcontext #acede alas variables de la base de datos
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')


#cuando termina de realizar una peticion a la base de datos
def init_app(app):

    #cuando termine que darnos la peticio  de la base de datos 
    # lo que hara es cerrar la conexion de la base de datos 
    app.teardown_appcontext(close_db) 

    #subcribo el comando de (init_db_command)
    app.cli.add_command(init_db_command)

