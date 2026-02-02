import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import base64
import os

st.set_page_config(
    page_title="Auditoria de Qualidade",
    page_icon="assets/icon.png",
    layout="wide"
)

def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [clas="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #0a0a0a;
    }}

    .stApp {{
        background: radial-gradient(circle at center, #1a1a1a 0%, #050505 100%);
    }}

    div[data-testid="stVerticalBlock"] > div:has(div.login-card) {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 90vh;
    }}

    .login-card {{
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid rgba(227, 112, 38, 0.3);
        width: 100%;
        max-width: 400px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    }}

    .login-card div[data-testid="stForm"] {{
        background: transparent ;
        border: none ;
        padding: 0 ;
    }}

    .stButton > button {{
        background-color: #E37026 ;
        color: white ;
        border-radius: 12px ;
        border: none ;
        padding: 12px ;
        font-weight: 600 ;
        text-transform: uppercase;
        margin-top: 15px;
        box-shadow: 0 0 15px rgba(227, 112, 38, 0.4)
        transition: 0.3s ease, box-shadow 0.2s;
    }}

    .stButton > button:hover {{
        background-color: #f0853d ;
        transform: translateY(-2px)
        box-shadow: 0 0 15px rgba(227, 112, 38, 0.4) ;
    }}

    [data-testid="stSidebar"] {{
        background-color: #050505 ;
        border-right: 1px solid rgba(227, 112, 38, 0.2);
    }}

    h1, h2, h3 {{ color: #ffffff !important; font-weight: 600; letter-spacing: -0.5px; }}

    .login-container {{
        background-color: transparent; 
        background-image: linear-gradient(160deg, #1e1e1f 0%, #0a0a0c 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }}
    
    .input {{
        background-color: rgba(255, 255, 255, 0.05) ;
        border: 1px solid rgba(255, 255, 255, 0.1) ;
        border-radius: 10px ;
        color: white ;
    }}
    .sidebar-logo-container {{
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }}
    .sidebar-logo-text {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.5rem;
        color: white;
        letter-spacing: 2px;
    }}
    .sidebar-logo-sub {{
        font-size: 0.7rem;
        color: var(--primary);
        text-transform: uppercase;
        letter-spacing: 3px;
    }}
    </style>
""", unsafe_allow_html=True)

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    _, col_login, _ = st.columns([1, 1, 1])
    with col_login:
        logo_file = "assets/logo.png" if os.path.exists("assets/logo.png") else "assets/logo.jpg"
        img_b64 = get_base64_image(logo_file)
        
        if img_b64:
            mime_type = "image/png" if logo_file.endswith(".png") else "image/jpeg"
            header_html = f'<img src="data:{mime_type};base64,{img_b64}" style="width: 650px; height: auto; display: block; margin: 0 auto 20px auto;">'
        else:
            header_html = "<h2 style='color:#E37026; margin-bottom: 10px;'>LAVIE</h2>"
        st.markdown(f"""
        <div class="login-container">
             {header_html}
            <h2 style='color:#E37026; font-size: 3rem; margin-top: 10px; margin-bottom: 0px;'>QUALIDADE</h2>
            <p style='color:#E37026; font-size: 0.8rem; margin-top: 0px; letter-spacing: 2px;'>Formulários de Auditoria</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("credenciais_acesso"):
            st.markdown("<p style='text-align: left; font-size: 14px; margin-bottom: 15px;'>Senha de Acesso</p>", unsafe_allow_html=True)
            senha_input = st.text_input("", type="password", label_visibility="collapsed")
            if st.form_submit_button("Entrar", use_container_width=True):
                if senha_input == st.secrets["access"]["password"]:
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("Senha inválida")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    conn = st.connection("gsheets", type=GSheetsConnection)
    auditores = ["Henrique Rodrigues", "Bianca Morais", "Gabriel Alves"]
    obras = ["Arc Space", "Burj Lavie", "Lavie Camboinha", "JCarlos"]
    sim_nao = ["Sim", "Não"]
    sim_nao_na = ["Sim", "Não", "Não se aplica"]

    with st.sidebar:
        st.image("assets/logo.png", use_container_width=True)
        st.markdown("")
        st.markdown("""
            <div class="sidebar-logo-container">
                <div class="sidebar-logo-text">QUALIDADE</div>
                <div class="sidebar-logo-sub">Formulários de Auditoria</div>
            </div>
        """, unsafe_allow_html=True)
        escolha = option_menu(
            None,
            ["Canteiro", "Estoque", "Habite-se", "Seg. Documental", "Seg. Externo", "Seg. Interno", "Qualidade"],
            icons=["building", "box", "clipboard-check", "file-earmark-lock", "person-up", "person-gear", "star"],
            styles={"nav-link-selected": {"background-color": "#E37026"}}
        )

    if escolha == "Canteiro":
        st.header("CANTEIRO E ESCRITÓRIO DE OBRAS")
        with st.form("form_canteiro"):
            aud = st.selectbox("Auditor interno responsável", auditores)
            obr = st.selectbox("Obra auditada", obras)
            st.subheader("CANTEIRO DE OBRAS")
            q1 = st.radio("Há disponibilidade de EPI's para visitantes?", sim_nao, horizontal=True)
            q2 = st.radio("Há kit de materiais de primeiros socorros em obra?", sim_nao, horizontal=True)
            q3 = st.radio("Há placas de sinalização e advertência no canteiro de obras? ", sim_nao, horizontal=True)
            q4 = st.radio("Há placas de orientação no canteiro de obras (rota segura, local de 1ºs socorros, locais do canteiro e nº dos pavimentos)? ", sim_nao, horizontal=True)
            q5 = st.radio("As áreas de vivência (refeitório, vestiário, banheiros e áreas comuns) estão em conformidade de organização e limpeza? ", sim_nao, horizontal=True)
            q6 = st.radio("O canteiro de obras está em conformidade de limpeza e organização? ", sim_nao, horizontal=True)
            q7 = st.radio("As escadas de canteiro (Quando houver) estão em condições seguras de uso", sim_nao_na, horizontal=True)
            q8 = st.radio("As barreiras e guarda corpos (quando houver) estão instalados em conformidade com as normas de segurança?", sim_nao_na, horizontal=True)
            q9 = st.radio("As áreas abaixo de locais de trabalho elevado (quando houver), onde há passagem de pessoas, estão protegidas contra a queda de objetos?", sim_nao_na, horizontal=True)
            q10 = st.radio("As máquinas e equipamentos (Bancada de serra, betoneira, guincho, etc) em uso estão em boas condições de funcionamento?", sim_nao, horizontal=True)
            q11 = st.radio("As instalações provisórias de canteiro estão em conformidade de segurança?", sim_nao, horizontal=True)
            q12 = st.radio("A obra possui extintores nas áreas exigidas por norma?", sim_nao, horizontal=True)
            st.subheader("ESCRITÓRIO DE OBRA")
            q13 = st.radio("Há na obra escritório onde a equipe técnica possa monitorar o progresso do projeto e acompanhar as demandas?", sim_nao, horizontal=True)
            q14 = st.radio("Há no escritório painel de gestão a vista com restrições e planejamentos de longo, médio e curto prazo?", sim_nao, horizontal=True)
            q15 = st.radio("Há registro atualizado (até o dia anterior à auditoria) no diário de obra?", sim_nao, horizontal=True)
            q16 = st.radio("O diário de obras está preenchido de forma completa (com frentes de serviço, mão de obra, e legendas nas imagens)", sim_nao, horizontal=True)
            q17 = st.radio("Há plano semanal atualizado no drive da obra?", sim_nao, horizontal=True)
            obs = st.text_area("Observações")
            if st.form_submit_button("SALVAR", use_container_width=True):
                df = pd.DataFrame([{"timestamp": datetime.now(), "auditor": aud, "obra": obr, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10, "q11": q11, "q12": q12, "q13": q13, "q14": q14, "q15": q15, "q16": q16, "q17": q17, "obs": obs}])
                conn.create(worksheet="auditoria_canteiro", data=df)
                st.success("Salvo com sucesso!")

    elif escolha == "Estoque":
        st.header("ESTOQUE")
        with st.form("form_estoque"):
            aud = st.selectbox("Auditor interno responsável", auditores)
            obr = st.selectbox("Obra auditada", obras)
            insumos_lista = ["Acabamento elétrico", "Areia", "Argamassa", "Barras de telas de aço", "Bloco de vedação", "Brita", "Cal hidratada", "Cimento", "Conjunto porta pronta", "Disjuntor", "Eletroduto", "Fio e cabos elétricos", "Gesso em pó", "Gesso para forro (placa e acartonada)", "Louça sanitária", "Madeira - Chapas compensadas", "Madeira - tábuas e barrotes", "Manta asfáltica", "Mármores e granitos", "Revestimento cerâmico, porcelanato ou pastilhas", "Tintas", "Tubos e conexões metálicas", "Tubos e conexões hidrossanitárias"]
            grupo = st.selectbox("Grupo de insumo a ser auditado", insumos_lista)
            especifico = st.text_input("Insumo específico controlado a ser auditádo")
            st.subheader("FICHA DE VERIFICAÇÃO DE MATERIAL")
            q1 = st.radio("A FVM (Ficha de Verificação de Material) foi preenchida? (Solicitar evidência)", sim_nao, horizontal=True)
            q2 = st.radio("Conferir se há não conformidade aplicada a FVM aberta. A data para remoção da não conformidade foi respeitada?", sim_nao_na, horizontal=True)
            st.subheader("LANÇAMENTO DE NOTA FISCAL")
            nf_num = st.text_input("Qual o Nº da nota fiscal do insumo auditado?")
            q3 = st.radio("A NF foi lançada no prazo previsto em procedimento? (Até 4 dias após o recebimento do insumo)", sim_nao, horizontal=True)
            st.subheader("ARMAZENAMENTO E IDENTIFICAÇÃO")
            q4 = st.radio("O insumo está armazenado conforme TAM", sim_nao_na, horizontal=True)
            st.subheader("ASSERTIVIDADE DE ESTOQUE")
            q6 = st.radio("Conferir o quantitativo descrito no relatório de 'Posição de estoque atual' com o armazenamento. Os valores estão corretos?", sim_nao, horizontal=True)
            obs = st.text_area("Observações importantes")
            if st.form_submit_button("SALVAR", use_container_width=True):
                df = pd.DataFrame([{"timestamp": datetime.now(), "auditor": aud, "obra": obr, "grupo": grupo, "insumo": especifico, "q1": q1, "q2": q2, "nf": nf_num, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "obs": obs}])
                conn.create(worksheet="auditoria_estoque", data=df)
                st.success("Salvo com sucesso!")

    elif escolha == "Habite-se":
        st.header("HABITE-SE")
        with st.form("form_habite"):
            aud = st.selectbox("Auditor interno responsável", auditores)
            obr = st.selectbox("Obra auditada", obras)
            st.subheader("DOCUMENTAÇÃO E IDENTIFICAÇÃO NO LOCAL")
            q1 = st.radio("Há placa de obra instalada com dados do responsável técnico?", sim_nao, horizontal=True)
            q2 = st.radio("Os projetos arquitetônicos e complementares estão disponíveis?", sim_nao, horizontal=True)
            q3 = st.radio("Há ART's e RRT's de execução e de responsáveis técnicos vigentes?", sim_nao, horizontal=True)
            st.subheader("CONFORMIDADE DA EDIFICAÇÃO COM PROJETO APROVADO")
            q4 = st.radio("Afastamentos frontais, laterais e de fundo coincidem com o projeto aprovado?", sim_nao, horizontal=True)
            q5 = st.radio("A altura da edificação coincide com o projeto aprovado?", sim_nao, horizontal=True)
            q6 = st.radio("Houve aumento de área construída que não conste no projeto aprovado?", sim_nao, horizontal=True)
            q7 = st.radio("As áreas de ocupação e permeabilidade coincidem com as taxas definidas em projeto?", sim_nao, horizontal=True)
            st.subheader("CONDIÇÕES GERAIS DA EDIFICAÇÃO")
            q8 = st.radio("Confirme se há estrutura não finalizada", sim_nao, horizontal=True)
            q9 = st.radio("Existem áreas de revestimento, acabamentos e pisos inacabados?", sim_nao, horizontal=True)
            q10 = st.radio("Todos os Corrimãos, guarda-corpos, portas e janelas estão devidamente instalados?", sim_nao, horizontal=True)
            q11 = st.radio("As adequações de acessibilidade estão executadas (rampas, piso tátil, wcs acessíveis)?", sim_nao, horizontal=True)
            st.subheader("INFRAESTRUTURA INSTALADA")
            q12 = st.radio("Ligação definitiva de energia elétrica está instalada?", sim_nao, horizontal=True)
            q13 = st.radio("A Ligação de água e esgoto estão em funcionamento?", sim_nao, horizontal=True)
            q14 = st.radio("As drenagens do terreno e das calhas foram executadas?", sim_nao, horizontal=True)
            q15 = st.radio("As instalações de gás (Se houver) foram executadas conforme normas?", sim_nao_na, horizontal=True)
            st.subheader("SEGURANÇA")
            q16 = st.radio("As rotas de saídas de emergência e rotas de fuga (se houver) estão desobstruídas?", sim_nao, horizontal=True)
            q17 = st.radio("Os extintores estão instalados conforme projeto aprovado?", sim_nao, horizontal=True)
            q18 = st.radio("Os extintores instalados estão dentro da validade?", sim_nao, horizontal=True)
            q19 = st.radio("As sinalizações de emergência foram instaladas conforme projeto aprovado?", sim_nao, horizontal=True)
            st.subheader("INFRAESTRUTURA EXTERNA")
            q20 = st.radio("As áreas de calçada e passeio estão em conformidade com o projeto aprovado?", sim_nao, horizontal=True)
            q21 = st.radio("As vagas de garagem estão de acordo com o projeto aprovado?", sim_nao, horizontal=True)
            q22 = st.radio("O acesso ao imóvel está livre de obstruções?", sim_nao, horizontal=True)
            q23 = st.radio("O paisagismo definido em projeto (se houver) está executado?", sim_nao, horizontal=True)
            st.subheader("CONFORMIDADE SANITÁRIA E AMBIENTAL")
            q24 = st.radio("Há acúmulo de resíduos de obra?", sim_nao, horizontal=True)
            q25 = st.radio("Houve destinação correta de resíduos durante a construção?", sim_nao, horizontal=True)
            q26 = st.radio("Há ligações clandestinas ou irregulares de água, esgoto ou elétrica?", sim_nao, horizontal=True)
            st.subheader("CONFORMIDADE DE SISTEMAS COMPLEMENTARES")
            q27 = st.radio("O sistema de combate a incêndio foi testado e aprovado?", ["Sim", "Não", "Não aplicável"], horizontal=True)
            q28 = st.radio("Os elevadores instalados possuem documento de conformidade?", sim_nao_na, horizontal=True)
            q29 = st.radio("Os reservatórios de água estão instalados e acessíveis?", sim_nao, horizontal=True)
            if st.form_submit_button("SALVAR", use_container_width=True, key="tip"):
                df = pd.DataFrame([{"timestamp": datetime.now(), "auditor": aud, "obra": obr, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10, "q11": q11, "q12": q12, "q13": q13, "q14": q14, "q15": q15, "q16": q16, "q17": q17, "q18": q18, "q19": q19, "q20": q20, "q21": q21, "q22": q22, "q23": q23, "q24": q24, "q25": q25, "q26": q26, "q27": q27, "q28": q28, "q29": q29}])
                conn.create(worksheet="auditoria_habitese", data=df)
                st.success("Salvo com sucesso!")

    elif escolha == "Seg. Documental":
        st.header("SEGURANÇA DO TRABALHO - DOCUMENTAL")
        with st.form("form_seg_doc"):
            aud = st.selectbox("Auditor interno responsável", auditores)
            obr = st.selectbox("Obra auditada", obras)
            docs = ["Há PGR (Programa de Gerenciamento de Riscos) em obra?", "Há PCMSO (Programa de Controle Médico de Saúde Ocupacional) em obra?", "Há ART (Anotação de Responsabilidade Técnica) de segurança em obra?", "Há ART de execução de obra e canteiro de obra?", "Há ART e projeto de canteiro da obra (Atualizado)?", "Há ART e projeto elétrico de canteiro da obra (Atualizado)?", "Há ART e projeto de incêndio de canteiro da obra (Atualizado)?", "Há projeto de SPDA (Sistema de proteção contra descarga atmosférica) ou laudo de despensa?", "Há relatório de análise ergonômica?", "Há PCA (Programa de Proteção Auditiva)?", "Há PPR (Programa de Proteção Respiratória)?", "Há comunicação prévia de início de obra cadastrado no MTE?", "Há Mapa de risco aplicado ao canteiro?", "Há CNO (Cadastro Nacional de Obra) - Receita Federal?", "Há laudo de conformidade de instalação de Bancada de Serra?", "Há laudo de conformidade de instalação de Betoneira?", "Há laudo de conformidade de instalação de Grua?", "Há laudo de conformidade de instalação de Elevador Cremalheira?", "Há laudo de conformidade de Policorte?"]
            respostas = [st.radio(d + "", sim_nao, horizontal=True) for d in docs]
            obs = st.text_area("Observações importantes")
            if st.form_submit_button("SALVAR", use_container_width=True):
                df = pd.DataFrame([{"timestamp": datetime.now(), "auditor": aud, "obra": obr, "res": str(respostas), "obs": obs}])
                conn.create(worksheet="auditoria_seg_doc", data=df)
                st.success("Salvo com sucesso!")

    elif escolha == "Seg. Externo":
        st.header("SEGURANÇA DO TRABALHO - COLABORADOR EXTERNO")
        with st.form("form_seg_ext"):
            aud = st.selectbox("Auditor interno responsável", auditores)
            obr = st.selectbox("Obra auditada", obras)
            forn = st.text_input("Nome do Fornecedor")
            colab = st.text_input("Nome do colaborador")
            cargo = st.selectbox("Cargo", ["Profissional", "Servente"])
            q1 = st.radio("A empresa terceirizada possui PCMSO (Programa de Controle Médico de Saúde Ocupacional) válido?", sim_nao, horizontal=True)
            q2 = st.radio("Há ART (Anotação de responsabilidade técnica) de execução do serviço?", sim_nao_na, horizontal=True)
            q3 = st.radio("O colaborador tem ficha de entrega de EPI atualizada (Equipamento de proteção individual) de acordo com o PGR?", sim_nao, horizontal=True)
            q4 = st.radio("O colaborador está usando EPI's adequdamente?", sim_nao, horizontal=True)
            q5 = st.radio("O colaborador possui ASO (Atestado de Saúde Ocupacional) e periódicos dentro do período de validade?", sim_nao, horizontal=True)
            q6 = st.radio("Solicitar a técnica de segurança a OS (Ordem de serviço) para o serviço em execução. Há OS assinada?", sim_nao, horizontal=True)
            q7 = st.radio("O colaborador foi treinado na NR06 (Equipamento de proteção individual)?", sim_nao_na, horizontal=True)
            q8 = st.radio("O colaborador foi treinado na NR12 (Segurança no trabalho em máquinas e equipamentos)?", sim_nao_na, horizontal=True)
            q9 = st.radio("O colaborador foi treinado na NR18 (Segurança e saúde no trabalho na indústria da construção)?", sim_nao_na, horizontal=True)
            q10 = st.radio("O colaborador foi treinado na NR35 (Trabalho em altura)?", sim_nao_na, horizontal=True)
            obs = st.text_area("Observações importantes")
            if st.form_submit_button("SALVAR", use_container_width=True):
                df = pd.DataFrame([{"timestamp": datetime.now(), "auditor": aud, "obra": obr, "forn": forn, "colab": colab, "cargo": cargo, "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10, "obs": obs}])
                conn.create(worksheet="auditoria_seg_ext", data=df)
                st.success("Salvo com sucesso!")

    elif escolha == "Seg. Interno":
        st.header("SEGURANÇA DO TRABALHO - COLABORADOR INTERNO")
        with st.form("form_seg_int"):
            aud = st.selectbox("Auditor interno responsável", auditores)
            obr = st.selectbox("Obra auditada", obras)
            nome = st.text_input("Nome de colaborador (Inserir nome completo)")
            cargo = st.text_input("Cargo")
            q1 = st.radio("O colaborador está usando os EPI's adequadamente?", sim_nao, horizontal=True)
            st.file_uploader("Imagem de colaborador: Mostrar EPI's em uso", type=["jpg", "png", "jpeg"])
            q2 = st.radio("O colaborador tem ficha de entrega de EPI de acordo com o PGR", sim_nao, horizontal=True)
            epis = st.text_input("Quais os EPI's que o colaborador está usando?")
            q3 = st.radio("Solicitar o registro de batida de ponto no dia da auditoria. O colaborador bateu o ponto?", sim_nao, horizontal=True)
            q4 = st.radio("O colaborador possui ASO (Atestado de saúde ocupacional) e periódicos dentro do período de validade?", sim_nao, horizontal=True)
            q5 = st.radio("Solicitar o registro de entrega de cesta básica do último mês entregue. O colaborador recebeu a cesta básica?", sim_nao_na, horizontal=True)
            q6 = st.radio("Solicitar a técnica de segurança as OS (Ordem de serviço) para o serviço em execução. Há OS assinada?", sim_nao, horizontal=True)
            q7 = st.radio("O colaborador foi treinado na NR06 (Equipamento de proteção individual)?", sim_nao, horizontal=True)
            q8 = st.radio("O colaborador foi treinado na NR12 (Segurança no trabalho em máquinas e equipamentos)?", sim_nao_na, horizontal=True)
            q9 = st.radio("O colaborador foi treinado na NR18 (Segurança e saúde no trabalho na indústria da construção)?", sim_nao, horizontal=True)
            q10 = st.radio("O colaborador foi treinado na NR35 (Trabalho em altura)?", sim_nao_na, horizontal=True)
            obs = st.text_area("Observações importantes")
            if st.form_submit_button("SALVAR", use_container_width=True):
                df = pd.DataFrame([{"timestamp": datetime.now(), "auditor": aud, "obra": obr, "nome": nome, "cargo": cargo, "q1": q1, "q2": q2, "epis": epis, "q3": q3, "q4": q4, "q5": q5, "q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10, "obs": obs}])
                conn.create(worksheet="auditoria_seg_int", data=df)
                st.success("Salvo com sucesso!")

    elif escolha == "Qualidade":
        st.header("SETOR DE QUALIDADE")
        with st.form("form_qual"):
            aud = st.selectbox("Auditor interno responsável", auditores)
            obr = st.selectbox("Obra auditada", obras)
            nome = st.text_input("Nome do colaborador (Inserir nome completo)")
            cargo = st.selectbox("Cargo", ["Profissional", "Servente", "Administrativo"])
            ativ = st.text_input("Atividade desenvolvida no momento da auditoria")
            q1 = st.radio("Foi aberta a FVS (Ficha de Verificação de Serviço) para conferir o serviço executado?", ["Sim", "Não", "Sim, porém incompleto"], horizontal=True)
            local = st.text_input("Local onde está sendo executado o serviço")
            q2 = st.radio("O colaborador foi treinado para executar o serviço através do PES (Procedimento de execução de serviço)?", sim_nao, horizontal=True)
            q3 = st.radio("Há NC (Não conformidade) para a FVS aberta?", ["Sim", "Não", "Não foi aberta a FVS", "Falta conferência do serviço"], horizontal=True)
            q4 = st.radio("Houve plano de ação para tratar a NC identificada?", ["Sim", "Não", "Não houve NC"], horizontal=True)
            if st.form_submit_button("SALVAR", use_container_width=True):
                df = pd.DataFrame([{"timestamp": datetime.now(), "auditor": aud, "obra": obr, "nome": nome, "cargo": cargo, "ativ": ativ, "fvs": q1, "local": local, "pes": q2, "nc": q3, "plano": q4}])
                conn.create(worksheet="auditoria_qualidade", data=df)
                st.success("Salvo com sucesso!")

