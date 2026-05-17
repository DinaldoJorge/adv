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

/* REMOVE ELEMENTOS STREAMLIT */

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
    font-size:28px;
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
    color: white !important;
    font-size:25px !important;
    font-weight:800 !important;
}

/* =====================================================
INPUTS
===================================================== */

.stTextInput input{

    background: black !important;

    color:white !important;

    border: 2px solid white !important;

    border-radius: 2px solid white !important;

    height:45px !important;

    font-size:18px !important;

    font-weight:600 !important;

    padding-left:18px !important;

    transition:0.3s !important;

   # box-shadow:
   #  0 0 10px white ;

}

.stTextInput input:focus{

    border: 2px solid #00d9ff !important;

}

/* =====================================================
TEXTAREA
===================================================== */

.stTextArea textarea{

    background: black !important;

    color: white !important;

    border: 2px solid white!important;

    border-radius: 2px solid white!important;

    font-size:19px !important;

    font-weight:600 !important;

    padding:18px !important;

    transition:0.3s !important;

}

.stTextArea textarea:focus{

    border: 4px solid green !important;

}

/* =====================================================
PLACEHOLDER
===================================================== */

::placeholder{

    color: #00d9ff !important;

    opacity:1 !important;

}

# Código Streamlit MZA Advogados — Atualizado Completo

Substitua apenas a seção abaixo no seu arquivo atual.

```python
/* =====================================================
FILE UPLOADER PREMIUM MZA
===================================================== */

[data-testid="stFileUploader"]{

    background: black !important;

    border: 2px solid #00d9ff !important;

    border-radius: 18px !important;

    padding: 22px !important;

    margin-top: 15px !important;

    transition: 0.3s ease-in-out !important;

    box-shadow:
        0 0 10px rgba(0,217,255,0.15);
}

/* ÁREA INTERNA */

[data-testid="stFileUploader"] section{

    background: #f5f5f5 !important;

    border-radius: 16px !important;

    border: 1px solid rgba(255,255,255,0.15) !important;

    padding: 22px !important;
}

/* REMOVE FUNDOS INTERNOS */

[data-testid="stFileUploader"] div{

    background-color: transparent !important;
}

/* TEXTO PRINCIPAL */

[data-testid="stFileUploader"] small{

    color: #0066ff !important;

    font-size: 17px !important;

    font-weight: 700 !important;

    letter-spacing: 0.3px !important;
}

/* LABEL */

[data-testid="stFileUploader"] label{

    color: white !important;

    font-size: 20px !important;

    font-weight: 800 !important;
}

/* TEXTO DRAG */

[data-testid="stFileUploader"] p{

    color: black !important;

    font-size: 16px !important;

    font-weight: 700 !important;
}

/* =====================================================
BOTÃO UPLOAD AZUL PREMIUM
===================================================== */

[data-testid="stFileUploader"] button{

    background: linear-gradient(
        135deg,
        #0066ff,
        #00aaff
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 14px !important;

    font-size: 18px !important;

    font-weight: 800 !important;

    height: 52px !important;

    padding: 0 30px !important;

    box-shadow:
        0 0 12px rgba(0,170,255,0.6),
        0 0 25px rgba(0,100,255,0.4) !important;

    transition: all 0.25s ease-in-out !important;
}

/* HOVER */

[data-testid="stFileUploader"] button:hover{

    background: linear-gradient(
        135deg,
        #0055ff,
        #00ccff
    ) !important;

    color: white !important;

    transform: translateY(-2px) scale(1.03);

    box-shadow:
        0 0 18px rgba(0,170,255,0.8),
        0 0 35px rgba(0,100,255,0.6) !important;
}

/* CLIQUE */

[data-testid="stFileUploader"] button:active{

    transform: scale(0.96);
}

/* REMOVE FUNDO BRANCO */

[data-testid="stFileUploader"] div{

    background-color:transparent !important;
}

/* TEXTO DRAG */

[data-testid="stFileUploader"] p{

    color: black !important;

    font-size:16px !important;

    font-weight:600 !important;
}

/* =====================================================
BOTÕES PREMIUM
===================================================== */

.stButton > button{

    width:100%;

    height:58px;

    border:none !important;

    border-radius:18px !important;

    background:linear-gradient(
        135deg,
        #00d9ff,
        #00d9ff
    ) !important;

    color: black !important;

    font-size:20px !important;

    font-weight:800 !important;

    letter-spacing:0.5px;


    transition:all 0.25s ease-in-out !important;
}

.stButton > button:hover{

    transform:translateY(-2px) scale(1.01);

    background:linear-gradient(
        135deg,
        #00d9ff,
        #00d9ff
    ) !important;

    color:black !important;
   
}

.stButton > button:active{

    transform:scale(0.98);

}

/* =====================================================
CARD
===================================================== */

.card{

    background:linear-gradient(
        180deg,
        #00d9ff,
        #00d9ff
    );

    border: 2px solid #00d9ff;

    border-radius: 2px #00d9ff;

    padding:35px;

    margin-bottom:30px;

  
}

/* =====================================================
TÍTULOS
===================================================== */

.titulo-admin{

    text-align:center;

    font-size:28px;

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

    color: #00d9ff;

    margin-top:40px;

    font-size:13px;

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
        "Enviar Dados"
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
        color: black;
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
            color:green;
            margin-bottom:25px;
            ">
            {nome_cliente}
            </div>

            <div style="
            font-size:22px;
            line-height:2.1;
            color: white;
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

                if os.path.exists(caminho_arquivo):

                    if arquivo_cliente.lower().endswith(
                        (".png",".jpg",".jpeg")
                    ):

                        st.image(
                            caminho_arquivo,
                            width=450
                        )

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
