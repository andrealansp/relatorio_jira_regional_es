import os
from datetime import date

from dateutil.relativedelta import relativedelta
from fpdf import FPDF

from jirareporter import JiraReporter
from app import app


class PdfSalas(FPDF):

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
        self.add_font("roboto", style="", fname="./static/font/Roboto-Light.ttf")
        self.add_font("roboto", style="b", fname="./static/font/Roboto-Bold.ttf")
        self.add_page()
        ultimo_chamado = list(dados)[-1]
        for chave, valor in dados.items():
            # ---------------------- Bloco 1 --------------------------------------
            self.set_font(family="roboto", style="B", size=10)
            self.ln(1.5)
            self.cell(w=0, h=0.7, text=f"{chave} - {valor.fields.summary}", new_x="LMARGIN", new_y="NEXT", align="C")

            self.set_font(family="roboto", style="B", size=9)
            site = f'SITE: {valor.fields.customfield_10060} / {valor.fields.customfield_10060.child.value}'

            self.cell(w=0, h=1, text=site, new_x="LMARGIN", new_y="NEXT", align="L", border=1)

            self.cell(w=(self.epw / 2), h=1, text="COORDENADOR: ALEXANDER SANTOS", align="L", border=1)

            self.cell(w=(self.epw / 2), h=1, text=f"TÉCNICO: {valor.fields.customfield_10116.value}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=(self.epw / 2), h=1, text=f"STATUS EQUIPAMENTO:OPERANDO",
                      align="L", border=1)

            self.cell(
                w=(self.epw / 2),
                h=1,
                text=f"LOCAL:SALAS DE OPERAÇÃO",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(w=(self.epw / 2), h=1, text=f"MOTIVO DA VISITA:PREVENTIVA",
                      align="L", border=1)

            self.cell(
                w=(self.epw / 2),
                h=1,
                text=f"ENDEREÇO:{valor.fields.customfield_10060.value}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(w=0, h=1, text=f"DATA DA VISITA: {valor.fields.customfield_10139}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=0, h=1, text=f"INÍCIO: {valor.fields.customfield_10141}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=0, h=1, text=f"FIM: {valor.fields.customfield_10144}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.ln(1)

            # ---------------------- CHECK LIST --------------------------------------
            self.set_font(family="roboto", style="", size=10)

            check_list_salas = f"""Checklist de atendimento para manutenção preventiva
            1 – Verificada a limpeza e organização interna das mesas ?  {valor.fields.customfield_10145.value} 
            2 – Verificada as conexões de rede dos computadores ? {valor.fields.customfield_10146.value}
            3 – Verificada as conexões do controlador com telas do Video wall? {valor.fields.customfield_10147.value}
            4 – Efetuado teste de autonimia do nobreak ? {valor.fields.customfield_10148.value}
            5 - Foi verificado os estado das baterias do nobreak ? {valor.fields.customfield_10149.value}
            6 – Telas do video wall estão funcionais? {valor.fields.customfield_10150.value}
            7 – Estações de trabalho (desktop / monitores) estão funcionais ? {valor.fields.customfield_10151.value}
            8 – Ambiente encontra-se climatizado ? {valor.fields.customfield_10152.value}
            9 - Verificada as conexões dos computadores com Video wall ? {valor.fields.customfield_10153.value}
            """
            self.multi_cell(
                w=0,
                h=1,
                text=check_list_salas,
                align="L",
                border=1,
                new_x="LMARGIN",
                new_y="NEXT",
            )

            self.add_page()

            # ---------------------- Evidências -------------------------------------
            self.set_font(family="roboto", style="B", size=10)
            self.ln(2)
            self.cell(w=0, h=1, text=f"Evidências da visita no local",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            # ---------------------- ADICIONANDO ANEXOS -----------------------------
            def desenhalinha(imagem, local):
                posicao = [(2, 4), (11, 4), (2, 15), (11, 15)]
                self.image(imagem.get(), posicao[local][0], posicao[local][1], 8)

            issue = JiraReporter(app.config["BASE_URL"], app.config["USUARIO"], app.config["API_TOKEN"])
            attachments = issue.getattachements(chave)
            quantidade_de_fotos = len(attachments.fields.attachment)
            for count, attachment in enumerate(attachments.fields.attachment, 0):
                if quantidade_de_fotos < 4:
                    desenhalinha(attachment, count)
                    if not ultimo_chamado == chave:
                        if count == quantidade_de_fotos - 1:
                            self.add_page()
                else:
                    if not ultimo_chamado == chave:
                        desenhalinha(attachment, count)
                        if count == 4 or count == 8:
                            self.add_page()

        mes_anterior = date.today() - relativedelta(months=1)
        endereco = f"static{os.sep}relatorios{os.sep}salas-{mes_anterior.year}-{mes_anterior.month}.pdf"
        self.output(endereco)
        return endereco
