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
# LIMPA LOGIN
# =========================================
if st.session_state.limpar_login:

    st.session_state["usuario"] = ""
    st.session_state["senha"] = ""

    st.session_state.limpar_login = False

# =========================================
# CSS PREMIUM CLEAN
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
}

.frase span {

    color: #00ffd0;
}

/* LABELS */
label,
.stTextInput label,
.stTextArea label {

    color: #FFFFFF !important;

    font-size: 20px !important;

    font-weight: 800 !important;
}

/* INPUTS */
.stTextInput input {

    background: #0b0b0b !important;

    border: 2px solid rgba(0,255,208,0.45) !important;

    #borda inicial nome email
    
    border-radius: 2px !important;

    color: #FFFFFF !important;

    font-size: 20px !important;

    font-weight: 700 !important;
#ajuste da altura do nome dentro da caixa
    height: 47px !important;

    padding-left: 22px !important;

    box-shadow: none !important;

    outline: none !important;

    transition: 0.2s ease !important;
}

/* INPUT FOCUS */
.stTextInput input:focus {

    border: 2px solid rgba(0,255,208,0.45) !important;

    box-shadow: none !important;

    outline: none !important;
}

/* PLACEHOLDER INPUT */
.stTextInput input::placeholder {

    color: rgba(255,255,255,0.82) !important;

    opacity: 1 !important;

    font-size: 20px !important;

    font-weight: 700 !important;
}

/* TEXTAREA */
.stTextArea textarea {

    background: #0b0b0b !important;

    border: 2px solid rgba(0,255,208,0.45) !important;

    border-radius: 2px !important;

    color: #FFFFFF !important;

    font-size: 24px !important;

    font-weight: 800 !important;

    padding: 24px !important;

    line-height: 1.7 !important;

    box-shadow: none !important;

    outline: none !important;

    transition: 0.2s ease !important;
}

/* TEXTAREA FOCUS */
.stTextArea textarea:focus {

    border: 1px solid rgba(0,255,208,0.55) !important;

    box-shadow: none !important;

    outline: none !important;
}

/* PLACEHOLDER TEXTAREA */
.stTextArea textarea::placeholder {

    color: rgba(255,255,255,0.82) !important;

    opacity: 1 !important;

    font-size: 24px !important;

    font-weight: 800 !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {

    background: #0b0b0b !important;

    border: 2px solid rgba(0,255,208,0.45) !important;

    border-radius: 2px !important;

    padding: 18px !important;

    box-shadow: none !important;

    margin-top: 14px !important;

    transition: 0.2s ease !important;
}

/* FILE UPLOADER INTERNO */
[data-testid="stFileUploader"] section {

    border: none !important;

    background: transparent !important;

    box-shadow: none !important;
}

/* REMOVE QUALQUER BRILHO */
.stTextInput,
.stTextArea,
[data-testid="stFileUploader"] {

    box-shadow: none !important;
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

    border-radius: 2px !important;

    height: 47px !important;

    width: 100%;

    border: none !important;

    margin-top: 24px;

    transition: 0.2s ease;

    box-shadow: none !important;
}

/* BOTÃO HOVER */
.stButton > button:hover {

    transform: translateY(-1px);

    box-shadow: none !important;
}

/* TÍTULO ADMIN */
.titulo-admin {

    font-size: 22px;

    font-weight: 900;

    text-align: center;

    margin-top: 20px;

    margin-bottom: 20px;

    color: white;
}

/* FOOTER */
.footer {

    text-align: center;

    color: #f0f0f0;

    font-size: 16px;

    margin-top: 30px;
}

/* CARD */
.card {

    background: #0d0d0d;

    padding: 35px;

    border-radius: 10px;

    margin-bottom: 35px;

    border: 2px solid rgba(0,255,208,0.45);
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

            os.makedirs(
                "documentos",
                exist_ok=True
            )

            caminho = os.path.join(
                "documentos",
                arquivo.name
            )

            with open(caminho, "wb") as f:

                f.write(
                    arquivo.getbuffer()
                )

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

        st.success(
            "✅ Dados enviados com sucesso!"
        )

        st.link_button(
            "💬 Falar no WhatsApp",
            link
        )

    else:

        st.error(
            "⚠️ Preencha os campos obrigatórios."
        )

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
# BOTÃO LOGIN
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

        st.error(
            "❌ Usuário ou senha inválidos."
        )

        st.rerun()

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

        df = df.iloc[::-1]

        st.markdown(f"""
        <div style="
        font-size:22px;
        font-weight:900;
        margin-bottom:25px;
        ">
        📊 Total de clientes: {len(df)}
        </div>
        """, unsafe_allow_html=True)

        for i, row in df.iterrows():

            nome_cliente = row.iloc[0]

            email_cliente = row.iloc[1]

            telefone_cliente = str(row.iloc[2])

            caso_cliente = row.iloc[3]

            arquivo_cliente = row.iloc[4]

            data_cliente = row.iloc[5]

            telefone_limpo = ''.join(
                filter(
                    str.isdigit,
                    telefone_cliente
                )
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
            margin-bottom:20px;
            ">
            👤 {nome_cliente}
            </div>

            <div style="
            font-size:21px;
            line-height:2;
            font-weight:700;
            ">

            📞 {telefone_cliente}<br><br>

            ✉️ {email_cliente}<br><br>

            ⚖️ {caso_cliente}<br><br>

            🕒 {data_cliente}

            </div>

            </div>
            """, unsafe_allow_html=True)

            if arquivo_cliente != "Nenhum arquivo":

                caminho_arquivo = os.path.join(
                    "documentos",
                    arquivo_cliente
                )

                st.markdown(f"""
                <div style="
                font-size:18px;
                font-weight:800;
                color:#00ffd0;
                margin-bottom:15px;
                ">
                📎 {arquivo_cliente}
                </div>
                """, unsafe_allow_html=True)

                if os.path.exists(caminho_arquivo):

                    if arquivo_cliente.lower().endswith(".pdf"):

                        with open(
                            caminho_arquivo,
                            "rb"
                        ) as pdf_file:

                            pdf_bytes = pdf_file.read()

                            st.download_button(
                                "⬇️ Baixar PDF",
                                data=pdf_bytes,
                                file_name=arquivo_cliente,
                                mime="application/pdf"
                            )

                    elif arquivo_cliente.lower().endswith(
                        (
                            ".png",
                            ".jpg",
                            ".jpeg"
                        )
                    ):

                        st.image(
                            caminho_arquivo,
                            width=500
                        )

                        with open(
                            caminho_arquivo,
                            "rb"
                        ) as file:

                            st.download_button(
                                "⬇️ Baixar Imagem",
                                data=file,
                                file_name=arquivo_cliente
                            )

                    else:

                        with open(
                            caminho_arquivo,
                            "rb"
                        ) as file:

                            st.download_button(
                                "⬇️ Baixar Documento",
                                data=file,
                                file_name=arquivo_cliente
                            )

                else:

                    st.warning(
                        "Arquivo não encontrado."
                    )

            st.link_button(
                "💬 Abrir WhatsApp",
                whatsapp
            )

            st.divider()

    else:

        st.warning(
            "Nenhum cliente encontrado."
        )

# =========================================
# FOOTER
# =========================================
st.markdown("""
<div class="footer">
🔒 Seus dados estão protegidos e não serão compartilhados.
</div>
""", unsafe_allow_html=True)
