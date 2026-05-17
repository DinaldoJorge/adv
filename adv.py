# =====================================================
# MZA ADVOGADOS - CÓDIGO FINAL COMPLETO
# =====================================================

import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="MZA Advogados",
    page_icon="⚖️",
    layout="wide"
)

# =====================================================
# LOGIN
# =====================================================

USUARIO = "admin"
SENHA = "mza2026"

if "logado" not in st.session_state:
    st.session_state["logado"] = False

# =====================================================
# CSS PREMIUM
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:black;
    color:white;
}

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

.block-container{
    padding-top:2rem;
    max-width:1200px;
}

/* =====================================================
FRASE
===================================================== */

.frase{
    text-align:center;
    font-size:28px;
    font-weight:900;
    color:white;
    margin-top:10px;
    margin-bottom:45px;
}

.frase span{
    color:#00d9ff;
}

/* =====================================================
LABELS
===================================================== */

label{
    color:white !important;
    font-size:25px !important;
    font-weight:800 !important;
}

/* =====================================================
INPUTS
===================================================== */

.stTextInput input{

    background:black !important;

    color:white !important;

    border:2px solid white !important;

    border-radius:4px !important;

    height:45px !important;

    font-size:18px !important;

    font-weight:600 !important;

    padding-left:18px !important;

    transition:0.3s !important;
}

.stTextInput input:focus{

    border:2px solid #00d9ff !important;
}

/* =====================================================
TEXTAREA
===================================================== */

.stTextArea textarea{

    background:black !important;

    color:white !important;

    border:2px solid white !important;

    border-radius:4px !important;

    font-size:19px !important;

    font-weight:600 !important;

    padding:18px !important;

    transition:0.3s !important;
}

.stTextArea textarea:focus{

    border:2px solid #00d9ff !important;
}

/* =====================================================
PLACEHOLDER
===================================================== */

::placeholder{

    color:#00d9ff !important;

    opacity:1 !important;
}

/* =====================================================
FILE UPLOADER PREMIUM
===================================================== */

[data-testid="stFileUploader"]{

    background:black !important;

    border:2px solid #00d9ff !important;

    border-radius:4px !important;

    padding:22px !important;

    margin-top:15px !important;
}

[data-testid="stFileUploader"] section{

    background:#f5f5f5 !important;

    border-radius:4px !important;

    border:1px solid rgba(255,255,255,0.15) !important;

    padding:22px !important;
}

[data-testid="stFileUploader"] div{

    background-color:transparent !important;
}

[data-testid="stFileUploader"] small{

    color:#0066ff !important;

    font-size:17px !important;

    font-weight:350 !important;
}

[data-testid="stFileUploader"] label{

    color:white !important;

    font-size:20px !important;

    font-weight:800 !important;
}

[data-testid="stFileUploader"] p{

    color:#00d9ff !important;

    font-size:16px !important;

    font-weight:700 !important;
}

[data-testid="stFileUploader"] button{

    background:linear-gradient(
        135deg,
        #0066ff,
        #00aaff
    ) !important;

    color:black !important;

    border:none !important;

    border-radius:14px !important;

    font-size:18px !important;

    font-weight:800 !important;

    height:45px !important;

    padding:0 30px !important;

    transition:all 0.25s ease-in-out !important;
}

[data-testid="stFileUploader"] button:hover{

    background:linear-gradient(
        135deg,
        #0055ff,
        #00ccff
    ) !important;

    color:black !important;

    transform:translateY(-2px) scale(1.03);
}

/* =====================================================
BOTÕES PREMIUM GERAIS
===================================================== */

.stForm button,
.stButton > button,
[data-testid="stDownloadButton"] button{

    width:100% !important;

    height:58px !important;

    border:none !important;

    border-radius:18px !important;

    background:linear-gradient(
        135deg,
        #0066ff,
        #00aaff
    ) !important;

    color:black !important;

    font-size:20px !important;

    font-weight:900 !important;

    letter-spacing:0.5px !important;

    box-shadow:
        0 0 12px rgba(0,170,255,0.5),
        0 0 25px rgba(0,100,255,0.3) !important;

    transition:all 0.25s ease-in-out !important;
}

.stForm button:hover,
.stButton > button:hover,
[data-testid="stDownloadButton"] button:hover{

    background:linear-gradient(
        135deg,
        #0055ff,
        #00ccff
    ) !important;

    color:black !important;

    transform:translateY(-2px) scale(1.02);
}

/* =====================================================
CARD
===================================================== */

.card{

    background:linear-gradient(
        180deg,
        #111111,
        #0d0d0d
    );

    border:2px solid #00d9ff;

    border-radius:22px;

    padding:35px;

    margin-bottom:30px;

    box-shadow:
        0 0 15px rgba(0,217,255,0.15);
}

/* =====================================================
FOOTER
===================================================== */

.footer{

    text-align:center;

    color:#00d9ff;

    margin-top:40px;

    font-size:13px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEETS
# =====================================================

planilha = None

try:

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    planilha = client.open(
        "leads_professores"
    ).sheet1

except Exception as e:

    st.error("Erro ao conectar com Google Sheets.")
    st.stop()

# =====================================================
# LOGO
# =====================================================

col1, col2, col3 = st.columns([1,2,1])

with col2:

    if os.path.exists("logomza.png"):

        st.image(
            "logomza.png",
            width=420
        )

# =====================================================
# FRASE
# =====================================================

st.markdown("""
<div class="frase">
Vamos <span>analisar</span> seus dados
</div>
""", unsafe_allow_html=True)

# =====================================================
# FORMULÁRIO
# =====================================================

with st.form("formulario", clear_on_submit=True):

    nome = st.text_input(
        "Nome completo",
        placeholder="Digite seu nome"
    )

    email = st.text_input(
        "Email",
        placeholder="Digite seu melhor email"
    )

    telefone = st.text_input(
        "Telefone",
        placeholder="Digite seu telefone"
    )

    caso = st.text_area(
        "Caso jurídico",
        placeholder="Explique sua situação jurídica...",
        height=220
    )

    arquivo = st.file_uploader(
        "📎 Anexar documento",
        type=["pdf","png","jpg","jpeg","doc","docx"]
    )

    enviar = st.form_submit_button(
        "Enviar Dados"
    )

# =====================================================
# FUNÇÃO SALVAR
# =====================================================

def salvar_dados():

    nome_arquivo = "Nenhum arquivo"

    if arquivo is not None:

        os.makedirs(
            "documentos",
            exist_ok=True
        )

        caminho = os.path.join(
            "documentos",
            arquivo.name
        )

        with open(caminho, "wb") as f:
            f.write(arquivo.getbuffer())

        nome_arquivo = arquivo.name

    data = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    ).strftime("%d/%m/%Y %H:%M")

    planilha.append_row([
        nome,
        email,
        telefone,
        caso,
        nome_arquivo,
        data
    ])

# =====================================================
# ENVIAR
# =====================================================

if enviar:

    if nome and email and caso:

        try:

            salvar_dados()

            st.success(
                "Dados enviados com sucesso!\n\nClique no botão abaixo para fazer contato com o advogado."
            )

            st.markdown("""
            <a href="https://wa.me/5583998234415" target="_blank">
                <button style="
                    width:100%;
                    height:60px;
                    margin-top:20px;
                    border:none;
                    border-radius:18px;
                    background:linear-gradient(135deg,#0066ff,#00aaff);
                    color:black;
                    font-size:20px;
                    font-weight:900;
                    cursor:pointer;
                ">
                📲 Contato direto MZA-Advogados
                </button>
            </a>
            """, unsafe_allow_html=True)

        except Exception as e:

            st.error(
                "Erro ao salvar informações."
            )

    else:

        st.warning(
            "Preencha os campos obrigatórios."
        )
