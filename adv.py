import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os

# =========================================
# CONFIGURAÇÃO
# =========================================
st.set_page_config(
    page_title="MZA",
    page_icon="⚖️",
    layout="wide"
)

# =========================================
# LOGIN
# =========================================
USUARIO = "admin"
SENHA = "mza2026"

if "logado" not in st.session_state:
    st.session_state["logado"] = False

# =========================================
# CSS
# =========================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.stApp {
    background-color: black;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

html, body, [class*="css"] {

    font-family: 'Inter', sans-serif;

    color: white;
}

.block-container {

    max-width: 1200px;

    padding-top: 1rem;

    padding-bottom: 2rem;
}

/* FRASE */
.frase {

    text-align: center;

    font-size: 26px;

    font-weight: 900;

    color: white;

    margin-top: 5px;

    margin-bottom: 45px;
}

.frase span {

    color: #00d9ff;
}

/* LABELS */
label {

    color: white !important;

    font-size: 20px !important;

    font-weight: 800 !important;
}

/* INPUTS */
.stTextInput input {

    background: #ffffff !important;

    border: 4px solid #00aaff !important;

    border-radius: 0px !important;

    color: #000000 !important;

    font-size: 20px !important;

    font-weight: 700 !important;

    height: 45px !important;

    padding: 0 22px !important;

    box-sizing: border-box !important;

    transition: all 0.25s ease !important;
}

/* INPUT AO CLICAR */
.stTextInput input:focus {

    border: 4px solid #00ff88 !important;

    box-shadow:
        0 0 12px rgba(0,255,136,0.25) !important;

    outline: none !important;
}

/* INPUT COM TEXTO */
.stTextInput input:not(:placeholder-shown) {

    border: 4px solid #00ff88 !important;
}

/* TEXTAREA */
.stTextArea textarea {

    background: white !important;

    border: 2px solid #00aaff !important;

    color: black !important;

    font-size: 22px !important;

    font-weight: 700 !important;

    padding: 24px !important;

    transition: all 0.25s ease !important;
}

/* TEXTAREA FOCUS */
.stTextArea textarea:focus {

    border: 2px solid #00ff88 !important;

    box-shadow:
        0 0 12px rgba(0,255,136,0.25) !important;
}

/* FILE */
[data-testid="stFileUploader"] {

    background: #0b0b0b !important;

    border: 2px solid #00d9ff !important;

    padding: 18px !important;
}

/* BOTÃO */
.stButton > button {

    background: linear-gradient(
        90deg,
        #00aaff,
        #00d9ff
    );

    color: black !important;

    border: none !important;

    font-size: 22px !important;

    font-weight: 900 !important;

    height: 45px !important;

    width: 100%;
}

/* CARD */
.card {

    background: linear-gradient(
        180deg,
        #0b0b0b 0%,
        #111111 100%
    );

    padding: 40px;

    margin-bottom: 40px;

    border: 1px solid #00d9ff;
}

/* TITULO */
.titulo-admin {

    font-size: 24px;

    font-weight: 900;

    text-align: center;

    margin-top: 20px;

    margin-bottom: 25px;

    color: white;
}

/* FOOTER */
.footer {

    text-align: center;

    color: #d0d0d0;

    font-size: 12px;

    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# GOOGLE SHEETS
# =========================================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

planilha = client.open("leads_professores").sheet1

# =========================================
# LOGO
# =========================================
col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.image(
        "logomza.png",
        width=320
    )

# =========================================
# FRASE
# =========================================
st.markdown("""
<div class="frase">
Vamos <span>analisar</span> seus dados
</div>
""", unsafe_allow_html=True)

# =========================================
# FORM
# =========================================
with st.form("formulario_cliente", clear_on_submit=True):

    nome = st.text_input(
        "Nome completo"
    )

    email = st.text_input(
        "Email"
    )

    telefone = st.text_input(
        "Telefone"
    )

    caso = st.text_area(
        "Caso jurídico",
        height=260
    )

    arquivo = st.file_uploader(
        "📎 Anexar documentos",
        type=[
            "pdf",
            "doc",
            "docx",
            "png",
            "jpg",
            "jpeg"
        ]
    )

    enviar = st.form_submit_button(
        "Enviar Dados"
    )

# =========================================
# SALVAR
# =========================================
def salvar(nome, email, telefone, caso, nome_arquivo):

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

# =========================================
# ENVIAR
# =========================================
if enviar:

    if nome and email and caso:

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

            with open(
                caminho,
                "wb"
            ) as f:

                f.write(
                    arquivo.getbuffer()
                )

            nome_arquivo = arquivo.name

        salvar(
            nome,
            email,
            telefone,
            caso,
            nome_arquivo
        )

        st.success(
            "Dados enviados com sucesso!"
        )

    else:

        st.error(
            "Preencha os campos obrigatórios."
        )

# =========================================
# LOGIN
# =========================================
st.divider()

st.markdown("""
<div class="titulo-admin">
Acesso Painel Jurídico
</div>
""", unsafe_allow_html=True)

usuario = st.text_input(
    "Usuário"
)

senha = st.text_input(
    "Senha",
    type="password"
)

# =========================================
# BOTÃO LOGIN
# =========================================
if st.button("Entrar no Painel"):

    if (
        usuario == USUARIO
        and senha == SENHA
    ):

        st.session_state["logado"] = True

        st.rerun()

    else:

        st.error(
            "Usuário ou senha inválidos."
        )

# =========================================
# PAINEL
# =========================================
if st.session_state["logado"]:

    st.divider()

    st.markdown("""
    <div class="titulo-admin">
    Painel Jurídico Premium
    </div>
    """, unsafe_allow_html=True)

    # =========================================
    # BOTÃO SAIR
    # =========================================
    if st.button("Sair do Painel"):

        st.session_state["logado"] = False

        st.rerun()

    dados = planilha.get_all_records()

    if dados:

        df = pd.DataFrame(dados)

        df = df.iloc[::-1]

        for i, row in df.iterrows():

            nome_cliente = row.iloc[0]
            email_cliente = row.iloc[1]
            telefone_cliente = str(row.iloc[2])
            caso_cliente = row.iloc[3]
            arquivo_cliente = row.iloc[4]
            data_cliente = row.iloc[5]

            st.markdown(f"""
            <div class="card">

            <div style="
            font-size:30px;
            font-weight:900;
            color:#00d9ff;
            margin-bottom:28px;
            ">
            {nome_cliente}
            </div>

            <div style="
            font-size:24px;
            line-height:2.3;
            font-weight:700;
            color:white;
            ">

            📞 {telefone_cliente}<br><br>

            ✉️ {email_cliente}<br><br>

            ⚖️ {caso_cliente}<br><br>

            🕒 {data_cliente}

            </div>
            """, unsafe_allow_html=True)

            # =========================================
            # ANEXO
            # =========================================
            if arquivo_cliente != "Nenhum arquivo":

                caminho_arquivo = os.path.join(
                    "documentos",
                    arquivo_cliente
                )

                st.markdown(f"""
                <div style="
                margin-top:25px;
                margin-bottom:15px;
                font-size:20px;
                font-weight:800;
                color:#00ff88;
                ">
                📎 {arquivo_cliente}
                </div>
                """, unsafe_allow_html=True)

                if os.path.exists(caminho_arquivo):

                    if arquivo_cliente.lower().endswith(
                        (
                            ".png",
                            ".jpg",
                            ".jpeg"
                        )
                    ):

                        st.image(
                            caminho_arquivo,
                            width=450
                        )

                    with open(
                        caminho_arquivo,
                        "rb"
                    ) as file:

                        st.download_button(
                            label="⬇️ Baixar Anexo",
                            data=file,
                            file_name=arquivo_cliente,
                            key=f"download_{i}"
                        )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

            st.divider()

# =========================================
# FOOTER
# =========================================
st.markdown("""
<div class="footer">
Seus dados estão protegidos e não serão compartilhados.
</div>
""", unsafe_allow_html=True)
