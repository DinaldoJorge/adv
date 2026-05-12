import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="MZA",
    page_icon="💼",
    layout="centered"
)

# =====================================================
# CSS PERSONALIZADO
# =====================================================
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

/* TEXTO */
html, body, [class*="css"] {
    color: white;
    font-family: 'Segoe UI', sans-serif;
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
    font-size: 34px;
    font-weight: 700;
    margin-top: 15px;
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
    background-color: #111111 !important;
    color: white !important;
    border: 2px solid #00C9A7 !important;
    border-radius: 16px !important;
    padding-left: 15px !important;
    height: 60px !important;
    font-size: 20px !important;
    transition: 0.3s;
}

/* PLACEHOLDER */
.stTextInput input::placeholder {
    color: #9e9e9e !important;
    font-size: 18px !important;
}

/* INPUT FOCUS */
.stTextInput > div > div > input:focus {
    border: 2px solid #00FFD0 !important;
    box-shadow: 0 0 15px #00FFD0 !important;
}

/* BOTÃO */
.stButton > button {
    width: 100%;
    height: 65px;
    border-radius: 18px;
    border: none;
    background: linear-gradient(90deg, #00D9B0, #00F0C0);
    color: black;
    font-size: 26px;
    font-weight: bold;
    margin-top: 20px;
    transition: 0.3s;
}

/* HOVER */
.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #00F0C0, #00D9B0);
}

/* RODAPÉ */
.footer {
    text-align: center;
    color: #8c8c8c;
    font-size: 15px;
    margin-top: 25px;
    line-height: 1.8;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEETS
# =====================================================
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

# =====================================================
# LOGO CENTRALIZADA
# =====================================================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "logomza.png",
        width=230,
        output_format="PNG"
    )

# =====================================================
# FRASE
# =====================================================
st.markdown("""
<div class="frase">
🛡️ Vamos <span>analisar</span> seus dados
</div>
""", unsafe_allow_html=True)

# =====================================================
# CAMPOS
# =====================================================
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

# =====================================================
# FUNÇÃO SALVAR
# =====================================================
def salvar(nome, email, telefone):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    planilha.append_row([nome, email, telefone, data])

# =====================================================
# BOTÃO
# =====================================================
if st.button("✈️ Enviar"):

    if nome and email:

        salvar(nome, email, telefone)

        link = (
            f"https://wa.me/5583991241249"
            f"?text=Olá, sou {nome} e quero analisar meus dados."
        )

        st.success("✅ Dados enviados com sucesso!")

        st.link_button(
            "💬 Abrir WhatsApp",
            link
        )

    else:
        st.error("⚠️ Preencha nome e email")

# =====================================================
# RODAPÉ
# =====================================================
st.markdown("""
<div class="footer">
🔒 Seus dados estão protegidos e não serão compartilhados.
</div>
""", unsafe_allow_html=True)
