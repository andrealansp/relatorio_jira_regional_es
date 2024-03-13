import logging
import traceback

from flask import render_template, request, redirect, session, flash, url_for

from jirareporter import JiraReporter
from app import app
from helpers import FormularioVelsis

@app.route("/velsis", methods=['GET', ])
def velsis():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    formulario = FormularioVelsis()
    return render_template('velsis.html', form=formulario, titulo="Preventivas - Balanças")


@app.route("/preventivas_velsis", methods=['POST', ])
def preventivasvelsis():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    form = FormularioVelsis(request.form)
    if not form.validate_on_submit():
        flash('Formulário não é válido!')
        return redirect(url_for('perkons'))
    try:
        jql = f"""created >= {form.data_inicial.data} AND created <= {form.data_final.data} AND project = CIES 
            AND issuetype = "Preventiva Balança" AND status = Resolved AND creator in
            (qm:ba8a45d0-c8a8-4107-98fe-bfc59d6bde38:70e33655-0037-42f7-94ef-d8503e158e39) 
            ORDER BY created ASC, cf[10060] ASC, creator DESC, issuetype ASC, timespent DESC, cf[10061] DESC"""

        acesso = JiraReporter(
            app.config["URL"],
            app.config["USUARIO"],
            app.config["API_TOKEN"],
            app.config["CAMPOS_VELSIS"],
            jql,
        )
        chamados = acesso.getissues()
        return render_template(
            "relatorio_velsis.html", resposta=chamados, titulo="Relatório - Balanças"
        )
    except Exception as e:
        logging.error(f"Erro ai camarada: {e.__str__()} / {traceback.format_exc()}")
        flash(e.__str__(), "alert-danger")
        return render_template('velsis.html', form=form, titulo="Preventivas - Balanças")
