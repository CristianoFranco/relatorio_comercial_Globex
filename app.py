from datetime import datetime
import io
import os
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Globex Multimodal - Ficha de Armazenagem",
    page_icon="📦",
    layout="centered"
)

# 01) Logo da Globex no cabeçalho centralizado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists("Logo.png"):
        st.image("Logo.png", use_container_width=True)
    else:
        st.warning("⚠️ Ficheiro 'Logo.png' não encontrado na pasta do projeto.")

st.markdown("<h2 style='text-align: center; color: #0A3641;'>Ficha Cadastral de Armazenagem</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Preencha os dados abaixo após o fechamento da proposta comercial.</p>", unsafe_allow_html=True)
st.markdown("---")

# Inicializar a lista de responsáveis no session_state
if "responsaveis" not in st.session_state:
    st.session_state["responsaveis"] = [
        {"nome": "", "setor": "Logística", "outro_setor": "", "telefone": "", "email": ""}
    ]

def adicionar_responsavel():
    st.session_state["responsaveis"].append(
        {"nome": "", "setor": "Logística", "outro_setor": "", "telefone": "", "email": ""}
    )

def remover_responsavel(index):
    if len(st.session_state["responsaveis"]) > 1:
        st.session_state["responsaveis"].pop(index)

# 1. DADOS DA EMPRESA
st.subheader("1. Dados da Empresa *(Obrigatório)*")
razao_social = st.text_input("Razão Social *", key="input_razao")
cnpj = st.text_input("CNPJ *", placeholder="00.000.000/0001-00", key="input_cnpj")
data_constituicao = st.date_input("Data de Constituição *", value=None, key="input_constituicao")
ramo_atividade = st.text_input("Ramo de Atividade *", key="input_ramo")

st.markdown("")

# 2. ENDEREÇO COMPLETO (Tratamento para reconhecimento de autofill do navegador)
st.subheader("2. Endereço Completo *(Obrigatório)*")
st.markdown("<p style='font-size: 12px; color: #666;'>* Dica: Se usar o preenchimento automático do navegador e o botão apontar campo vazio, clique brevemente em cima do campo para validar.</p>", unsafe_allow_html=True)

col_end1, col_end2 = st.columns([3, 1])
with col_end1:
    rua = st.text_input("Rua *", key="input_rua")
with col_end2:
    numero = st.text_input("Número *", key="input_numero")
    
bairro = st.text_input("Bairro *", key="input_bairro")

col_cidade, col_uf, col_cep = st.columns([2, 1, 1])
with col_cidade:
    cidade = st.text_input("Cidade *", key="input_cidade")
with col_uf:
    uf = st.text_input("UF *", max_chars=2, key="input_uf")
with col_cep:
    cep = st.text_input("CEP *", placeholder="00000-000", key="input_cep")

st.markdown("")

# 3. INSCRIÇÕES E REGIME TRIBUTÁRIO
st.subheader("3. Inscrições e Regime Tributário *(Obrigatório)*")
inscricao_estadual = st.text_input("Inscrição Estadual * (ou 'Isento')", key="input_ie")
inscricao_municipal = st.text_input("Inscrição Municipal * (ou 'Isento')", key="input_im")

st.markdown("**Regime Tributário da Empresa: ***")
regime_tributario = st.radio(
    "Selecione o Regime Tributário",
    ["Simples Nacional", "Lucro Presumido", "Lucro Real", "Outro"],
    label_visibility="collapsed",
    key="radio_regime"
)

regime_outro = ""
if regime_tributario == "Outro":
    regime_outro = st.text_input("Especifique o Regime Tributário Outro *", key="input_regime_outro")

st.markdown("---")

# 4. RESPONSÁVEIS
st.subheader("4. Responsáveis")
st.markdown("Preencha os dados dos responsáveis da empresa por setor.")

setores_predefinidos = ["Logística", "Financeiro", "Operação", "Compras", "Responsável Técnico"]

for i, resp in enumerate(st.session_state["responsaveis"]):
    st.markdown(f"**Responsável {i+1}**")
    c_r1, c_r2 = st.columns([2, 2])
    
    with c_r1:
        st.session_state["responsaveis"][i]["nome"] = st.text_input(f"Nome completo {i+1}", value=resp["nome"], key=f"nome_{i}")
    with c_r2:
        escolha_setor = st.selectbox(
            f"Setor Responsável {i+1}",
            setores_predefinidos + ["Outro (Cadastrar novo)"],
            index=setores_predefinidos.index(resp["setor"]) if resp["setor"] in setores_predefinidos else len(setores_predefinidos),
            key=f"setor_select_{i}"
        )
        
        if escolha_setor == "Outro (Cadastrar novo)":
            novo_setor = st.text_input(f"Especifique o novo setor {i+1}", value=resp["outro_setor"], key=f"outro_setor_{i}")
            st.session_state["responsaveis"][i]["setor"] = novo_setor
            st.session_state["responsaveis"][i]["outro_setor"] = novo_setor
        else:
            st.session_state["responsaveis"][i]["setor"] = escolha_setor
            st.session_state["responsaveis"][i]["outro_setor"] = ""

    c_r3, c_r4 = st.columns([1, 1])
    with c_r3:
        st.session_state["responsaveis"][i]["telefone"] = st.text_input(f"Telefone / WhatsApp {i+1}", value=resp["telefone"], key=f"tel_{i}")
    with c_r4:
        st.session_state["responsaveis"][i]["email"] = st.text_input(f"E-mail {i+1}", value=resp["email"], key=f"email_{i}")
    
    if len(st.session_state["responsaveis"]) > 1:
        st.button("🗑️ Remover este responsável", key=f"rem_{i}", on_click=remover_responsavel, args=(i,))
    st.markdown("---")

# Botão para adicionar responsável acima da data
st.button("➕ Adicionar Outro Responsável", on_click=adicionar_responsavel, type="secondary", use_container_width=True)

st.markdown("")

# 5. CONFIRMAÇÃO (Data automática)
data_preenchimento = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
st.info(f"📅 **Data do preenchimento:** {data_preenchimento} (Gerada automaticamente)")

st.markdown("")

# Botão de Geração do PDF
submitted = st.button("Gerar PDF da Proposta", type="primary", use_container_width=True)

if submitted:
    erros = []
    if not razao_social: erros.append("Razão Social")
    if not cnpj: erros.append("CNPJ")
    if not data_constituicao: erros.append("Data de Constituição")
    if not ramo_atividade: erros.append("Ramo de Atividade")
    if not rua or not numero or not bairro or not cidade or not uf or not cep: erros.append("Endereço Completo")
    if not inscricao_estadual: erros.append("Inscrição Estadual")
    if not inscricao_municipal: erros.append("Inscrição Municipal")
    if regime_tributario == "Outro" and not regime_outro: erros.append("Especificação do Regime Tributário 'Outro'")

    if erros:
        st.error(f"⚠️ Preencha os seguintes campos obrigatórios antes de gerar o PDF: {', '.join(erros)}.")
    else:
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=2 * cm,
                leftMargin=2 * cm,
                topMargin=2 * cm,
                bottomMargin=2.5 * cm
            )
            
            styles = getSampleStyleSheet()
            
            style_title = ParagraphStyle(
                'PdfTitle',
                parent=styles['Heading1'],
                fontSize=14,
                alignment=1,
                textColor=colors.HexColor('#0A3641'),
                spaceAfter=15
            )
            style_subtitle = ParagraphStyle(
                'PdfSubtitle',
                parent=styles['Heading2'],
                fontSize=11,
                textColor=colors.HexColor('#0A3641'),
                spaceBefore=10,
                spaceAfter=5
            )
            style_body = ParagraphStyle(
                'PdfBody',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#333333'),
                spaceAfter=4
            )

            story = []

            # 02) Logo ajustada no PDF sem distorção (proporção correta de largura e altura proporcionais)
            if os.path.exists("Logo.png"):
                from reportlab.platypus import Image
                img = Image("Logo.png", width=6 * cm, height=1.65 * cm)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 10))

            story.append(Paragraph("FICHA CADASTRAL DE ARMAZENAGEM - GLOBEX MULTIMODAL", style_title))
            story.append(Spacer(1, 5))

            story.append(Paragraph("1. DADOS DA EMPRESA", style_subtitle))
            data_empresa = [
                [Paragraph(f"<b>Razão Social:</b> {razao_social}", style_body), Paragraph(f"<b>CNPJ:</b> {cnpj}", style_body)],
                [Paragraph(f"<b>Data de Constituição:</b> {data_constituicao.strftime('%d/%m/%Y')}", style_body), Paragraph(f"<b>Ramo de Atividade:</b> {ramo_atividade}", style_body)]
            ]
            t1 = Table(data_empresa, colWidths=[9 * cm, 8 * cm])
            t1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
            story.append(t1)

            story.append(Paragraph("2. ENDEREÇO COMPLETO", style_subtitle))
            data_end = [
                [Paragraph(f"<b>Logradouro:</b> {rua}, Nº {numero}", style_body), Paragraph(f"<b>Bairro:</b> {bairro}", style_body)],
                [Paragraph(f"<b>Cidade/UF:</b> {cidade} - {uf}", style_body), Paragraph(f"<b>CEP:</b> {cep}", style_body)]
            ]
            t2 = Table(data_end, colWidths=[10 * cm, 7 * cm])
            t2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
            story.append(t2)

            story.append(Paragraph("3. INSCRIÇÕES E REGIME TRIBUTÁRIO", style_subtitle))
            regime_final = regime_tributario if regime_tributario != "Outro" else f"Outro: {regime_outro}"
            data_tribut = [
                [Paragraph(f"<b>Inscrição Estadual:</b> {inscricao_estadual}", style_body), Paragraph(f"<b>Inscrição Municipal:</b> {inscricao_municipal}", style_body)],
                [Paragraph(f"<b>Regime Tributário:</b> {regime_final}", style_body), Paragraph("", style_body)]
            ]
            t3 = Table(data_tribut, colWidths=[9 * cm, 8 * cm])
            t3.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
            story.append(t3)

            story.append(Paragraph("4. RESPONSÁVEIS", style_subtitle))
            for idx, resp in enumerate(st.session_state["responsaveis"]):
                if resp["nome"].strip():
                    data_resp = [
                        [Paragraph(f"<b>Responsável {idx+1}:</b> {resp['nome']}", style_body), Paragraph(f"<b>Setor:</b> {resp['setor']}", style_body)],
                        [Paragraph(f"<b>Telefone/WhatsApp:</b> {resp['telefone']}", style_body), Paragraph(f"<b>E-mail:</b> {resp['email']}", style_body)]
                    ]
                    t_resp = Table(data_resp, colWidths=[9 * cm, 8 * cm])
                    t_resp.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('BOTTOMPADDING', (0,0), (-1,-1), 6)]))
                    story.append(t_resp)

            story.append(Paragraph("5. CONFIRMAÇÃO", style_subtitle))
            story.append(Paragraph(f"<b>Data e Hora do Preenchimento:</b> {data_preenchimento}", style_body))

            def add_footer(canvas, doc):
                canvas.saveState()
                canvas.setFont('Helvetica', 8)
                canvas.setFillColor(colors.HexColor('#555555'))
                
                linha1 = "Avenida Vitoria Rossi Martini, 31"
                linha2 = "Distrito Industrial Indaiatuba - SP - CEP: 13.347-613"
                linha3 = "+55 19 3936-8520 / www.globexmultimodal.com.br"
                
                width, _ = A4
                canvas.drawCentredString(width / 2.0, 45, linha1)
                canvas.drawCentredString(width / 2.0, 33, linha2)
                canvas.drawCentredString(width / 2.0, 21, linha3)
                canvas.restoreState()

            doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
            buffer.seek(0)
            
            st.success("🎉 PDF gerado com sucesso!")
            
            # 01) Nome do PDF alterado para Ficha_Cadastral_Armazenagem
            st.download_button(
                label="📥 Baixar PDF Preenchido",
                data=buffer,
                file_name=f"Ficha_Cadastral_Armazenagem_{razao_social.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary"
            )

        except Exception as e:
            st.error(o := f"Ocorreu um erro ao gerar o arquivo PDF: {e}")

# 02) Endereço da Globex no rodapé centralizado da página web do Streamlit
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666666; font-size: 13px; line-height: 1.5;'>
        <b>Avenida Vitoria Rossi Martini, 31</b><br>
        Distrito Industrial Indaiatuba - SP - CEP: 13.347-613<br>
        +55 19 3936-8520 / www.globexmultimodal.com.br
    </div>
    """,
    unsafe_allow_html=True
)
