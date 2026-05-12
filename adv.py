import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="MZA",
    page_icon="💼",
    layout="centered"
)

# =========================================
# CSS
# =========================================
st.markdown("""
<style>

/* FUNDO */
.stApp {
    background-color: #050505;
}

/* REMOVE ELEMENTOS */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* FONTE */
html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

/* CONTAINER CENTRAL */
.block-container {
    max-width: 430px;
    padding-top: 1rem;
    padding-bottom: 1rem;
}

/* LOGO */
.logo {
    text-align: center;
    margin-top: 10px;
    margin-bottom: 10px;
}

/* FRASE */
.frase {
    text-align: center;
    color: white;
    font-size: 20px;
    margin-top: 5px;
    margin-bottom: 35px;
    font-weight: 500;
}

.frase span {
    color: #00E0B8;
    font-weight: bold;
}

/* LABELS */
label {
    color: white !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* INPUTS */
.stTextInput > div > div > input {
    background-color: #0d0d0d !important;
    border: 1.8px solid #00C9A7 !important;
    border-radius: 14px !important;
    color: white !important;
    height: 58px !important;
    font-size: 18px !important;
    padding-left: 18px !important;
}

/* PLACEHOLDER */
.stTextInput input::placeholder {
    color: #8d8d8d !important;
    font-size: 17px !important;
}

/* FOCO */
.stTextInput > div > div > input:focus {
    border: 2px solid #00ffd0 !important;
    box-shadow: 0 0 10px #00ffd0 !important;
}

/* BOTÃO */
.stButton > button {
    background: linear-gradient(90deg, #00d9b5, #00f2c9);
    color: black !important;
    font-size: 28px !important;
    font-weight: bold !important;
    border-radius: 14px !important;
    height: 68px !important;
    width: 100%;
    border: none !important;
    margin-top: 25px;
    transition: 0.3s;
}

/* HOVER */
.stButton > button:hover {
    transform: scale(1.01);
    box-shadow: 0 0 20px #00ffd0;
}

/* RODAPÉ */
.footer {
    text-align: center;
    color: #7e7e7e;
    font-size: 13px;
    margin-top: 18px;
}

/* ESPAÇAMENTO */
div[data-baseweb="input"] {
    margin-bottom: 18px;
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
st.markdown('<div class="logo">', unsafe_allow_html=True)

st.image(
    "logomza.png",
    width=190,
    output_format="PNG"
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# FRASE
# =========================================
st.markdown("""
<div class="frase">
🛡️ Vamos <span>analisar</span> seus dados
</div>
""", unsafe_allow_html=True)

# =========================================
# FORMULÁRIO
# =========================================
nome = st.text_input(
    "Nome completo",
    placeholder="Digite seu nome completo"
)

email = st.text_input(
    "Email",
    placeholder="✉️   Digite seu melhor e-mail"
)

telefone = st.text_input(
    "Telefone",
    placeholder="📞   Digite seu número de telefone"
)

# =========================================
# FUNÇÃO SALVAR
# =========================================
def salvar(nome, email, telefone):

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    planilha.append_row([
        nome,
        email,
        telefone,
        data
    ])

# =========================================
# BOTÃO
# =========================================
if st.button("✈️  Enviar"):

    if nome and email:

        salvar(nome, email, telefone)

        link = (
            f"https://wa.me/5583991241249"
            f"?text=Olá, sou {nome} e desejo analisar meus dados."
        )

        st.success("✅ Dados enviados com sucesso!")

        st.link_button(
            "💬 Falar no WhatsApp",
            link
        )

    else:
        st.error("⚠️ Preencha nome e email.")

# =========================================
# RODAPÉ
# =========================================
st.markdown("""
<div class="footer">
🔒 Seus dados estão protegidos e não serão compartilhados.
</div>
""", unsafe_allow_html=True)
