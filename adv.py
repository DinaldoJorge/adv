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
# CSS MODERNO
# =========================================
st.markdown("""
<style>

/* FUNDO */
.stApp {
    background: #000000;
}

/* REMOVE MENU */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* CENTRALIZA CONTEÚDO */
.block-container {
    max-width: 560px;
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
    display: flex;
    justify-content: center;
    margin-top: 10px;
    margin-bottom: 10px;
}

/* FRASE */
.frase {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
    color: white;
    margin-top: 10px;
    margin-bottom: 45px;
}

.frase span {
    color: #00E0B8;
}

/* LABELS */
label {
    color: #ffffff !important;
    font-size: 20px !important;
    font-weight: 700 !important;
}

/* INPUTS */
.stTextInput input {

    background: rgba(12,12,12,0.96) !important;

    border: 2px solid rgba(0,224,184,0.75) !important;

    border-radius: 18px !important;

    color: white !important;

    font-size: 22px !important;

    font-weight: 500 !important;

    height: 68px !important;

    padding-left: 22px !important;

    transition: 0.3s ease;

    box-shadow:
        0 0 12px rgba(0,224,184,0.10);
}

/* TEXTAREA */
.stTextArea textarea {

    background: rgba(12,12,12,0.96) !important;

    border: 2px solid rgba(0,224,184,0.75) !important;

    border-radius: 20px !important;

    color: white !important;

    font-size: 21px !important;

    font-weight: 500 !important;

    padding: 22px !important;

    line-height: 1.7 !important;

    transition: 0.3s ease;

    box-shadow:
        0 0 12px rgba(0,224,184,0.10);
}

/* PLACEHOLDER */
input::placeholder,
textarea::placeholder {

    color: #b0b0b0 !important;

    opacity: 1 !important;

    font-size: 20px !important;
}

/* FOCO */
.stTextInput input:focus,
.stTextArea textarea:focus {

    border: 2px solid #00ffd0 !important;

    box-shadow:
        0 0 18px rgba(0,255,208,0.35),
        0 0 35px rgba(0,255,208,0.12) !important;

    transform: scale(1.01);
}

/* BOTÃO */
.stButton > button {

    background: linear-gradient(
        90deg,
        #00d9b5,
        #00f5c4
    );

    color: black !important;

    font-size: 28px !important;

    font-weight: 800 !important;

    border-radius: 18px !important;

    height: 74px !important;

    width: 100%;

    border: none !important;

    margin-top: 30px;

    transition: all 0.3s ease;

    box-shadow:
        0 0 20px rgba(0,245,196,0.25);
}

/* HOVER */
.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 28px rgba(0,255,208,0.45),
        0 0 50px rgba(0,255,208,0.18);
}

/* ESPAÇAMENTO */
div[data-baseweb="input"] {
    margin-bottom: 24px;
}

/* RODAPÉ */
.footer {
    text-align: center;
    color: #8d8d8d;
    font-size: 15px;
    margin-top: 30px;
    line-height: 1.8;
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
    placeholder="Digite seu melhor e-mail"
)

telefone = st.text_input(
    "Telefone",
    placeholder="Digite seu número de telefone"
)

caso = st.text_area(
    "Escreva seu caso jurídico para análise",
    placeholder="Explique sua dúvida ou situação jurídica...",
    height=220
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
🔒 Seus dados estão protegidos e não serão compartilhados.<br>
Mouzalas Advogados
</div>
""", unsafe_allow_html=True)
