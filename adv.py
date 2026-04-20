import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Revisão de Valores",
    page_icon="💰",
    layout="centered"
)

# CSS (FUNDO BRANCO + INPUT MELHORADO)
st.markdown("""
<style>
.main {
    background-color: white;
}

h1, h2, h3 {
    color: #222;
    text-align: center;
}

p {
    color: #444;
    font-size: 18px;
    text-align: center;
}

/* INPUT MAIS ESCURO E VISÍVEL */
.stTextInput > div > div > input {
    background-color: #e0e0e0;
    border: 1px solid #bdbdbd;
    border-radius: 8px;
    color: #000;
}

/* EFEITO AO CLICAR */
.stTextInput > div > div > input:focus {
    border: 1px solid #00C9A7;
    background-color: #e8fdf8;
}

/* BOTÃO */
.stButton>button {
    background-color: #00C9A7;
    color: black;
    font-size: 18px;
    border-radius: 10px;
    height: 50px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# 🔐 CONEXÃO COM GOOGLE SHEETS
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)

client = gspread.authorize(creds)
planilha = client.open("leads_professores").sheet1

# 🖼️ IMAGEM NO TOPO
st.image("logomza.png", use_container_width=True)

# HERO
st.markdown("## 💰 Valores Retroativos")
st.markdown("Verifique se você pode ter direito à revisão salarial")

# CONTEÚDO
st.markdown("### 📌 Entenda a situação")
st.markdown("""
Professores substitutos podem ter recebido valores inferiores aos professores efetivos em situações semelhantes.
""")

st.markdown("### ⚖️ Possibilidade jurídica")
st.markdown("""
Cada caso deve ser analisado individualmente, com base na legislação.
""")

# FORMULÁRIO
st.markdown("### 📩 Solicitar análise")

nome = st.text_input("Nome completo")
email = st.text_input("Email")
telefone = st.text_input("Telefone")

# FUNÇÃO PARA SALVAR
def salvar(nome, email, telefone):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    planilha.append_row([nome, email, telefone, data])

# BOTÃO
if st.button("📨 Enviar para análise"):
    if nome and email:
        salvar(nome, email, telefone)

        link = f"https://wa.me/5583991241249?text=Olá, sou {nome} e quero verificar valores retroativos"

        st.success("✅ Dados enviados com sucesso!")
        st.link_button("💬 Falar no WhatsApp", link)
    else:
        st.error("Preencha nome e email")

# RODAPÉ
st.markdown("---")
st.markdown("""
<p style='font-size:12px; color:gray; text-align:center;'>
Seus dados são tratados com confidencialidade.<br>
Este contato não garante direito ao recebimento.<br>
Mouzalas Advogados
</p>
""", unsafe_allow_html=True)
