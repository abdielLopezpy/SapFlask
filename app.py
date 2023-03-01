from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect

from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

# Configuración de la bd
'''
Los espacios USER_DB, PASS_DB y URL_DB corresponden a la información de conexión de la base de datos.
Debes reemplazar cada uno de estos espacios por los valores correspondientes de tu propia base de datos.

USER_DB: Debe contener el nombre de usuario de tu base de datos.
PASS_DB: Debe contener la contraseña de tu base de datos.
URL_DB: Debe contener la URL o dirección IP de tu base de datos. Por ejemplo: 'localhost' o '127.0.0.1'.
NAME_DB: Debe contener el nombre de la base de datos que deseas utilizar.
Recuerda que debes asegurarte de que la base de datos exista y que el usuario especificado tenga permisos para acceder 
a ella.
'''
USER_DB = ''
PASS_DB = ''
URL_DB = ''
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializacion del objeto db de sqlalchemy
db.init_app(app)

# configurar flask-migrate
migrate = Migrate()
migrate.init_app(app, db)

# configuracion de flask-wtf
app.config['SECRET_KEY'] = 'llave_secreta'

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def inicio():
    """
    Renderiza la plantilla index.html con el listado de personas y el total de personas.
    """
    # Listado de personas
    personas = Persona.query.order_by('id')
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas: {personas}')
    app.logger.debug(f'Total Personas: {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)


@app.route('/ver/<int:id>')
def ver_detalle(id):
    """
    Renderiza la plantilla detalle.html con los detalles de la persona que tenga el id proporcionado.
    """
    # Recuperamos la persona según el id proporcionado
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona=persona)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    """
    Renderiza la plantilla agregar.html para agregar una nueva persona o procesa el formulario y agrega la persona a la base de datos.
    """
    persona = Persona()
    personaForm = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f'Persona a insertar: {persona}')
            # Insertamos el nuevo registro
            db.session.add(persona)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma=personaForm)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """
    Renderiza la plantilla editar.html para editar una persona o procesa el formulario y actualiza la persona en la base de datos.
    """
    # Recuperamos el objeto persona a editar
    persona = Persona.query.get_or_404(id)
    personaForma = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForma.validate_on_submit():
            personaForma.populate_obj(persona)
            app.logger.debug(f'Persona a actualizar: {persona}')
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar.html', forma=personaForma)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    """
    Elimina la persona que tenga el id proporcionado de la base de datos.
    """
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Persona a eliminar: {persona}')
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('inicio'))
