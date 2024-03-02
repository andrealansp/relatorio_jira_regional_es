import json
import logging
import os
import pprint
from typing import cast

import jirapt
import requests
from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
from requests.auth import HTTPBasicAuth
from config import API_TOKEN, USUARIO, BASE_URL, CAMPOS_PCLS

logging.basicConfig(level=logging.INFO, filename="acessojira.log", format="%(asctime)s - %(levelname)s - %(message)s")


class JiraReporter:
    def __init__(self, jql, url, usuario, senha, fields):
        self.__jql = jql
        self.__url = url
        self.__usuario = usuario
        self.__senha = senha
        self.__fields = fields
        self.__jira = JIRA(server=BASE_URL, basic_auth=(self.__usuario, self.__senha))

    def __repr__(self):
        return f"{self.__jql, self.__url, self.__usuario}"

    def executa_pequisa(self, fields):
        myself = self.__jira.myself()
        issues = cast(ResultList[Issue], jirapt.search_issues(self.__jira, self.__jql, 4, fields=fields))
        return issues

    def getissues(self):
        try:
            issues = self.executa_pequisa(self.__fields)
            dict_chamados = {}
            dict_anexos = {}
            for issue in issues:
                dict_chamados[issue.key] = issue.fields
                dict_anexos[issue.key] = issue.fields.attachment
            return dict_chamados, dict_anexos
        except Exception as e:
            logging.error(f"Erro ai camarada: {e.__str__()}")

    def getfields(self):
        campos = self.__jira.fields()
        pprint.pprint(campos)

if __name__ == "__main__":
    jql = f"""assignee in (currentUser()) AND project = CIES AND issuetype = "Preventiva PCL" AND "Request Type"
                     in ("PREVENTIVA PONTO DE COLETA (CIES)") AND status = Resolved 
                     AND resolved >= 2024-02-29 AND resolved <= 2024-03-01  ORDER BY cf[10139] 
                     ASC, cf[10116] DESC, created ASC, cf[10060] ASC, creator DESC, issuetype ASC, 
                     timespent DESC, cf[10061] DESC"""
    jira = JiraReporter(jql, BASE_URL, USUARIO, API_TOKEN,CAMPOS_PCLS)
    chamados = jira.getissues()
    for chave, valor in chamados[1].items():
        print(chave)
        pprint.pprint(valor[0].self)