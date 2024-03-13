from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, DateField, SelectField


class FormularioUsuario(FlaskForm):
    usuario = StringField('Usuario', [validators.data_required(), validators.Length(min=1, max=12)])
    senha = PasswordField('Senha', [validators.data_required(), validators.Length(min=1, max=100)])
    login = SubmitField('LOGAR')


class FormularioRelatorio(FlaskForm):
    data_inicial = DateField('Data Inicial', [validators.data_required()])
    data_final = DateField('Data Final', [validators.data_required()], format="%Y-%m-%d")
    visualizar = SubmitField('Visualizar')


class FormularioGerarPDF(FlaskForm):
    data_inicial = DateField('Data Inicial', [validators.data_required()])
    data_final = DateField('Data Final', [validators.data_required()], format="%Y-%m-%d")
    tipo_relatorio = SelectField('Tipo de Relatório', choices=[("pcl", "Pontos de Coleta"),
                                                               ("balanca", "Pontos Com Balança"),
                                                               ("salas", "Salas de Controle e Operação")])
    emitir = SubmitField('Emitir')


class FormularioPerkonsPaineis(FlaskForm):
    data_inicial = DateField('Data Inicial', [validators.data_required()])
    data_final = DateField('Data Final', [validators.data_required()], format="%Y-%m-%d")
    visualizar = SubmitField('Visualizar')


class FormularioSalas(FlaskForm):
    data_inicial = DateField('Data Inicial', [validators.data_required()])
    data_final = DateField('Data Final', [validators.data_required()], format="%Y-%m-%d")
    visualizar = SubmitField('Visualizar')


class FormularioVelsis(FlaskForm):
    data_inicial = DateField('Data Inicial', [validators.data_required()])
    data_final = DateField('Data Final', [validators.data_required()], format="%Y-%m-%d")
    visualizar = SubmitField('Visualizar')