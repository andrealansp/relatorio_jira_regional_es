import datetime
import os
from io import BytesIO

from fpdf import FPDF

import acessojira


class PDF(FPDF):

    def header(self):
        pass

    def footer(self):
        # Setting position at 1.5 cm from bottom:
        self.set_y(-1.5)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Setting text color to gray:
        self.set_text_color(128)
        # Printing page number
        self.cell(0, 1, f"Page {self.page_no()}", align="C")

    def escreve_relatorio(self, dados, anexos) -> str:
        """
        Gera o relatório.

        :param dados: dicionário com as informações dos chamados de preventivas
        :param anexos: lista com os links para as imagens do relatório
        :return: None
        """
        self.add_page()
        for chave, valor in dados.items():
            # ---------------------- Bloco 1 --------------------------------------
            self.set_font(family='helvetica', style='B', size=10)
            self.cell(w=0, h=0.7, text=f"{chave} - {valor['summary']}", new_x="LMARGIN", new_y="NEXT", align="C")

            self.set_font(family='helvetica', style='B', size=9)
            site = (f"SITE: {valor.get('customfield_10060').get('value')} / "
                    f"{valor.get('customfield_10060').get('child').get('value')}")

            self.cell(w=0, h=1, text=site, new_x="LMARGIN", new_y="NEXT", align="L", border=1)

            self.cell(w=(self.epw / 2), h=1, text="COORDENADOR: ALEXANDER SANTOS", align="L", border=1)

            self.cell(w=(self.epw / 2), h=1, text=f"TÉCNICO: {valor['customfield_10116']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=(self.epw / 2), h=1, text=f"STATUS EQUIPAMENTO:OPERANDO",
                      align="L", border=1)

            self.cell(w=(self.epw / 2), h=1, text=f"COORDENADA:{valor['customfield_10117']}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=(self.epw / 2), h=1, text=f"MOTIVO DA VISITA:PREVENTIVA",
                      align="L", border=1)

            self.cell(w=(self.epw / 2), h=1,
                      text=f"ENDEREÇO:{valor['customfield_10118']['content'][0]['content'][0]['text']}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=0, h=1, text=f"DATA DA VISITA: {valor['customfield_10139']}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=0, h=1, text=f"INÍCIO: {valor['customfield_10141']}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.cell(w=0, h=1, text=f"FIM: {valor['customfield_10144']}",
                      align="L", new_x="LMARGIN", new_y="NEXT", border=1)

            self.ln(1)

            # ---------------------- CHECK LIST --------------------------------------
            self.set_font(family='helvetica', style='B', size=10)
            self.cell(w=0, h=1, text=f"Checklist de atendimento para manutenção preventiva",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.set_font(family='helvetica', style='B', size=9)
            self.cell(w=0, h=1, text=f"1-Efetuada a limpeza de lentes e cúpulas? "
                                     f"{valor['customfield_10106']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1, text=f"2-Necessário ajustes de posicionamento? "
                                     f"{valor['customfield_10107']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1, text=f"3-Foram verificadas as conexões de cabeamento lógico? "
                                     f"{valor['customfield_10108']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1, text=f"4-Foram verificados os componentes elétricos utilizados para alimentação dos "
                                     f"equipamentos(nobreak,disjuntor e fusíveis)? "
                                     f"{valor['customfield_10109']['value']} ",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1,
                      text=f"5-Foi verifica do os estado das baterias para alimentação externa(painelsolar)? "
                           f"{valor['customfield_10109']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1, text=f"6-Efetuada a limpeza preventiva externa e interna dos equipamentos? "
                                     f"{valor['customfield_10110']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1, text=f"7-Foi verificado o reaperto dos contatos elétricos? "
                                     f"{valor['customfield_10112']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1, text=f"8-Foi verificada a vedaçãodo gabinete? "
                                     f"{valor['customfield_10113']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1, text=f"9-Há obstrução das lentes das câmeras? "
                                     f"{valor['customfield_10114']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.cell(w=0, h=1, text=f"10-Verificada a conectividade com o DSS? "
                                     f"{valor['customfield_10115']['value']}",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            self.add_page()

            # ---------------------- Evidências -------------------------------------

            self.cell(w=0, h=1, text=f"Evidências da visita no local",
                      align="L", new_x="LMARGIN", new_y="NEXT")

            def desenhalinha(imagem, local):
                posicao = [(2, 2), (11, 2), (2, 14), (11, 14)]
                self.image(imagem, posicao[local][0], posicao[local][1], 8)

            count = 0

            for indice, anexo in enumerate(anexos.get(chave), 0):
                print("#" * indice, anexo[1], count)
                imagem = acessojira.JiraReporter.baixar_anexos(anexo[1], chave)
                desenhalinha(imagem, count)
                count = count + 1
                if count > 3:
                    count = 0
                    self.add_page()

        self.output(f"static{os.sep}relatorios{os.sep}{datetime.date.today().year}-{datetime.date.today().month}.pdf")

        return os.path.basename(
            f"static{os.sep}relatorios{os.sep}{datetime.date.today().year}-{datetime.date.today().month}.pdf")
