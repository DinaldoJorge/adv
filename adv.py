import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# =========================================
# CONFIGURAÇÃO
# =========================================
st.set_page_config(
    page_title="MZA",
    page_icon="⚖️",
    layout="wide"
)

# =========================================
# LOGIN
# =========================================
USUARIO = "admin"
SENHA = "mza2026"

if "logado" not in st.session_state:
    st.session_state.logado = False

# =========================================
# CSS PREMIUM
# =========================================
st.markdown("""
<style>

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
    max-width: 1450px;
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
    font-size: 32px;
    font-weight: 500;
    color: white;
    margin-top: 5px;
    margin-bottom: 40px;
}

.frase span {
    color: #00ffd0;
    font-weight: 800;
}

/* INPUTS */
.stTextInput input {

    background: rgba(12,12,12,0.96) !important;

    border: 1.8px solid rgba(0,224,184,0.65) !important;

    border-radius: 14px !important;

    color: white !important;

    font-size: 18px !important;

    height: 54px !important;

    padding-left: 20px !important;

    box-shadow:
        0 0 10px rgba(0,255,208,0.05);
}

/* TEXTAREA */
.stTextArea textarea {

    background: rgba(12,12,12,0.96) !important;

    border: 1.8px solid rgba(0,224,184,0.65) !important;

    border-radius: 16px !important;

    color: white !important;

    font-size: 18px !important;

    padding: 22px !important;

    line-height: 1.8 !important;
}

/* FOCO */
.stTextInput input:focus,
.stTextArea textarea:focus {

    border: 2px solid #00ffd0 !important;

    box-shadow:
        0 0 20px rgba(0,255,208,0.25);
}

/* BOTÕES */
.stButton > button {

    background: linear-gradient(
        90deg,
        #00e0b8,
        #00ffd0
    );

    color: black !important;

    font-size: 22px !important;

    font-weight: 800 !important;

    border-radius: 16px !important;

    height: 56px !important;

    width: 100%;

    border: none !important;

    margin-top: 18px;

    transition: 0.3s ease;

    box-shadow:
        0 0 20px rgba(0,255,208,0.18);
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 35px rgba(0,255,208,0.35);
}

/* TITULO */
.titulo-admin {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-top: 35px;
    margin-bottom: 35px;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #8d8d8d;
    font-size: 13px;
    margin-top: 35px;
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
    width=430
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
    height=200
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
# ENVIAR
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

    else:
        st.error("⚠️ Preencha os campos obrigatórios.")

# =========================================
# LOGIN ADMIN
# =========================================
st.divider()

st.markdown("""
<div class="titulo-admin">
🔐 Acesso Painel Jurídico
</div>
""", unsafe_allow_html=True)

usuario_input = st.text_input(
    "Usuário"
)

senha_input = st.text_input(
    "Senha",
    type="password"
)

if st.button("🚪 Entrar no Painel"):

    if (
        usuario_input == USUARIO
        and senha_input == SENHA
    ):

        st.session_state.logado = True
        st.success("✅ Login realizado!")
        st.rerun()

    else:
        st.error("❌ Usuário ou senha inválidos.")

# =========================================
# PAINEL JURÍDICO
# =========================================
if st.session_state.logado:

    st.divider()

    st.markdown("""
    <div class="titulo-admin">
    ⚖️ Painel Jurídico Premium
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Sair do Painel"):

        st.session_state.logado = False
        st.rerun()

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
            telefone_cliente = str(row.iloc[2])
            caso_cliente = row.iloc[3]
            data_cliente = row.iloc[4]

            telefone_limpo = ''.join(
                filter(str.isdigit, telefone_cliente)
            )

            whatsapp = (
                f"https://wa.me/55{telefone_limpo}"
            )

            st.markdown(f"""
            <div style="
            background: linear-gradient(145deg,#0f0f0f,#161616);
            padding:35px;
            border-radius:28px;
            margin-bottom:35px;
            border:1px solid rgba(0,255,208,0.25);
            box-shadow:
            0 0 30px rgba(0,255,208,0.08);
            ">

            <div style="
            display:flex;
            align-items:center;
            gap:18px;
            margin-bottom:28px;
            ">

            <div style="
            font-size:52px;
            ">
            👤
            </div>

            <div style="
            font-size:52px;
            font-weight:900;
            color:#00ffd0;
            line-height:1;
            ">
            {nome_cliente}
            </div>

            </div>

            <div style="
            background:#050505;
            padding:22px;
            border-radius:20px;
            margin-bottom:18px;
            border-left:6px solid #00ffd0;
            ">

            <div style="
            font-size:24px;
            font-weight:800;
            color:white;
            margin-bottom:12px;
            ">
            📞 Telefone:
            </div>

            <div style="
            font-size:48px;
            font-weight:900;
            color:white;
            letter-spacing:1px;
            ">
            {telefone_cliente}
            </div>

            </div>

            <div style="
            background:#050505;
            padding:22px;
            border-radius:20px;
            margin-bottom:18px;
            border-left:6px solid #00ffd0;
            ">

            <div style="
            font-size:24px;
            font-weight:800;
            color:white;
            margin-bottom:12px;
            ">
            ✉️ Email:
            </div>

            <div style="
            font-size:42px;
            font-weight:800;
            color:white;
            ">
            {email_cliente}
            </div>

            </div>

            <div style="
            background:#050505;
            padding:25px;
            border-radius:20px;
            margin-top:18px;
            margin-bottom:22px;
            border-left:6px solid #00ffd0;
            ">

            <div style="
            font-size:24px;
            font-weight:800;
            color:white;
            margin-bottom:18px;
            ">
            ⚖️ Caso Jurídico
            </div>

            <div style="
            font-size:46px;
            font-weight:700;
            color:white;
            line-height:1.5;
            ">
            {caso_cliente}
            </div>

            </div>

            <div style="
            color:#d0d0d0;
            font-size:24px;
            font-weight:700;
            margin-top:12px;
            ">
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
