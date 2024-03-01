import config
from acessojira import JiraReporter
from escreve_relatorio import PDF


def gerar_relatorio(dtinicial, dtfinal, pagina, relatorio):
    pdf = PDF(unit='cm', orientation='p', format='A4')
    jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type" 
     in ("PREVENTIVA PONTO DE COLETA (CIES)")  AND status = Resolved AND resolved >= {dtinicial} AND 
     resolved <= {dtfinal} ORDER BY cf[10139] ASC, cf[10116] 
     DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC, timespent DESC, cf[10061] DESC"""
    url = config.URL
    usuario = config.USUARIO
    senha = config.API_TOKEN
    acesso = JiraReporter(jql, url, usuario, senha)
    resposta, anexos = acesso.listar_todas_preventivas_perkons()
    local = pdf.escreve_relatorio(resposta, anexos)
    print(local)


if __name__ == "__main__":
    # http://172.23.1.10:8080/gerar_relatorio/2024-02-27/2024-02-28/1/2
    gerar_relatorio("2024-02-01", "2024-03-01", 1, 2)
