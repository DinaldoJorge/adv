import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="Revisão de Valores",
    page_icon="💰",
    layout="centered"
)

# =========================================
# CSS PERSONALIZADO
# =========================================
st.markdown("""
<style>

/* FUNDO GERAL */
.stApp {
    background-color: #000000;
}

/* TEXTOS */
h1, h2, h3, h4, h5, h6, p, label, div {
    color: white !important;
}

/* INPUTS */
.stTextInput > div > div > input {
    background-color: #1e1e1e;
    border: 1px solid #444;
    border-radius: 10px;
    color: white;
    height: 50px;
    font-size: 16px;
}

/* INPUT AO CLICAR */
.stTextInput > div > div > input:focus {
    border: 1px solid #00C9A7 !important;
    box-shadow: 0 0 8px #00C9A7;
}

/* BOTÃO */
.stButton > button {
    background-color: #00C9A7;
    color: black;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    height: 55px;
    width: 100%;
    border: none;
    transition: 0.3s;
}

/* HOVER */
.stButton > button:hover {
    background-color: #00e6bf;
    transform: scale(1.02);
}

/* LOGO */
.logo-container {
    display: flex;
    justify-content: center;
    margin-top: 5px;
    margin-bottom: 25px;
}

/* QUALIDADE DA IMAGEM */
.logo-container img {
    width: 370px;
    max-width: 100%;
    border-radius: 12px;
}

/* RODAPÉ */
.footer {
    font-size: 12px;
    color: #9e9e9e;
    text-align: center;
    margin-top: 35px;
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
# LOGO CENTRALIZADA
# =========================================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(
        "logomza.png",
        width=370,
        output_format="PNG"
    )

# =========================================
# HERO
# =========================================
st.markdown("""
<h1 style='text-align:center; margin-top:10px;'>
💰 Valores Retroativos
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; font-size:18px; color:#d9d9d9;'>
Verifique se você pode ter direito à revisão salarial
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================
# CONTEÚDO
# =========================================
st.markdown("### 📌 Entenda a situação")

st.markdown("""
Professores substitutos podem ter recebido valores inferiores
a professores efetivos em situações semelhantes.
""")

st.markdown("### ⚖️ Possibilidade jurídica")

st.markdown("""
Cada caso deve ser analisado individualmente,
com base na legislação e nos documentos funcionais.
""")

st.markdown("<br>", unsafe_allow_html=True)

# =========================================
# FORMULÁRIO
# =========================================
st.markdown("### 📩 Solicitar análise")

nome = st.text_input("Nome completo")
email = st.text_input("Email")
telefone = st.text_input("Telefone")

# =========================================
# FUNÇÃO SALVAR
# =========================================
def salvar(nome, email, telefone):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    planilha.append_row([nome, email, telefone, data])

# =========================================
# BOTÃO
# =========================================
if st.button("📨 Enviar para análise"):

    if nome and email:

        salvar(nome, email, telefone)

        link = (
            f"https://wa.me/5583991241249"
            f"?text=Olá, sou {nome} e quero verificar valores retroativos"
        )

        st.success("✅ Dados enviados com sucesso!")

        st.link_button(
            "💬 Falar no WhatsApp",
            link
        )

    else:
        st.error("⚠️ Preencha nome e email")

# =========================================
# RODAPÉ
# =========================================
st.markdown("---")

st.markdown("""
<div class="footer">
Seus dados são tratados com confidencialidade.<br>
Este contato não garante direito ao recebimento.<br><br>
Mouzalas Advogados
</div>
""", unsafe_allow_html=True)
