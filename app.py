from datetime import datetime
from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from acessojira import JiraReporter
from waitress import serve
import logging

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
db:SQLAlchemy
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


def datetime_format(value, format="%d/%m/%y"):
    ano = value[0:4]
    mes = value[5:7]
    dia = value[8:10]
    hora = value[11:13]
    minuto = value[14:16]
    if len(value) > 10:
        return f"{dia}/{mes}/{ano}-{hora}:{minuto}h"
    else:
        return f"{dia}/{mes}/{ano}"

app.jinja_env.filters['datetime_format'] = datetime_format

@app.route("/")
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    return render_template('preventivas.html')

from views_perkons import *
from views_usuarios import *
from views_velsis import *
from views_relatorios import *



if __name__ == '__main__':
    app.run(debug=True)
