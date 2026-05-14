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

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

.stApp {
    background-color: #050505;
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
    font-size: 40px;
    font-weight: 800;
    color: #FFFFFF;
    margin-top: 5px;
    margin-bottom: 45px;
    text-shadow: 0 0 18px rgba(255,255,255,0.22);
}

.frase span {
    color: #00ffd0;
    font-weight: 900;
}

/* SUBHEADER */
.stSubheader {
    color: white !important;
}

/* LABELS */
label,
.stTextInput label,
.stTextArea label {
    color: #FFFFFF !important;
    font-size: 26px !important;
    font-weight: 900 !important;
    opacity: 1 !important;
    text-shadow: 0 0 12px rgba(255,255,255,0.14);
}

/* INPUTS */
.stTextInput input {

    background: rgba(12,12,12,0.98) !important;

    border: 2px solid rgba(0,255,208,0.75) !important;

    border-radius: 18px !important;

    color: #FFFFFF !important;

    font-size: 26px !important;

    font-weight: 800 !important;

    height: 72px !important;

    padding-left: 24px !important;

    box-shadow:
        0 0 22px rgba(0,255,208,0.10);
}

/* PLACEHOLDER */
.stTextInput input::placeholder {
    color: #FFFFFF !important;
    opacity: 0.82 !important;
    font-size: 23px !important;
    font-weight: 700 !important;
}

/* TEXTAREA */
.stTextArea textarea {

    background: rgba(12,12,12,0.98) !important;

    border: 2px solid rgba(0,255,208,0.75) !important;

    border-radius: 20px !important;

    color: #FFFFFF !important;

    font-size: 26px !important;

    font-weight: 700 !important;

    padding: 26px !important;

    line-height: 1.9 !important;

    box-shadow:
        0 0 22px rgba(0,255,208,0.10);
}

/* PLACEHOLDER TEXTAREA */
.stTextArea textarea::placeholder {
    color: #FFFFFF !important;
    opacity: 0.82 !important;
    font-size: 23px !important;
    font-weight: 700 !important;
}

/* FOCO */
.stTextInput input:focus,
.stTextArea textarea:focus {

    border: 2px solid #00ffd0 !important;

    box-shadow:
        0 0 30px rgba(0,255,208,0.34);
}

/* BOTÕES */
.stButton > button {

    background: linear-gradient(
        90deg,
        #00e0b8,
        #00ffd0
    );

    color: #000000 !important;

    font-size: 28px !important;

    font-weight: 900 !important;

    border-radius: 20px !important;

    height: 68px !important;

    width: 100%;

    border: none !important;

    margin-top: 22px;

    transition: 0.3s ease;

    box-shadow:
        0 0 28px rgba(0,255,208,0.24);
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 40px rgba(0,255,208,0.45);
}

/* TITULO ADMIN */
.titulo-admin {
    font-size: 52px;
    font-weight: 900;
    text-align: center;
    margin-top: 35px;
    margin-bottom: 35px;
    color: white;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #f0f0f0;
    font-size: 20px;
    font-weight: 700;
    margin-top: 35px;
}

/* ALERTAS */
.stSuccess,
.stError,
.stWarning {
    font-size: 22px !important;
    font-weight: 800 !important;
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
    height=240
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

        st.markdown(f"""
        <div style="
        font-size:30px;
        font-weight:900;
        color:white;
        margin-bottom:30px;
        text-shadow:0 0 12px rgba(255,255,255,0.18);
        ">
        📊 Total de clientes: {len(df)}
        </div>
        """, unsafe_allow_html=True)

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
            padding:40px;
            border-radius:30px;
            margin-bottom:40px;
            border:2px solid rgba(0,255,208,0.25);
            box-shadow:
            0 0 36px rgba(0,255,208,0.10);
            ">

            <div style="
            display:flex;
            align-items:center;
            gap:22px;
            margin-bottom:34px;
            ">

            <div style="
            font-size:60px;
            ">
            👤
            </div>

            <div style="
            font-size:58px;
            font-weight:900;
            color:#00ffd0;
            line-height:1;
            text-shadow:0 0 20px rgba(0,255,208,0.22);
            ">
            {nome_cliente}
            </div>

            </div>

            <div style="
            background:#050505;
            padding:28px;
            border-radius:24px;
            margin-bottom:24px;
            border-left:8px solid #00ffd0;
            ">

            <div style="
            font-size:30px;
            font-weight:900;
            color:#FFFFFF;
            margin-bottom:14px;
            ">
            📞 Telefone:
            </div>

            <div style="
            font-size:54px;
            font-weight:900;
            color:#FFFFFF;
            letter-spacing:1px;
            text-shadow:0 0 14px rgba(255,255,255,0.12);
            ">
            {telefone_cliente}
            </div>

            </div>

            <div style="
            background:#050505;
            padding:28px;
            border-radius:24px;
            margin-bottom:24px;
            border-left:8px solid #00ffd0;
            ">

            <div style="
            font-size:30px;
            font-weight:900;
            color:#FFFFFF;
            margin-bottom:14px;
            ">
            ✉️ Email:
            </div>

            <div style="
            font-size:46px;
            font-weight:900;
            color:#FFFFFF;
            text-shadow:0 0 14px rgba(255,255,255,0.12);
            ">
            {email_cliente}
            </div>

            </div>

            <div style="
            background:#050505;
            padding:30px;
            border-radius:24px;
            margin-top:18px;
            margin-bottom:24px;
            border-left:8px solid #00ffd0;
            ">

            <div style="
            font-size:32px;
            font-weight:900;
            color:#FFFFFF;
            margin-bottom:22px;
            ">
            ⚖️ Caso Jurídico
            </div>

            <div style="
            font-size:36px;
            font-weight:800;
            color:#FFFFFF;
            line-height:1.8;
            text-shadow:0 0 14px rgba(255,255,255,0.10);
            ">
            {caso_cliente}
            </div>

            </div>

            <div style="
            color:#FFFFFF;
            font-size:26px;
            font-weight:800;
            margin-top:14px;
            opacity:0.92;
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
