import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="MZA",
    page_icon="⚖️",
    layout="centered"
)

# =========================================
# CSS MELHORADO
# =========================================
st.markdown("""
<style>

/* FUNDO */
.stApp {
    background-color: #000000;
}

/* REMOVE ELEMENTOS */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* CENTRALIZA CONTEÚDO */
.block-container {
    max-width: 520px;
    padding-top: 1rem;
}

/* FONTE */
html, body, [class*="css"] {
    font-family: Arial, sans-serif;
    color: white;
}

/* LOGO */
.logo {
    display: flex;
    justify-content: center;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* FRASE */
.frase {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 40px;
    color: white;
}

.frase span {
    color: #00E0B8;
}

/* LABELS */
label {
    color: white !important;
    font-size: 19px !important;
    font-weight: bold !important;
}

/* INPUTS */
.stTextInput input {
    background-color: #0a0a0a !important;
    border: 2px solid #00E0B8 !important;
    border-radius: 14px !important;
    color: white !important;
    font-size: 20px !important;
    height: 60px !important;
    padding-left: 18px !important;
}

/* TEXTAREA */
.stTextArea textarea {
    background-color: #0a0a0a !important;
    border: 2px solid #00E0B8 !important;
    border-radius: 14px !important;
    color: white !important;
    font-size: 18px !important;
    padding: 18px !important;
}

/* PLACEHOLDER */
input::placeholder,
textarea::placeholder {
    color: #a5a5a5 !important;
    opacity: 1 !important;
    font-size: 18px !important;
}

/* FOCO */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border: 2px solid #00ffd0 !important;
    box-shadow: 0 0 12px #00ffd0 !important;
}

/* BOTÃO */
.stButton > button {
    background: linear-gradient(90deg, #00d9b5, #00f5c4);
    color: black !important;
    font-size: 26px !important;
    font-weight: bold !important;
    border-radius: 16px !important;
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
    color: #8d8d8d;
    font-size: 14px;
    margin-top: 25px;
    line-height: 1.8;
}

/* ESPAÇAMENTO */
div[data-baseweb="input"] {
    margin-bottom: 20px;
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
st.markdown('<div class="logo">', unsafe_allow_html=True)

st.image(
    "logomza.png",
    width=230,
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

caso = st.text_area(
    "Escreva seu caso jurídico para análise",
    placeholder="Explique sua dúvida ou situação jurídica...",
    height=180
)

# =========================================
# FUNÇÃO SALVAR
# =========================================
def salvar(nome, email, telefone, caso):

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    planilha.append_row([
        nome,
        email,
        telefone,
        caso,
        data
    ])

# =========================================
# BOTÃO
# =========================================
if st.button("📨 Enviar para análise"):

    if nome and email and caso:

        salvar(nome, email, telefone, caso)

        link = (
            f"https://wa.me/5583991241249"
            f"?text=Olá, sou {nome} e desejo análise jurídica."
        )

        st.success("✅ Dados enviados com sucesso!")

        st.link_button(
            "💬 Falar no WhatsApp",
            link
        )

    else:
        st.error("⚠️ Preencha os campos obrigatórios.")

# =========================================
# RODAPÉ
# =========================================
st.markdown("""
<div class="footer">
🔒 Seus dados estão protegidos e não serão compartilhados.<br>
Mouzalas Advogados
</div>
""", unsafe_allow_html=True)
