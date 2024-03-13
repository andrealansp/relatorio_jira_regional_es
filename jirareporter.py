import json
import logging
import os
import pprint
from typing import cast
from fpdf import FPDF
from datetime import date

import jirapt
import requests
from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
from requests.auth import HTTPBasicAuth
from config import API_TOKEN, USUARIO, BASE_URL, CAMPOS_PCLS, CAMPOS_VELSIS

# logging.basicConfig(level=logging.INFO, filename="acessojira.log", format="%(asctime)s - %(levelname)s - %(message)s")


class JiraReporter:
    def __init__(self,url, usuario, senha, fields=None, jql=None):
        self.__jql = jql
        self.__url = url
        self.__usuario = usuario
        self.__senha = senha
        self.__fields = fields
        self.__jira = JIRA(server=BASE_URL, basic_auth=(self.__usuario, self.__senha))

    def __repr__(self):
        return f"{self.__jql, self.__url, self.__usuario, self.__jql}"

    def search(self, fields):
        issues = cast(ResultList[Issue], jirapt.search_issues(self.__jira, self.__jql, 4, fields=fields))
        return issues

    def getissues(self):
        try:
            issues = self.search(self.__fields)
            dict_chamados = {}
            for issue in issues:
                dict_chamados[issue.key] = issue
            return dict_chamados
        except Exception as e:
            logging.error(f"Erro ai camarada: {e.__str__()}")

    def getfields(self):
        campos = self.__jira.fields()
        pprint.pprint(campos)

    def getattachements(self, chave):
        issue = self.__jira
        attachment = issue.issue(chave, fields="attachment")
        return attachment


if __name__ == "__main__":
    jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type"
                     in ("PREVENTIVA PONTO DE COLETA (CIES)") AND status = Resolved
                     AND resolved >= 2024-02-29 AND resolved <= 2024-03-01  ORDER BY cf[10139]
                     ASC, cf[10116] DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC,
                     timespent DESC, cf[10061] DESC"""

    # jql = f"""created >= 2024-01-02 AND created <= 2024-01-03 AND project = CIES
    #         AND issuetype = "Preventiva Balança" AND status = Resolved AND creator in
    #         (qm:ba8a45d0-c8a8-4107-98fe-bfc59d6bde38:70e33655-0037-42f7-94ef-d8503e158e39)
    #         ORDER BY created ASC, cf[10060] ASC, creator DESC, issuetype ASC, timespent DESC, cf[10061] DESC"""

    jira = JiraReporter(BASE_URL, USUARIO, API_TOKEN, CAMPOS_PCLS, jql)
    chamados = jira.getissues()
    print(chamados)
