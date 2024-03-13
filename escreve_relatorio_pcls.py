import os
from datetime import date

from dateutil.relativedelta import relativedelta
from fpdf import FPDF

from jirareporter import JiraReporter
from app import app


class PdfPcls(FPDF):

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
            self.cell(
                w=0,
                h=0.7,
                text=f"{chave} - {valor.fields.summary}",
                new_x="LMARGIN",
                new_y="NEXT",
                align="C",
            )

            self.set_font(family="roboto", style="B", size=9)
            site = f"SITE: {valor.fields.customfield_10060} / {valor.fields.customfield_10060.child.value}"

            self.cell(
                w=0, h=1, text=site, new_x="LMARGIN", new_y="NEXT", align="L", border=1
            )

            self.cell(
                w=(self.epw / 2),
                h=1,
                text="COORDENADOR: ALEXANDER SANTOS",
                align="L",
                border=1,
            )

            self.cell(
                w=(self.epw / 2),
                h=1,
                text=f"TÉCNICO: {valor.fields.customfield_10116.value}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(
                w=(self.epw / 2),
                h=1,
                text=f"STATUS EQUIPAMENTO:OPERANDO",
                align="L",
                border=1,
            )

            self.cell(
                w=(self.epw / 2),
                h=1,
                text=f"COORDENADA:{valor.fields.customfield_10117}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(
                w=(self.epw / 2),
                h=1,
                text=f"MOTIVO DA VISITA:PREVENTIVA",
                align="L",
                border=1,
            )

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
                text=f"DATA DA VISITA: {valor.fields.customfield_10139}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(
                w=0,
                h=1,
                text=f"INÍCIO: {valor.fields.customfield_10141}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.cell(
                w=0,
                h=1,
                text=f"FIM: {valor.fields.customfield_10144}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
                border=1,
            )

            self.ln(1)

            # ---------------------- CHECK LIST --------------------------------------
            self.set_font(family="roboto", style="", size=10)

            check_list_pcl = f"""Checklist de atendimento para manutenção preventiva
            1-Efetuada a limpeza de lentes e cúpulas? - {valor.fields.customfield_10106.value}
            2-Necessário ajustes de posicionamento? - {valor.fields.customfield_10107.value}
            3-Foram verificadas as conexões de cabeamento lógico? - {valor.fields.customfield_10108.value}
            4-Foram verificados os componentes elétricos utilizados para alimentação dos equipamentos
            (nobreak,disjuntor e fusíveis)? - {valor.fields.customfield_10109.value}
            5-Foi verifica do os estado das baterias para alimentação externa(painelsolar)? - {valor.fields.customfield_10110.value}
            6-Efetuada a limpeza preventiva externa e interna dos equipamentos? - {valor.fields.customfield_10111.value}
            7-Foi verificado o reaperto dos contatos elétricos? {valor.fields.customfield_10112.value}
            8-Foi verificada a vedaçãodo gabinete? {valor.fields.customfield_10113.value}
            9-Há obstrução das lentes das câmeras? {valor.fields.customfield_10114.value}
            10-Verificada a conectividade com o DSS? {valor.fields.customfield_10115.value}
            """

            self.multi_cell(
                w=0,
                h=1,
                text=check_list_pcl,
                border=1,
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            self.add_page()

            # ---------------------- Evidências -------------------------------------
            self.ln(2)
            self.set_font(family="roboto", style="B", size=10)
            self.cell(
                w=0,
                h=1,
                text=f"Evidências da visita no local",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT",
            )

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
                if numero_da_foto % 4 == 0:
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
                if not count > 6:
                    print(f"---{count}---{posicao_imagem}---{chave}")
                    adiciona_imagem_na_posicao(attachment, posicao_imagem)
                    posicao_imagem = adicionar_pagina(count, posicao_imagem)

        mes_anterior = date.today() - relativedelta(months=1)
        endereco = f"static{os.sep}relatorios{os.sep}pcls-{mes_anterior.year}-{mes_anterior.month}.pdf"
        self.output(endereco)
        return os.path.basename(endereco)
