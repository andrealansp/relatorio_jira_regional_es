from flask import render_template, request, redirect, session, flash, url_for

from acessojira import JiraReporter
from app import app
from helpers import FormularioRelatorio, FormularioSalas, FormularioPerkonsPaineis


@app.route("/perkons", methods=['GET'])
def perkons():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    formulario_pcl = FormularioRelatorio()
    return render_template('perkons.html', form=formulario_pcl,
                           titulo="Preventivas - PCL")


@app.route("/perkons_paineis", methods=['GET'])
def perkons_paineis():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    formulario_paineis = FormularioPerkonsPaineis()
    return render_template('perkons_paineis.html', form=formulario_paineis,
                           titulo="Preventivas - PCL")


@app.route("/salas", methods=['GET', ])
def salas():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    formulario = FormularioRelatorio()
    return render_template('salas.html', form=formulario, titulo="Preventivas - Salas")


@app.route("/preventivas_perkons", methods=['GET', 'POST', ])
def preventivas_perkons():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    form = FormularioRelatorio(request.form)

    if not form.validate_on_submit():
        flash('Formulário não é válido!')
        return redirect(url_for('perkons'))

    jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type"
                 in ("PREVENTIVA PONTO DE COLETA (CIES)") AND status = Resolved 
                 AND resolved >= {form.data_inicial.data} AND resolved <= {form.data_final.data} ORDER BY cf[10139] 
                 ASC, cf[10116] DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC, 
                 timespent DESC, cf[10061] DESC"""
    url = app.config['URL']
    usuario = app.config['USUARIO']
    senha = app.config['API_TOKEN']
    acesso = JiraReporter(jql, url, usuario, senha)

    # Relatório em partes

    if form.tipo_relatorio.data == "Em Partes":
        try:
            qtd_paginas = acesso.paginacao_qtd_paginas()
            indices = [indice for indice in range(1, qtd_paginas + 1)]
            dados = {"dtinicial": form.data_inicial.data, "dtfinal": form.data_final.data, "indices": indices}
            return render_template("perkons.html", form=form, titulo="Preventivas - PCL", dados=dados)
        except Exception as e:
            print('oi')
            flash(e.__str__(), "alert-danger")
            return render_template('perkons.html', form=form, titulo="Preventivas - PCL")
    try:
        resposta, anexos = acesso.listar_todas_preventivas_perkons()
        return render_template('relatorio_perkons.html', resposta=resposta, anexos=anexos,
                               titulo="Relatório - PCL")
    except Exception as e:
        flash(e.__str__(), "alert-danger")
        return render_template('perkons.html', form=form, titulo="Preventivas - PCL")


@app.route("/preventivas_perkons_paineis", methods=['GET', 'POST', ])
def preventivas_perkons_paineis():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    form = FormularioPerkonsPaineis(request.form)
    if not form.validate_on_submit():
        flash('Formulário não é válido!')
        return redirect(url_for('perkons_paineis'))
    jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type"
                 in ("PREVENTIVA PONTO DE COLETA (CIES)") AND status = Resolved 
                 AND resolved >= {form.data_inicial.data} AND resolved <= {form.data_final.data} AND 
                 "Equipamentos[Select List (cascading)]" in (
                 P0091-PCL-PK-VIA,P0114-PCL-PK-SER,P0163-PK-VLS-MIM,P0165-PK-VLS-BAR,P0167-PK-VLS-DOR,
                 P0169-PK-VLS-BOM,P0170-PK-VLS-MIM,P0171-PK-VLS-PRE,P0174-PK-VLS-LIN,P0175-PK-VLS-LIN,
                 P0181-PK-VLS-RNS,P0190-PK-VLS-MUC,P0191-PK-VLS-ADN,P0192-PK-VLS-MON,P0193-PK-VLS-ADN,
                 P0196-PK-VLS-PED,P0197-PK-VLS-FUN,P0200-PK-VLS-LIN,P0201-PK-VLS-ITP,P0202-PK-VLS-MIM,
                 P0203-PK-VLS-ECO,P0212-PK-VLS-COL,P0213-PK-VLS-ABR,P0214-PK-VLS-BAR,P0215-PK-VLS-NOV,
                 P0216-PK-VLS-NOV,P0218-PK-VLS-AFO,P0221-PK-VLS-RBA,P0224-PK-VLS-SMA,P0230-PK-VLS-MON,
                 P0231-PK-VLS-MAN,P0233-PK-VLS-LIN,P0234-PK-VLS-PED,P0235-PK-VLS-SMA,P0239-PK-VLS-ATI)
                 ORDER BY cf[10139] 
                 ASC, cf[10116] DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC, 
                 timespent DESC, cf[10061] DESC"""
    url = app.config['URL']
    usuario = app.config['USUARIO']
    senha = app.config['API_TOKEN']
    acesso = JiraReporter(jql, url, usuario, senha)
    try:
        resposta, anexos = acesso.listar_todas_preventivas_perkons()
        return render_template('relatorio_perkons.html', resposta=resposta, anexos=anexos,
                               titulo="Relatório - PCL")
    except Exception as e:
        flash(e.__str__(), "alert-danger")
        return render_template('perkons_paineis.html', form=form, titulo="Preventivas - PCL")


@app.route("/preventivas_perkons_paginado/<dtinicial>/<dtfinal>/<int:pagina>", methods=['GET', 'POST', ])
def preventivas_perkons_paginado(dtinicial, dtfinal, pagina):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type"
                     in ("PREVENTIVA PONTO DE COLETA (CIES)") AND status = Resolved 
                     AND resolved >= {dtinicial} AND resolved <= {dtfinal} ORDER BY cf[10139] ASC, cf[10116] 
                     DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC, timespent DESC, cf[10061] DESC"""
    url = app.config['URL']
    usuario = app.config['USUARIO']
    senha = app.config['API_TOKEN']
    acesso = JiraReporter(jql, url, usuario, senha)
    try:
        resposta, anexos = acesso.listar_preventivas_perkons_paginada(pagina)
        return render_template('relatorio_perkons.html', resposta=resposta, anexos=anexos,
                               titulo="Relatório - PCL")
    except Exception as e:
        flash(e.__str__(), "alert-danger")
        form = FormularioRelatorio()
        return render_template('perkons.html', form=form, titulo="Preventivas - PCL")


@app.route("/preventivasalas", methods=['POST', ])
def preventivasalas():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))

    form = FormularioSalas(request.form)

    if not form.validate_on_submit():
        flash('Formulário não é válido!', "alert-dangers")
        return redirect(url_for('salas'))

    try:
        jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva Salas"  AND "Request Type"
         in ("PREVENTIVAS SALA DE CONTROLE E OPERAÇÃO E PRODEST (CIES)") AND status = Resolved AND resolved >= 
         {form.data_inicial.data} AND resolved <= {form.data_final.data} ORDER BY cf[10139] ASC, cf[10116] DESC, 
         created ASC, cf[10060] ASC, creator DESC, issuetype ASC, timespent DESC, cf[10061] DESC"""
        url = app.config['URL']
        usuario = app.config['USUARIO']
        senha = app.config['API_TOKEN']
        acesso = JiraReporter(jql, url, usuario, senha)
        resposta, anexos = acesso.listar_preventivas_salas()
        return render_template('relatorio_salas.html', resposta=resposta, anexos=anexos,
                               titulo="Relatório - Salas")
    except Exception as e:
        flash(e.__str__(), "alert-danger")


@app.route("/raw", methods=['GET', ])
def raw():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type"
                     in ("PREVENTIVA PONTO DE COLETA (CIES)") AND status = Resolved 
                     AND resolved >= 2024-01-01 AND resolved <= 2024-01-31 ORDER BY cf[10139] ASC, cf[10116] 
                     DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC, timespent DESC, cf[10061] DESC"""
    url = app.config['URL']
    usuario = app.config['USUARIO']
    senha = app.config['API_TOKEN']
    acesso = JiraReporter(jql, url, usuario, senha)
    resposta = acesso.retorna_json()
    return resposta


@app.route("/custonfields", methods=['POST', 'GET'])
def custonfields():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login'))
    usuario = app.config['USUARIO']
    senha = app.config['API_TOKEN']
    acesso = JiraReporter.imprimir_campos_personalizados(usuario, senha)
    return acesso
