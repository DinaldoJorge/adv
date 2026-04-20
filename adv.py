import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Revisão de Valores",
    page_icon="💰",
    layout="wide"
)

# CSS moderno
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: white;
}
p {
    color: #cfcfcf;
    font-size: 18px;
}
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

# HERO
st.markdown("<h1 style='text-align:center;'>💰 Valores Retroativos para Professores</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Verifique gratuitamente se você pode ter direito à revisão salarial</p>", unsafe_allow_html=True)

st.write("")

# BOTÃO PRINCIPAL
if st.button("🔎 Verificar meu direito agora"):
    st.rerun()

st.write("")

# PROBLEMA
st.markdown("## 📌 Entenda a situação")
st.markdown("""
Professores substitutos podem ter recebido valores inferiores aos professores efetivos em situações semelhantes.

Dependendo do caso, isso pode gerar direito à revisão e recebimento de valores retroativos.
""")

# OPORTUNIDADE
st.markdown("## ⚖️ Possibilidade jurídica")
st.markdown("""
Cada situação deve ser analisada individualmente, com base na legislação e entendimento dos tribunais.

Nossa equipe realiza essa análise de forma técnica e responsável.
""")

# COMO FUNCIONA
st.markdown("## 🚀 Como funciona")
st.markdown("""
1. Você preenche seus dados  
2. Nossa equipe analisa seu caso  
3. Entramos em contato com orientação  

✔ Análise gratuita  
✔ Sem compromisso  
✔ Atendimento rápido  
""")

# FORMULÁRIO
st.markdown("## 📩 Solicitar análise gratuita")

nome = st.text_input("Nome completo")
email = st.text_input("Email")
telefone = st.text_input("Telefone (opcional)")

if st.button("📨 Enviar para análise"):
    if nome and email:
        st.success("✅ Dados enviados! Nossa equipe entrará em contato.")
    else:
        st.error("Preencha nome e email")

# RODAPÉ
st.markdown("---")
st.markdown("""
<p style='text-align:center; font-size:12px; color:gray;'>
Seus dados são tratados com confidencialidade.<br>
Este contato não garante direito ao recebimento, sendo necessária análise individual.<br>
Mouzalas Advogados
</p>
""", unsafe_allow_html=True)
