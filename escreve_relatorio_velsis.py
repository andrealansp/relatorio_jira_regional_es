import os
from datetime import date

from dateutil.relativedelta import relativedelta
from fpdf import FPDF

from jirareporter import JiraReporter
from app import app


class PdfVelsis(FPDF):

    def header(self):
        self.image("./static/logo2.png", x=1, y=1, w=3)
        self.image("./static/logoDETRAN.png", x=17, y=1, w=3)

    def footer(self):
        # Setting position at 1.5 cm from bottom:
        self.set_y(-1.5)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        self.set_text_color(128)
        # Printing page number
        self.cell(0, 1, f"Página {self.page_no()} / {{nb}}", align="C")
        self.cell(0, 1, f"Desenvolvido por A3 DEV", align="C")

    def escreve_relatorio(self, dados) -> str:
        """
        Gera o relatório.

        :param dados: dicionário com as informações dos chamados de preventivas
        :return: None
        """
        self.add_font('roboto', style="", fname="./static/font/Roboto-Light.ttf")
        self.add_font('roboto', style="b", fname="./static/font/Roboto-Bold.ttf")
        self.add_page()
        ultimo_chamado = list(dados)[-1]
        for chave, valor in dados.items():
            # ---------------------- Bloco 1 --------------------------------------
            self.set_font(family='roboto', style='B', size=10)
            self.ln(1.5)
            self.cell(w=0, h=0.7, text=f"{chave} - {valor.fields.summary}", new_x="LMARGIN", new_y="NEXT", align="C")

            self.set_font(family='roboto', style='B', size=9)
            site = f'SITE: {valor.fields.customfield_10060} / {valor.fields.customfield_10060.child.value}'

            self.cell(w=0, h=1, text=site, new_x="LMARGIN", new_y="NEXT", align="L", border=1)

            self.cell(
                w=(self.epw / 2),
                h=1,
                text="COORDENADOR: RICARDO GONÇALVES",
                align="L",
                border=1,
            )

            self.cell(
                w=(self.epw / 2),
                h=1,
                text=f"TÉCNICO: {valor.fields.customfield_10135.value}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(w=(self.epw / 2), h=1, text=f"STATUS EQUIPAMENTO:OPERANDO",
                      align="L", border=1)

            self.cell(w=(self.epw / 2), h=1, text=f"COORDENADA:{valor.fields.customfield_10117}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=(self.epw / 2), h=1, text=f"MOTIVO DA VISITA:PREVENTIVA",
                      align="L", border=1)

            self.cell(
                w=(self.epw / 2),
                h=1,
                text=f"ENDEREÇO:{valor.fields.customfield_10118}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(
                w=0,
                h=1,
                text=f"DATA DA ABERTURA DO CHAMADO:{valor.fields.created}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(
                w=0,
                h=1,
                text=f" DATA DO FECHAMENTO DO CHAMADO:{valor.fields.resolutiondate}<",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.ln(1)

            # ---------------------- CHECK LIST --------------------------------------
            self.set_font(family='roboto', style='', size=10)

            check_list_velsis = f"""
            Checklist de atendimento para manutenção preventiva
            1-Realizou limpeza e verificação das caixas de câmeras? - {valor.fields.customfield_10124.value}
            2-Fechaduras e parafusos estão ok? - {valor.fields.customfield_10120.value}
            3-Realizou limpeza interna do Gabinete? - {valor.fields.customfield_10121.value}
            4-Realizou limpeza de todos os conectores do equipamento? - {valor.fields.customfield_10122.value}
            5-Realizou limpeza dos filtros do Coolers? - {valor.fields.customfield_10125.value}
            6-Realizou inspeção visual dos cabos de rede e energia? - {valor.fields.customfield_10126.value}
            7-Verificou os Iluminadores? - {valor.fields.customfield_10127.value}
            8-Verificou se existe alertas de funcionamento do Software? - {valor.fields.customfield_10128.value}
            9-Verificou as configurações do Software? - {valor.fields.customfield_10129.value}
            10-Verificou se conexões de rede do modem e sua conectividade com a central estão ok? - {valor.fields.customfield_10130.value}
            11-Desligou os programas em execução e ativou todos novamente? - {valor.fields.customfield_10131.value}
            12-As tensões da caixa de câmera estão ok? - >{valor.fields.customfield_10132.value}
            13-As tensões da caixa do iluminador estão ok? - {valor.fields.customfield_10133.value}
            14-As tensões do gabinete estão ok? - {valor.fields.customfield_10134.value}
            """

            self.multi_cell(
                w=0,
                h=1,
                text=check_list_velsis,
                border=1,
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            self.add_page()

            # ---------------------- Evidências -------------------------------------
            self.ln(2)
            self.cell(w=0, h=1, text=f"Evidências da visita no local",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            # ---------------------- ADICIONANDO ANEXOS -----------------------------
            issue = JiraReporter(
                app.config["BASE_URL"], app.config["USUARIO"], app.config["API_TOKEN"]
            )
            attachments = issue.getattachements(chave)
            posicao_imagem = 0

            def adiciona_imagem_na_posicao(imagem, local):

                posicao = [(2, 4), (11, 4), (2, 15), (11, 15)]
                self.image(imagem.get(), posicao[local][0], posicao[local][1], 8)

            def adicionar_pagina(numero_da_foto, posicao):
                if numero_da_foto % 2 == 0:
                    self.add_page()
                    posicao = 0
                    return posicao
                elif numero_da_foto == len(attachments.fields.attachment):
                    self.add_page()
                    posicao = 0
                    return posicao
                else:
                    posicao = posicao + 1
                    return posicao

            for count, attachment in enumerate(attachments.fields.attachment, 1):
                print(f"---{count}---{posicao_imagem}---{chave}")
                adiciona_imagem_na_posicao(attachment, posicao_imagem)
                posicao_imagem = adicionar_pagina(count, posicao_imagem)

        mes_anterior = date.today() - relativedelta(months=1)
        endereco = f"static{os.sep}relatorios{os.sep}velsis-{mes_anterior.year}-{mes_anterior.month}.pdf"
        self.output(endereco)
        return endereco
