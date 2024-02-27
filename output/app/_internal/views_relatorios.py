from flask import render_template
from escreve_relatorio import PDF

from acessojira import JiraReporter
from app import app
from helpers import FormularioRelatorio


@app.get('/gerar_relatorio/<dtinicial>/<dtfinal>/<int:pagina>/<int:relatorio>')
def gerar_relatorio(dtinicial, dtfinal, pagina, relatorio):
    pdf = PDF(unit='cm', orientation='p', format='A4')
    jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type"                         in ("PREVENTIVA PONTO DE COLETA (CIES)") AND status = Resolved 
                         AND resolved >= {dtinicial} AND resolved <= {dtfinal} ORDER BY cf[10139] ASC, cf[10116] 
                         DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC, timespent DESC, cf[10061] DESC"""
    url = app.config['URL']
    usuario = app.config['USUARIO']
    senha = app.config['API_TOKEN']
    acesso = JiraReporter(jql, url, usuario, senha)
    resposta, anexos = acesso.listar_todas_preventivas_perkons()
    local = pdf.escreve_relatorio(resposta, anexos)
    print(local)
    formulario_pcl = FormularioRelatorio()
    return render_template('perkons.html', form=formulario_pcl,
                           titulo="Preventivas - PCL")
