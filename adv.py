import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================

st.set_page_config(
    page_title="MZA Advogados",
    page_icon="⚖️",
    layout="wide"
)

# =====================================================
# LOGIN
# =====================================================

USUARIO = "admin"
SENHA = "mza2026"

if "logado" not in st.session_state:
    st.session_state["logado"] = False

# =====================================================
# CSS PREMIUM
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

.stApp{
    background:black;
    color:white;
}

/* REMOVE STREAMLIT */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

.block-container{
    padding-top:2rem;
    max-width:1200px;
}

/* =====================================================
FRASE
===================================================== */

.frase{
    text-align:center;
    font-size:30px;
    font-weight:900;
    color:white;
    margin-top:10px;
    margin-bottom:45px;
}

.frase span{
    color:#00d9ff;
}

/* =====================================================
LABELS
===================================================== */

label{
    color:white !important;
    font-size:21px !important;
    font-weight:800 !important;
}

/* =====================================================
INPUTS
===================================================== */

.stTextInput input{

    background: black !important;

    color:white !important;

    border:2px solid white !important;

    border-radius:2px !important;

    height:45px !important;

    font-size:18px !important;

    font-weight:600 !important;

    padding-left:18px !important;

    transition:0.3s !important;

}

.stTextInput input:focus{

    border:2px solid #00d9ff !important;

}

/* =====================================================
TEXTAREA
===================================================== */

.stTextArea textarea{

    background:black !important;

    color:white !important;

    border:2px solid white !important;

    border-radius: 2px !important;

    font-size:19px !important;

    font-weight:600 !important;

    padding:18px !important;

    transition:0.3s !important;

}

.stTextArea textarea:focus{

    border:2px solid #00d9ff !important;

}

/* =====================================================
PLACEHOLDER
===================================================== */

::placeholder{

    color:#00d9ff !important;

    opacity:1 !important;

}

/* =====================================================
FILE UPLOADER PREMIUM
===================================================== */

[data-testid="stFileUploader"]{

    background:black !important;

    border:2px solid white !important;

    border-radius: 2px !important;

    padding:20px !important;

    margin-top:10px !important;
}

/* ÁREA INTERNA */

[data-testid="stFileUploader"] section{

    background: white !important;

    border-radius:2px !important;

    border:1px solid #00d9ff !important;

    padding:18px !important;

}

/* TEXTO */

[data-testid="stFileUploader"] small{

    color:#00d9ff !important;

    font-size:15px !important;

    font-weight:600 !important;

}

/* BOTÃO UPLOAD */

[data-testid="stFileUploader"] button{

    background:linear-gradient(
        135deg,
        #00d9ff,
        #00d9ff
    ) !important;

    color:black !important;

    border:none !important;

    border-radius: 2px !important;

    font-size:15px !important;

    font-weight:900 !important;

    height:44px !important;

    padding:0 24px !important;

}
/* =====================================================
DOWNLOAD BUTTON AZUL NEON
===================================================== */

.stDownloadButton > button{

    width:100% !important;

    height:55px !important;

    background:linear-gradient(
        135deg,
        #00aaff,
        #00d9ff
    ) !important;

    color:black !important;

    border:none !important;

    border-radius:18px !important;

    font-size:18px !important;

    font-weight:900 !important;

    box-shadow:
    0 0 14px rgba(0,217,255,0.35),
    0 0 22px rgba(0,217,255,0.20);

    transition:0.3s ease-in-out !important;
}


/* HOVER */

.stDownloadButton > button:hover{

    transform:scale(1.02);

    background:linear-gradient(
        135deg,
        #00d9ff,
        #00aaff
    ) !important;

    color:black !important;

    box-shadow:
    0 0 20px rgba(0,217,255,0.55),
    0 0 30px rgba(0,217,255,0.35);
}
/* =====================================================
CARD
===================================================== */

.card{

    background:linear-gradient(
        180deg,
        black,
        black
    );

    border:1px solid #00d9ff;

    border-radius: 4px;

    padding:35px;

    margin-bottom:30px;

}

/* =====================================================
TÍTULOS
===================================================== */

.titulo-admin{

    text-align:center;

    font-size:30px;

    font-weight:900;

    margin-top:20px;

    margin-bottom:25px;

    color:white;

}

/* =====================================================
FOOTER
===================================================== */

.footer{

    text-align:center;

    color:#00d9ff;

    margin-top:40px;

    font-size:14px;

    font-weight:700;

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEETS
# =====================================================

planilha = None

try:

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    planilha = client.open(
        "leads_professores"
    ).sheet1

except Exception as e:

    st.error("Erro ao conectar com Google Sheets.")
    st.stop()

# =====================================================
# LOGO
# =====================================================

col1, col2, col3 = st.columns([1,2,1])

with col2:

    if os.path.exists("logomza.png"):

        st.image(
            "logomza.png",
            width=420
        )

# =====================================================
# FRASE
# =====================================================

st.markdown("""
<div class="frase">
Vamos <span>analisar</span> seus dados
</div>
""", unsafe_allow_html=True)

# =====================================================
# FORMULÁRIO
# =====================================================

with st.form("formulario", clear_on_submit=True):

    nome = st.text_input(
        "Nome completo",
        placeholder="Digite seu nome"
    )

    email = st.text_input(
        "Email",
        placeholder="Digite seu melhor email"
    )

    telefone = st.text_input(
        "Telefone",
        placeholder="Digite seu telefone"
    )

    caso = st.text_area(
        "Caso jurídico",
        placeholder="Explique sua situação jurídica...",
        height=220
    )

    arquivo = st.file_uploader(
        "📎 Anexar documento",
        type=["pdf","png","jpg","jpeg","doc","docx"]
    )

    enviar = st.form_submit_button(
        "⚖️ Enviar Dados"
    )

# =====================================================
# FUNÇÃO SALVAR
# =====================================================

def salvar_dados():

    nome_arquivo = "Nenhum arquivo"

    if arquivo is not None:

        os.makedirs(
            "documentos",
            exist_ok=True
        )

        caminho = os.path.join(
            "documentos",
            arquivo.name
        )

        with open(caminho, "wb") as f:
            f.write(arquivo.getbuffer())

        nome_arquivo = arquivo.name

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

# =====================================================
# ENVIAR
# =====================================================

if enviar:

    if nome and email and caso:

        try:

            salvar_dados()

            st.success(
                "Dados enviados com sucesso!"
            )

            st.link_button(
                "📞 Fazer contato com MZA-ADVOGADOS",
                "https://wa.me/5583998234415"
            )

        except Exception as e:

            st.error(
                "Erro ao salvar informações."
            )

    else:

        st.warning(
            "Preencha os campos obrigatórios."
        )

# =====================================================
# LOGIN
# =====================================================

st.divider()

st.markdown("""
<div class="titulo-admin">
Acesso Painel Jurídico
</div>
""", unsafe_allow_html=True)

usuario = st.text_input(
    "Usuário",
    placeholder="Digite o usuário"
)

senha = st.text_input(
    "Senha",
    type="password",
    placeholder="Digite a senha"
)

if st.button("Entrar no Painel"):

    if usuario == USUARIO and senha == SENHA:

        st.session_state["logado"] = True
        st.rerun()

    else:

        st.error(
            "Usuário ou senha inválidos."
        )

# =====================================================
# PAINEL ADMIN
# =====================================================

if st.session_state["logado"]:

    st.divider()

    st.markdown("""
    <div class="titulo-admin">
    Painel Jurídico Premium
    </div>
    """, unsafe_allow_html=True)

    if st.button("Sair do Painel"):

        st.session_state["logado"] = False
        st.rerun()

    dados = planilha.get_all_records()

    if dados:

        df = pd.DataFrame(dados)

        df = df.iloc[::-1]

        busca = st.text_input(
            "Pesquisar cliente",
            placeholder="Digite nome, email ou telefone"
        )

        if busca:

            df = df[
                df.astype(str)
                .apply(
                    lambda x:
                    x.str.contains(
                        busca,
                        case=False
                    )
                )
                .any(axis=1)
            ]

        st.markdown(f"""
        <div style="
        font-size:24px;
        font-weight:900;
        margin-bottom:30px;
        color:#00d9ff;
        ">
        Total de clientes: {len(df)}
        </div>
        """, unsafe_allow_html=True)

        for i, row in df.iterrows():

            nome_cliente = row.iloc[0]
            email_cliente = row.iloc[1]
            telefone_cliente = row.iloc[2]
            caso_cliente = row.iloc[3]
            arquivo_cliente = row.iloc[4]
            data_cliente = row.iloc[5]

            st.markdown(f"""
            <div class="card">

            <div style="
            font-size:30px;
            font-weight:900;
            color:#00d9ff;
            margin-bottom:25px;
            ">
            {nome_cliente}
            </div>

            <div style="
            font-size:22px;
            line-height:2.1;
            color:white;
            font-weight:700;
            ">

            📞 {telefone_cliente}<br><br>

            ✉️ {email_cliente}<br><br>

            ⚖️ {caso_cliente}<br><br>

            🕒 {data_cliente}

            </div>

            </div>
            """, unsafe_allow_html=True)

            # =====================================================
            # ANEXOS
            # =====================================================

            if arquivo_cliente != "Nenhum arquivo":

                caminho_arquivo = os.path.join(
                    "documentos",
                    arquivo_cliente
                )

                if os.path.exists(caminho_arquivo):

                    st.markdown("""
                    <div style="
                    color:#00d9ff;
                    font-size:20px;
                    font-weight:900;
                    margin-bottom:15px;
                    ">
                    Pré-visualização do anexo
                    </div>
                    """, unsafe_allow_html=True)

                    # IMAGEM

                    if arquivo_cliente.lower().endswith(
                        (".png",".jpg",".jpeg")
                    ):

                        st.image(
                            caminho_arquivo,
                            width=500
                        )

                    # PDF

                    elif arquivo_cliente.lower().endswith(".pdf"):

                        with open(caminho_arquivo, "rb") as pdf_file:

                            PDFbyte = pdf_file.read()

                            st.download_button(
                                label="📄 Baixar PDF",
                                data=PDFbyte,
                                file_name=arquivo_cliente,
                                mime="application/pdf",
                                key=f"pdf_{i}"
                            )

                    # DOWNLOAD GERAL

                    with open(
                        caminho_arquivo,
                        "rb"
                    ) as file:

                        st.download_button(
                            label="⬇️ Baixar Anexo",
                            data=file,
                            file_name=arquivo_cliente,
                            key=f"download_{i}"
                        )

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
🔒 Seus dados estão protegidos e não serão compartilhados.
</div>
""", unsafe_allow_html=True)
