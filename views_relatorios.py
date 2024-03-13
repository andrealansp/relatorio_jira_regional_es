import logging
import time
import traceback

from flask import (
    render_template,
    request,
    redirect,
    send_file,
    session,
    flash,
    url_for,
)
from jirareporter import JiraReporter
from app import app
from escreve_relatorio_pcls import PdfPcls
from escreve_relatorio_salas import PdfSalas
from escreve_relatorio_velsis import PdfVelsis
from helpers import FormularioGerarPDF


@app.route(
    "/emitir_relatorio",
    methods=[
        "GET",
    ],
)
def emitir_relatorio():
    if "usuario_logado" not in session or session["usuario_logado"] is None:
        return redirect(url_for("login"))
    form = FormularioGerarPDF()
    return render_template(
        "emitir_relatorios.html", form=form, titulo="Gerar Relatórios"
    )


@app.route(
    "/gerar_relatorio",
    methods=[
        "POST",
    ],
)
def gerar_relatorio():
    pdf_pcls = PdfPcls(unit="cm", orientation="p", format="A4")
    pdf_salas = PdfSalas(unit="cm", orientation="p", format="A4")
    pdf_velsis = PdfVelsis(unit="cm", orientation="p", format="A4")
    form = FormularioGerarPDF(request.form)
    match form.tipo_relatorio.data:
        case "pcl":
            try:
                jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type"
                 in ("PREVENTIVA PONTO DE COLETA (CIES)") AND status = Resolved 
                 AND resolved >= {form.data_inicial.data} AND resolved <= {form.data_final.data} ORDER BY cf[10139] 
                 ASC, cf[10116] DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC, 
                 timespent DESC, cf[10061] DESC"""
                acesso = JiraReporter(
                    app.config["URL"],
                    app.config["USUARIO"],
                    app.config["API_TOKEN"],
                    app.config["CAMPOS_PCLS"],
                    jql,
                )
                chamados = acesso.getissues()
                local = pdf_pcls.escreve_relatorio(chamados)
                time.sleep(10)
                return send_file(local, as_attachment=True)
            except Exception as e:
                flash(
                    f"{e.__str__()} - Trecho do código: {traceback.format_exc()}",
                    "alert-danger",
                )
                return render_template(
                    "emitir_relatorios.html", form=form, titulo="Gerar Relatórios"
                )

        case "balanca":
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
                local = pdf_velsis.escreve_relatorio(chamados)
                return send_file(local, as_attachment=True)
            except Exception as e:
                flash(
                    f"{e.__str__()} - Trecho do código: {traceback.format_exc()}",
                    "alert-danger",
                )
                return render_template(
                    "emitir_relatorios.html", form=form, titulo="Gerar Relatórios"
                )

        case "salas":
            try:
                jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva Salas"  AND "Request Type"
                         in ("PREVENTIVAS SALA DE CONTROLE E OPERAÇÃO E PRODEST (CIES)") AND status = Resolved AND resolved >= 
                         {form.data_inicial.data} AND resolved <= {form.data_final.data} ORDER BY cf[10139] ASC, cf[10116] DESC, 
                         created ASC, cf[10060] ASC, creator DESC, issuetype ASC, timespent DESC, cf[10061] DESC"""

                acesso = JiraReporter(
                    app.config["URL"],
                    app.config["USUARIO"],
                    app.config["API_TOKEN"],
                    app.config["CAMPOS_SALAS"],
                    jql,
                )

                chamados = acesso.getissues()
                local = pdf_salas.escreve_relatorio(chamados)
                return send_file(local, as_attachment=True)
            except Exception as e:
                flash(
                    f"{e.__str__()} - Trecho do código: {traceback.format_exc()}",
                    "alert-danger",
                )
                return render_template(
                    "emitir_relatorios.html", form=form, titulo="Gerar Relatórios"
                )
