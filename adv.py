import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os

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

if "limpar_login" not in st.session_state:
    st.session_state.limpar_login = False

# =========================================
# LIMPA CAMPOS LOGIN
# =========================================
if st.session_state.limpar_login:

    st.session_state["usuario"] = ""
    st.session_state["senha"] = ""

    st.session_state.limpar_login = False

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
    max-width: 1200px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* FRASE */
.frase {
    text-align: center;
    font-size: 22px;
    font-weight: 900;
    color: #FFFFFF;
    margin-top: 5px;
    margin-bottom: 45px;
    text-shadow: 0 0 20px rgba(255,255,255,0.22);
}

.frase span {
    color: #00ffd0;
    font-weight: 900;
}

/* LABELS */
label,
.stTextInput label,
.stTextArea label {

    color: #FFFFFF !important;

    font-size: 22px !important;

    font-weight: 900 !important;

    opacity: 1 !important;

    letter-spacing: 0.5px;

    text-shadow:
        0 0 18px rgba(255,255,255,0.22);
}

/* INPUTS */
.stTextInput input {

    background: rgba(12,12,12,0.98) !important;

    border: 2px solid rgba(0,255,208,0.75) !important;

    border-radius: 15px !important;

    color: #FFFFFF !important;

    font-size: 20px !important;

    font-weight: 800 !important;

    height: 47px !important;

    padding-left: 28px !important;

    box-shadow:
        0 0 26px rgba(0,255,208,0.12);
}

/* PLACEHOLDER */
.stTextInput input::placeholder {

    color: #FFFFFF !important;

    opacity: 3 !important;

    font-size: 20px !important;

    font-weight: 700 !important;
}

/* TEXTAREA */
.stTextArea textarea {

    background: rgba(12,12,12,0.98) !important;

    border: 2px solid rgba(0,255,208,0.75) !important;

    border-radius: 22px !important;

    color: #FFFFFF !important;

    font-size: 22px !important;

    font-weight: 700 !important;

    padding: 30px !important;

    line-height: 1.9 !important;

    box-shadow:
        0 0 26px rgba(0,255,208,0.12);
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {

    background: rgba(12,12,12,0.98);

    border: 2px solid rgba(0,255,208,0.75);

    border-radius: 22px;

    padding: 20px;

    box-shadow:
        0 0 26px rgba(0,255,208,0.12);

    margin-top: 15px;
}

/* BOTÕES */
.stButton > button {

    background: linear-gradient(
        90deg,
        #00e0b8,
        #00ffd0
    );

    color: #000000 !important;

    font-size: 20px !important;

    font-weight: 900 !important;

    border-radius: 22px !important;

    height: 50px !important;

    width: 100%;

    border: none !important;

    margin-top: 24px;

    transition: 0.3s ease;

    box-shadow:
        0 0 30px rgba(0,255,208,0.24);
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 42px rgba(0,255,208,0.45);
}

/* TITULO ADMIN */
.titulo-admin {

    font-size: 22px;

    font-weight: 900;

    text-align: center;

    margin-top: 20px;

    margin-bottom: 20px;

    color: white;

    text-shadow: 0 0 12px rgba(255,255,255,0.18);
}

/* FOOTER */
.footer {

    text-align: center;

    color: #f0f0f0;

    font-size: 12px;

    font-weight: 400;

    margin-top: 30px;
}

.card {

    background: linear-gradient(145deg,#0f0f0f,#161616);

    padding:42px;

    border-radius:32px;

    margin-bottom:42px;

    border:2px solid rgba(0,255,208,0.25);

    box-shadow:
    0 0 38px rgba(0,255,208,0.10);
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
col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.image(
        "logomza.png",
        width=300
    )

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
with st.form("formulario_cliente", clear_on_submit=True):

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
        height=260
    )

    # =========================================
    # ANEXO
    # =========================================
    arquivo = st.file_uploader(
        "📎 Anexar documentos (máx. 5MB)",
        type=[
            "pdf",
            "doc",
            "docx",
            "txt",
            "png",
            "jpg",
            "jpeg"
        ]
    )

    enviar = st.form_submit_button("✈️ Enviar Dados")

# =========================================
# SALVAR
# =========================================
def salvar(nome, email, telefone, caso, nome_arquivo):

    data = datetime.now(
        ZoneInfo("America/Sao_Paulo")
    ).strftime("%d/%m/%Y %H:%M")

    planilha.append_row([
        nome,
        email,
        telefone,
        caso,
        nome_arquivo,
        data
    ])

# =========================================
# ENVIO
# =========================================
if enviar:

    if nome and email and caso:

        nome_arquivo = "Nenhum arquivo"

        if arquivo is not None:

            tamanho_mb = arquivo.size / (1024 * 1024)

            if tamanho_mb > 5:

                st.error("❌ O arquivo excede 5MB.")
                st.stop()

            os.makedirs("documentos", exist_ok=True)

            caminho = os.path.join(
                "documentos",
                arquivo.name
            )

            with open(caminho, "wb") as f:
                f.write(arquivo.getbuffer())

            nome_arquivo = arquivo.name

        salvar(
            nome,
            email,
            telefone,
            caso,
            nome_arquivo
        )

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
    "Usuário",
    key="usuario"
)

senha_input = st.text_input(
    "Senha",
    type="password",
    key="senha"
)

# =========================================
# LOGIN BOTÃO
# =========================================
if st.button("🚪 Entrar no Painel"):

    usuario_digitado = st.session_state.usuario
    senha_digitada = st.session_state.senha

    st.session_state.limpar_login = True

    if (
        usuario_digitado == USUARIO
        and senha_digitada == SENHA
    ):

        st.session_state.logado = True

        st.success("✅ Login realizado!")

        st.rerun()

    else:

        st.error("❌ Usuário ou senha inválidos.")

        st.rerun()

# =========================================
# PAINEL
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
        font-size:22px;
        font-weight:900;
        color:white;
        margin-bottom:34px;
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
            arquivo_cliente = row.iloc[4]
            data_cliente = row.iloc[5]

            telefone_limpo = ''.join(
                filter(str.isdigit, telefone_cliente)
            )

            whatsapp = (
                f"https://wa.me/55{telefone_limpo}"
            )

            st.markdown(f"""
            <div class="card">

            <div style="
            font-size:24px;
            font-weight:900;
            color:#00ffd0;
            margin-bottom:24px;
            ">
            👤 {nome_cliente}
            </div>

            <div style="
            font-size:22px;
            color:white;
            line-height:2;
            font-weight:800;
            ">

            📞 {telefone_cliente}<br><br>

            ✉️ {email_cliente}<br><br>

            ⚖️ {caso_cliente}<br><br>

            🕒 {data_cliente}

            </div>

            </div>
            """, unsafe_allow_html=True)

            # =========================================
            # ANEXO
            # =========================================
            if arquivo_cliente != "Nenhum arquivo":

                caminho_arquivo = os.path.join(
                    "documentos",
                    arquivo_cliente
                )

                st.markdown(f"""
                <div style="
                font-size:20px;
                font-weight:800;
                color:#00ffd0;
                margin-bottom:15px;
                ">
                📎 Arquivo anexado:
                {arquivo_cliente}
                </div>
                """, unsafe_allow_html=True)

                if os.path.exists(caminho_arquivo):

                    # =========================================
                    # VISUALIZAR PDF
                    # =========================================
                    if arquivo_cliente.lower().endswith(".pdf"):

                        with open(caminho_arquivo, "rb") as pdf_file:

                            st.download_button(
                                label="⬇️ Baixar PDF",
                                data=pdf_file,
                                file_name=arquivo_cliente,
                                mime="application/pdf"
                            )

                        st.markdown("### 👁️ Visualização do PDF")

                        with open(caminho_arquivo, "rb") as f:
                            pdf_bytes = f.read()

                        st.download_button(
                            "📄 Baixar Documento",
                            data=pdf_bytes,
                            file_name=arquivo_cliente
                        )

                    # =========================================
                    # IMAGENS
                    # =========================================
                    elif arquivo_cliente.lower().endswith(
                        (".png", ".jpg", ".jpeg")
                    ):

                        st.image(
                            caminho_arquivo,
                            width=600
                        )

                        with open(caminho_arquivo, "rb") as file:

                            st.download_button(
                                "⬇️ Baixar Imagem",
                                data=file,
                                file_name=arquivo_cliente
                            )

                    # =========================================
                    # OUTROS ARQUIVOS
                    # =========================================
                    else:

                        with open(caminho_arquivo, "rb") as file:

                            st.download_button(
                                "⬇️ Baixar Documento",
                                data=file,
                                file_name=arquivo_cliente
                            )

                else:

                    st.warning(
                        "Arquivo não encontrado na pasta."
                    )

            st.link_button(
                "💬 Abrir WhatsApp",
                whatsapp
            )

            st.divider()

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
