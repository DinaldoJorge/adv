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
# CSS PERSONALIZADO
# =========================================
st.markdown("""
<style>

/* FUNDO */
.stApp {
    background-color: #000000;
}

/* REMOVE MENU */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* TEXTO GERAL */
html, body, [class*="css"] {
    font-family: 'Arial', sans-serif;
    color: white;
}

/* LOGO */
.logo-container {
    display: flex;
    justify-content: center;
    margin-top: 10px;
    margin-bottom: 10px;
}

/* FRASE */
.frase {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    margin-top: 5px;
    margin-bottom: 40px;
    color: white;
}

.frase span {
    color: #00E0B8;
}

/* LABELS */
label {
    color: white !important;
    font-size: 20px !important;
    font-weight: 600 !important;
}

/* INPUTS */
.stTextInput > div > div > input {
    background-color: #0f0f0f;
    border: 2px solid #00E0B8;
    border-radius: 16px;
    color: white !important;
    height: 60px;
    font-size: 20px;
    padding-left: 20px;
}

/* PLACEHOLDER */
.stTextInput input::placeholder {
    color: #9e9e9e;
    font-size: 18px;
}

/* INPUT AO CLICAR */
.stTextInput > div > div > input:focus {
    border: 2px solid #00ffd0 !important;
    box-shadow: 0 0 12px #00ffd0;
}

/* BOTÃO */
.stButton > button {
    background: linear-gradient(90deg, #00d4aa, #00f5c4);
    color: black;
    font-size: 28px;
    font-weight: bold;
    border-radius: 18px;
    height: 70px;
    width: 100%;
    border: none;
    margin-top: 25px;
    transition: 0.3s;
}

/* HOVER */
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px #00f5c4;
}

/* MENSAGEM */
.stSuccess {
    border-radius: 12px;
}

/* RODAPÉ */
.footer {
    text-align: center;
    color: #8f8f8f;
    font-size: 15px;
    margin-top: 30px;
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
# LOGO CENTRALIZADA
# =========================================
st.markdown('<div class="logo-container">', unsafe_allow_html=True)

st.image(
    "logomza.png",
    width=260,
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
    placeholder="Digite seu melhor e-mail"
)

telefone = st.text_input(
    "Telefone",
    placeholder="Digite seu número de telefone"
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
if st.button("📨 Enviar"):

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
