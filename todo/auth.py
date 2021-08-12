import functools #funciones 

from flask import (
    Blueprint, flash, #envia mensajes genericos a las plantillas
    g, render_template, request, url_for, session, redirect
)

#-> verificar si la contraseña es la correcta y (generate) incripta la contraseña
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from todo import db 

from todo.db import get_db

#-> importo la libreria de Blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        #saco la variable de username del formulario
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'select id from user where username = %s', (username,)
        )

        #-> asigno los mensajes de error a la variable 'error' tipo flash
        if not username:
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)

        #-> si no tiene nada el error, que me ejecute la consulta
        if error is None:
            c.execute(
                'insert into user (username, password) values (%s, %s)',
                (username, generate_password_hash(password))#encripto la contraseña
            )
            db.commit()

            return redirect(url_for('auth.login'))#-> redirijo al usuario a esta plantilla 

        #-> mando el mensaje de error al cliente
        flash(error)


    return render_template('auth/register.html')#-> solo se renderiza si el usuario manda una peticion de tipo 'GET'


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválida'

        if error is None:
            session.clear()
            session['user_id'] = user['id'] #le asigno el id del usuario de la base de datos 
            return redirect(url_for('todo.index'))

        flash(error)
    return render_template('auth/login.html')





#-> coloca el usuario dentro de la variable 'g'
@bp.before_app_request
def load_logged_in_user(): #-> se encarga de cargar el usuario
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()#-> devuelve el primer elemento que encuentre en la base de datos 



#-> funcion que protege las rutas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:#pregunta si existe el usuario dentro de la variable global
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))











