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
# CSS PREMIUM
# =========================================
st.markdown("""
<style>

/* FUNDO */
.stApp {
    background-color: #050505;
}

/* REMOVE MENU */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* CONTAINER */
.block-container {
    max-width: 470px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* FONTE */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: white;
}
/* LOGO */
.logo {

    width: 100%;

    display: flex;

    justify-content: center;

    align-items: center;

    text-align: center;

    margin-top: 5px;

    margin-bottom: 15px;
}

/* CENTRALIZA A IMAGEM */
.logo img {

    display: block;

    margin-left: auto;

    margin-right: auto;
}

/* FRASE */
.frase {
    text-align: center;
    font-size: 25px;
    font-weight: 500;
    color: white;
    margin-top: 5px;
    margin-bottom: 45px;
}

.frase span {
    color: #00E0B8;
    font-weight: 700;
}

/* LABELS */
label {
    color: white !important;
    font-size: 10px !important;
    font-weight: 600 !important;
}

/* INPUTS */
.stTextInput input {

    background: rgba(12,12,12,0.96) !important;

    border: 1.8px solid rgba(0,224,184,0.65) !important;

    border-radius: 10px !important;

    color: white !important;

    font-size: 19px !important;

    font-weight: 400 !important;

    height: 32px !important;

    padding-left: 20px !important;

    padding-right: 20px !important;

    padding-top: 20px !important;

    padding-bottom: 20px !important;

    transition: 0.3s ease;

    box-sizing: border-box !important;

    box-shadow:
        0 0 10px rgba(0,224,184,0.08);
}

/* TEXTAREA */
.stTextArea textarea {

    background: rgba(12,12,12,0.96) !important;

    border: 1.8px solid rgba(0,224,184,0.65) !important;

    border-radius: 14px !important;

    color: white !important;

    font-size: 17px !important;

    font-weight: 400 !important;

    padding: 20px !important;

    line-height: 1.7 !important;

    transition: 0.3s ease;

    box-sizing: border-box !important;

    box-shadow:
        0 0 10px rgba(0,224,184,0.08);
}

/* PLACEHOLDER */
input::placeholder,
textarea::placeholder {

    color: #9f9f9f !important;

    opacity: 1 !important;

    font-size: 17px !important;

    line-height: normal !important;
}

/* FOCO */
.stTextInput input:focus,
.stTextArea textarea:focus {

    border: 2px solid #00ffd0 !important;

    box-shadow:
        0 0 15px rgba(0,255,208,0.25),
        0 0 25px rgba(0,255,208,0.08) !important;
}

/* BOTÃO */
.stButton > button {

    background: linear-gradient(
        90deg,
        #00d9b5,
        #00f5c4
    );

    color: black !important;

    font-size: 24px !important;

    font-weight: 700 !important;

    border-radius: 14px !important;

    height: 64px !important;

    width: 100%;

    border: none !important;

    margin-top: 28px;

    transition: all 0.3s ease;

    box-shadow:
        0 0 18px rgba(0,245,196,0.20);
}

/* HOVER */
.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 25px rgba(0,255,208,0.35),
        0 0 40px rgba(0,255,208,0.12);
}

/* ESPAÇAMENTO */
div[data-baseweb="input"] {
    margin-bottom: 22px;
}

/* RODAPÉ */
.footer {
    text-align: center;
    color: #7f7f7f;
    font-size: 13px;
    margin-top: 25px;
    line-height: 1.7;
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
    width=220,
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
if st.button("✈️  Enviar"):

    if nome and email and caso:

        salvar(nome, email, telefone, caso)

        link = (
            f"https://wa.me/5583991241249"
            f"?text=Olá, sou {nome} e desejo uma análise jurídica."
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
🔒 Seus dados estão protegidos e não serão compartilhados.
</div>
""", unsafe_allow_html=True)
