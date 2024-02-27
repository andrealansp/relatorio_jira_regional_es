from app import app
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    if proxima:
        form = FormularioUsuario()
        return render_template('login.html', proxima=proxima, form=form)
    else:
        form = FormularioUsuario()
        return render_template('login.html', form=form)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    print(form.senha.data)
    usuario = Usuarios.query.filter_by(usuario=form.usuario.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.usuario
        flash(usuario.usuario + ' Logado com sucesso',"alert-success")
        if request.form['proxima']:
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            return redirect(url_for('index'))
    else:
        flash('Erro na senha!', category='error')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash("Logout efetuado com sucesso","alert-danger")
    return redirect(url_for('index'))
