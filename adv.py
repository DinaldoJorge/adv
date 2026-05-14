import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="MZA",
    page_icon="⚖️",
    layout="wide"
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

/* FONTE */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: white;
}

/* CONTAINER */
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* LOGO */
.logo {
    display: flex;
    justify-content: center;
    margin-top: 5px;
    margin-bottom: 20px;
}

/* FRASE */
.frase {
    text-align: center;
    font-size: 30px;
    font-weight: 500;
    color: white;
    margin-top: 5px;
    margin-bottom: 40px;
}

.frase span {
    color: #00E0B8;
    font-weight: 700;
}

/* INPUTS */
.stTextInput input {

    background: rgba(12,12,12,0.96) !important;

    border: 1.8px solid rgba(0,224,184,0.65) !important;

    border-radius: 12px !important;

    color: white !important;

    font-size: 18px !important;

    height: 50px !important;

    padding-left: 20px !important;
}

/* TEXTAREA */
.stTextArea textarea {

    background: rgba(12,12,12,0.96) !important;

    border: 1.8px solid rgba(0,224,184,0.65) !important;

    border-radius: 14px !important;

    color: white !important;

    font-size: 17px !important;

    padding: 20px !important;

    line-height: 1.7 !important;
}

/* BOTÃO */
.stButton > button {

    background: linear-gradient(
        90deg,
        #00d9b5,
        #00f5c4
    );

    color: black !important;

    font-size: 22px !important;

    font-weight: 700 !important;

    border-radius: 14px !important;

    height: 50px !important;

    width: 100%;

    border: none !important;

    margin-top: 22px;
}

/* CARD */
.card {

    background: linear-gradient(
        145deg,
        #111111,
        #1b1b1b
    );

    border: 1px solid rgba(0,255,208,0.20);

    border-radius: 22px;

    padding: 25px;

    margin-bottom: 22px;

    box-shadow:
        0 0 18px rgba(0,255,208,0.08);
}

/* NOME */
.nome {
    font-size: 28px;
    font-weight: 700;
    color: #00ffd0;
    margin-bottom: 15px;
}

/* INFO */
.info {
    font-size: 17px;
    color: white;
    margin-bottom: 10px;
    line-height: 1.7;
}

/* DATA */
.data {
    color: #8d8d8d;
    font-size: 14px;
    margin-top: 18px;
}

/* TITULO */
.titulo-admin {
    font-size: 36px;
    font-weight: 700;
    color: white;
    margin-top: 30px;
    margin-bottom: 30px;
    text-align: center;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #7f7f7f;
    font-size: 13px;
    margin-top: 25px;
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
    width=420
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
# LAYOUT
# =========================================
col1, col2 = st.columns([1, 1.2])

# =========================================
# FORMULÁRIO
# =========================================
with col1:

    st.subheader("📋 Formulário")

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
        placeholder="Digite seu telefone"
    )

    caso = st.text_area(
        "Caso jurídico",
        placeholder="Explique sua situação jurídica...",
        height=180
    )

    # =========================================
    # SALVAR
    # =========================================
    def salvar(nome, email, telefone, caso):

        data = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        ).strftime("%d/%m/%Y %H:%M")

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
    if st.button("✈️ Enviar Dados"):

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

            st.rerun()

        else:
            st.error("⚠️ Preencha os campos obrigatórios.")

# =========================================
# PAINEL ADMIN
# =========================================
with col2:

    st.markdown("""
    <div class="titulo-admin">
    ⚖️ Painel Jurídico
    </div>
    """, unsafe_allow_html=True)

    dados = planilha.get_all_records()

    if dados:

        df = pd.DataFrame(dados)

        busca = st.text_input(
            "🔍 Pesquisar cliente"
        )

        if busca:

            df = df[
                df.astype(str).apply(
                    lambda x: x.str.contains(
                        busca,
                        case=False
                    )
                ).any(axis=1)
            ]

        st.write(f"📊 Total de clientes: {len(df)}")

        df = df.iloc[::-1]

        for i, row in df.iterrows():

            nome_cliente = row.iloc[0]
            email_cliente = row.iloc[1]
            telefone_cliente = row.iloc[2]
            caso_cliente = row.iloc[3]
            data_cliente = row.iloc[4]

            whatsapp = (
                f"https://wa.me/55"
                f"{telefone_cliente}"
            )

            st.markdown(f"""
            <div class="card">

                <div class="nome">
                👤 {nome_cliente}
                </div>

                <div class="info">
                📞 {telefone_cliente}
                </div>

                <div class="info">
                ✉️ {email_cliente}
                </div>

                <div class="info">
                ⚖️ {caso_cliente}
                </div>

                <div class="data">
                🕒 {data_cliente}
                </div>

            </div>
            """, unsafe_allow_html=True)

            st.link_button(
                "💬 Abrir WhatsApp",
                whatsapp
            )

    else:
        st.warning("Nenhum cliente encontrado.")

# =========================================
# FOOTER
# =========================================
st.markdown("""
<div class="footer">
🔒 Seus dados estão protegidos e não serão compartilhados.
</div>
""", unsafe_allow_html=True)
