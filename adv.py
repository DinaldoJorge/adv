import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# CONFIG
st.set_page_config(page_title="Revisão de Valores", page_icon="💰", layout="wide")

# CSS
st.markdown("""
<style>
.main {background-color: #0e1117;}
h1, h2, h3 {color: white;}
p {color: #cfcfcf; font-size: 18px;}
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

# CONEXÃO GOOGLE SHEETS
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
client = gspread.authorize(creds)

planilha = client.open("leads_professores").sheet1

# HERO
st.markdown("<h1 style='text-align:center;'>💰 Valores Retroativos para Professores</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Verifique gratuitamente se você pode ter direito à revisão salarial</p>", unsafe_allow_html=True)

# CONTEÚDO
st.markdown("## 📌 Entenda a situação")
st.markdown("""
Professores substitutos podem ter recebido valores inferiores aos professores efetivos.
""")

st.markdown("## ⚖️ Possibilidade jurídica")
st.markdown("""
Cada caso deve ser analisado individualmente.
""")

# FORM
st.markdown("## 📩 Solicitar análise gratuita")

nome = st.text_input("Nome completo")
email = st.text_input("Email")
telefone = st.text_input("Telefone")

# FUNÇÃO SALVAR
def salvar(nome, email, telefone):
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    planilha.append_row([nome, email, telefone, data])

# ENVIO
if st.button("📨 Enviar para análise"):
    if nome and email:
        salvar(nome, email, telefone)

        # LINK WHATSAPP
        link = f"https://wa.me/5583SEUNUMERO?text=Olá, sou {nome} e quero verificar valores retroativos"

        st.success("✅ Dados enviados com sucesso!")
        st.link_button("💬 Falar no WhatsApp", link)

    else:
        st.error("Preencha nome e email")

# RODAPÉ
st.markdown("---")
st.markdown("""
<p style='text-align:center; font-size:12px; color:gray;'>
Seus dados são confidenciais.<br>
Mouzalas Advogados
</p>
""", unsafe_allow_html=True)
Seus dados são tratados com confidencialidade.<br>
Este contato não garante direito ao recebimento, sendo necessária análise individual.<br>
Mouzalas Advogados
</p>
""", unsafe_allow_html=True)
