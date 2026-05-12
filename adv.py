import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="MZA",
    page_icon="💰",
    layout="centered"
)

# =========================================
# CSS PERSONALIZADO
# =========================================
st.markdown("""
<style>

/* FUNDO */
.stApp {
    background-color: black;
}

/* ESCONDE MENU */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* CENTRALIZA LOGO */
.logo-container {
    display: flex;
    justify-content: center;
    margin-top: -20px;
}

/* MELHORA QUALIDADE */
.logo-container img {
    width: 420px;
    max-width: 100%;
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
# LOGO MZA
# =========================================
st.markdown('<div class="logo-container">', unsafe_allow_html=True)

st.image(
    "logomza.png",
    width=420,
    output_format="PNG"
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================
# FORMULÁRIO
# =========================================
nome = st.text_input("Nome completo")
email = st.text_input("Email")
telefone = st.text_input("Telefone")

# =========================================
# SALVAR
# =========================================
def salvar(nome, email, telefone):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    planilha.append_row([nome, email, telefone, data])

# =========================================
# BOTÃO
# =========================================
if st.button("📨 Enviar"):

    if nome and email:

        salvar(nome, email, telefone)

        link = (
            f"https://wa.me/5583991241249"
            f"?text=Olá, sou {nome} e quero verificar valores retroativos"
        )

        st.success("✅ Dados enviados!")

        st.link_button(
            "💬 WhatsApp",
            link
        )

    else:
        st.error("⚠️ Preencha nome e email")
