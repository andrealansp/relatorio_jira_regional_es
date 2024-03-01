import json
import math
import os
from pprint import pprint
from jira import JIRA
from PIL import Image
from io import StringIO

import requests
from requests.auth import HTTPBasicAuth
from config import API_TOKEN, USUARIO, URL


class JiraReporter:
    def __init__(self, jql, url, usuario, senha):
        self.__jql = jql
        self.__url = url
        self.__usuario = usuario
        self.__senha = senha
        self.__lista_de_chamados = {}
        self.__pgs = 0
        self.__chave = None

    def __repr__(self):
        return f"{self.__jql, self.__url, self.__usuario}"

    def paginacao_qtd_paginas(self):
        url = self.__url
        auth = HTTPBasicAuth(self.__usuario, self.__senha)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "jql": self.__jql,
            "maxResults": 100,
            "fieldsByKeys": False,
            "startAt": 0,
        })
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth)
        response_data = json.loads(response.text)
        qt_total_chamados = int(response_data.get('total'))
        qt_total_paginas: int = math.ceil(qt_total_chamados / 100)
        return qt_total_paginas

    def listar_todas_preventivas_perkons(self):
        lista_retorno = []
        dicionario_chamados = {}
        dicionario_anexos = {}
        pgs = self.paginacao_qtd_paginas()
        for x in range(1, pgs + 1):
            index = (x - 1) * 100
            url = self.__url
            auth = HTTPBasicAuth(self.__usuario, self.__senha)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = json.dumps({
                "fields": [
                    "summary",
                    "self",
                    "customfield_10060",
                    "customfield_10116",
                    "customfield_10117",
                    "customfield_10118",
                    "customfield_10141",
                    "customfield_10144",
                    "customfield_10106",
                    "customfield_10107",
                    "customfield_10108",
                    "customfield_10109",
                    "customfield_10110",
                    "customfield_10111",
                    "customfield_10112",
                    "customfield_10113",
                    "customfield_10114",
                    "customfield_10115",
                    "customfield_10139",
                    "attachments"
                ],
                "jql": self.__jql,
                "maxResults": 100,
                "fieldsByKeys": False,
                "startAt": index,
            })
            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers,
                auth=auth)

            self.__lista_de_chamados = json.loads(response.text)
            lista_retorno.append(self.__lista_de_chamados['issues'])

        for x in lista_retorno:
            for y in x:
                dicionario_chamados[y['key']] = y['fields']
                dicionario_anexos[y['key']] = self.listar_anexos_chamado(y['key'])

        return dicionario_chamados, dicionario_anexos

    def listar_preventivas_perkons_paginada(self, pagina):
        lista_retorno = []
        dicionario_chamados = {}
        dicionario_anexos = {}
        index = (pagina - 1) * 100
        url = self.__url
        auth = HTTPBasicAuth(self.__usuario, self.__senha)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "fields": [
                "summary",
                "self",
                "customfield_10060",
                "customfield_10116",
                "customfield_10117",
                "customfield_10118",
                "customfield_10141",
                "customfield_10144",
                "customfield_10106",
                "customfield_10107",
                "customfield_10108",
                "customfield_10109",
                "customfield_10110",
                "customfield_10111",
                "customfield_10112",
                "customfield_10113",
                "customfield_10114",
                "customfield_10115",
                "customfield_10139",
                "attachments"
            ],
            "jql": self.__jql,
            "maxResults": 100,
            "fieldsByKeys": False,
            "startAt": index,
        })
        response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth)

        self.__lista_de_chamados = json.loads(response.text)
        lista_retorno.append(self.__lista_de_chamados['issues'])

        for x in lista_retorno:
            for y in x:
                dicionario_chamados[y['key']] = y['fields']
                dicionario_anexos[y['key']] = self.listar_anexos_chamado(y['key'])

        return dicionario_chamados, dicionario_anexos

    def listar_preventivas_velsis(self):
        lista_retorno = []
        dicionario_chamados = {}
        dicionario_anexos = {}
        pgs = self.paginacao_qtd_paginas()
        for x in range(1, pgs + 1):
            index = (x - 1) * 100
            url = self.__url
            auth = HTTPBasicAuth(self.__usuario, self.__senha)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = json.dumps({
                "fields": [
                    "summary",
                    "customfield_10131",
                    "customfield_10132",
                    "customfield_10133",
                    "customfield_10134",
                    "customfield_10117",
                    "customfield_10118",
                    "customfield_10060",
                    "customfield_10120",
                    "customfield_10119",
                    "customfield_10126",
                    "customfield_10122",
                    "customfield_10125",
                    "customfield_10124",
                    "customfield_10121",
                    "customfield_10135",
                    "customfield_10129",
                    "customfield_10127",
                    "customfield_10130",
                    "customfield_10128",
                    "created",
                    "resolutiondate"
                ],
                "jql": self.__jql,
                "maxResults": 100,
                "fieldsByKeys": False,
                "startAt": index,
            })
            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers,
                auth=auth)

            self.__lista_de_chamados = json.loads(response.text)
            lista_retorno.append(self.__lista_de_chamados['issues'])

        for x in lista_retorno:
            for y in x:
                dicionario_chamados[y['key']] = y['fields']
                dicionario_anexos[y['key']] = self.listar_anexos_chamado(y['key'])

        return dicionario_chamados, dicionario_anexos

    def listar_preventivas_salas(self):
        lista_retorno = []
        dicionario_chamados = {}
        dicionario_anexos = {}
        pgs = self.paginacao_qtd_paginas()
        for x in range(1, pgs + 1):
            index = (x - 1) * 100
            url = self.__url
            auth = HTTPBasicAuth(self.__usuario, self.__senha)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = json.dumps({
                "fields": [
                    "summary",
                    "self",
                    "customfield_10060",
                    "customfield_10116",
                    "customfield_10139",
                    "customfield_10141",
                    "customfield_10144",
                    "customfield_10145",
                    "customfield_10146",
                    "customfield_10147",
                    "customfield_10148",
                    "customfield_10149",
                    "customfield_10150",
                    "customfield_10151",
                    "customfield_10152",
                    "customfield_10153"
                ],
                "jql": self.__jql,
                "maxResults": 100,
                "fieldsByKeys": False,
                "startAt": index,
            })
            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers,
                auth=auth)

            self.__lista_de_chamados = json.loads(response.text)
            lista_retorno.append(self.__lista_de_chamados['issues'])

        for x in lista_retorno:
            for y in x:
                dicionario_chamados[y['key']] = y['fields']
                dicionario_anexos[y['key']] = self.listar_anexos_chamado(y['key'])

        return dicionario_chamados, dicionario_anexos

    @staticmethod
    def imprimir_campos_personalizados(usuario, senha):
        url = "https://servicedeskpedrasverdes.atlassian.net/rest/api/3/field"

        auth = HTTPBasicAuth(usuario, senha)

        headers = {
            "Accept": "application/json"
        }
        response = requests.request(
            "GET",
            url,
            headers=headers,
            auth=auth
        )
        return response.json()

    def listar_anexos_chamado(self, chave):
        url = f"https://servicedeskpedrasverdes.atlassian.net/rest/api/3/issue/{chave}"

        auth = HTTPBasicAuth(self.__usuario, self.__senha)

        headers = {
            "Accept": "application/json"
        }
        payload = {"fields": [
            "key",
            "attachment"
        ]}
        response = requests.request(
            "GET",
            url,
            params=payload,
            headers=headers,
            auth=auth,

        )

        response_anexos = json.loads(response.text)
        lista_anexo = []
        self.__chave = response_anexos['key']

        for anexo in response_anexos.get('fields').get('attachment'):
            lista_anexo.append((anexo['content'], anexo['id']))

        return lista_anexo

    def retorna_json(self):
        lista_retorno = []
        dicionario_chamados = {}
        pgs = self.paginacao_qtd_paginas()
        for x in range(1, pgs + 1):
            index = (x - 1) * 100
            url = self.__url
            auth = HTTPBasicAuth(self.__usuario, self.__senha)
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            payload = json.dumps({
                "jql": self.__jql,
                "maxResults": 100,
                "fieldsByKeys": False,
                "startAt": index,
            })
            response = requests.request(
                "POST",
                url,
                data=payload,
                headers=headers,
                auth=auth)

            self.__lista_de_chamados = json.loads(response.text)
            pprint(self.__lista_de_chamados)
            lista_retorno.append(self.__lista_de_chamados['issues'])

        return lista_retorno

    @staticmethod
    def baixar_anexos(id, chave):
        instancia_jira = JIRA(server="https://servicedeskpedrasverdes.atlassian.net", basic_auth=(USUARIO, API_TOKEN))
        attachment = instancia_jira.attachment(id)  # 12345 is attachment_key
        imagem = attachment.get()
        imgPillow = StringIO.read(imagem)
        return imgPillow


        # diretorio = "static"+os.sep+"relatorios"+os.sep+"imagens"
        # arquivo = f"{diretorio}{os.sep}{chave}-{id}.jpg"
        # if not os.path.exists(arquivo):
        #     with open(arquivo, 'wb') as f:
        #         f.write(image)
        #     return arquivo
        # else:
        #     return arquivo
