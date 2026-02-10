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
        st.markdown("")
        st.image("assets/logo.png", use_container_width=True)
        st.markdown("")
        st.markdown("""
            <div class="sidebar-logo-container">
                <div class="sidebar-logo-text">QUALIDADE</div>
                <div class="sidebar-logo-sub">Formulários de Auditoria</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        escolha = option_menu(
            "Formulários",
            ["Canteiro", "Estoque", "Habite-se", "Seg. Documental", "Seg. Externo", "Seg. Interno", "Qualidade", "Acompanhamento", "Dashboards"],
            icons=["building", "box", "clipboard-check", "file-earmark-lock", "person-up", "person-gear", "patch-check", "list", "bar-chart-fill" ],
            styles={
                "container": {"padding": "0!important", "background": "transparent"},
                "nav-link": {"color": "#aaa", "font-size": "0.9rem", "margin":"6px", "text-align": "left"},
                "nav-link-selected": {
                    "background-color": "rgba(227, 112, 38, 0.15)", 
                    "color": "#E37026", 
                    "border-left": "3px solid #E37026"
                },
                "icon": {"font-size": "1.1rem"}
            }
        )

    if escolha == "Canteiro":
        st.header("CANTEIRO E ESCRITÓRIO DE OBRAS", divider="orange")
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
            q10 = st.radio("As máquinas e equipamentos (Bancada de serra, betoneira, guincho, etc) em uso estão em boas condições de funcionamento?", sim_nao_na, horizontal=True)
            q11 = st.radio("As instalações provisórias de canteiro estão em conformidade de segurança?", sim_nao, horizontal=True)
            q12 = st.radio("A obra possui extintores nas áreas exigidas por norma?", sim_nao, horizontal=True)
            st.subheader("ESCRITÓRIO DE OBRA")
            q13 = st.radio("Há na obra escritório onde a equipe técnica possa monitorar o progresso do projeto e acompanhar as demandas?", sim_nao, horizontal=True)
            q14 = st.radio("Há no escritório painel de gestão a vista com restrições e planejamentos de longo, médio e curto prazo?", sim_nao, horizontal=True)
            q15 = st.radio("Há registro atualizado (até o dia anterior à auditoria) no diário de obra?", sim_nao, horizontal=True)
            q16 = st.radio("O diário de obras está preenchido de forma completa (com frentes de serviço, mão de obra, e legendas nas imagens)", sim_nao, horizontal=True)
            q17 = st.radio("Há plano semanal atualizado no drive da obra?", sim_nao, horizontal=True)
            obs = st.text_area("Observações")
            if st.form_submit_button("SALVAR", use_container_width=True, type="primary"):
                df_old = conn.read(worksheet="auditoria_canteiro", ttl=0)
                novo_dado = pd.DataFrame([{
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "auditor": aud, "obra": obr, "epi_visitantes": q1, "kit_primeiros_socorros": q2,
                    "sinalizacao_advertencia": q3, "placas_orientacao": q4, "areas_vivencia_limpeza": q5,
                    "canteiro_limpeza": q6, "escadas_seguras": q7, "barreiras_guarda_corpo": q8,
                    "protecao_queda_objetos": q9, "maquinas_equipamentos": q10, "instalacoes_provisorias": q11,
                    "extintores_norma": q12, "escritorio_monitoramento": q13, "painel_gestao": q14,
                    "diario_obra_atualizado": q15, "diario_obra_completo": q16, "plano_semanal_drive": q17,
                    "observacoes": obs
                }])
                df_final = pd.concat([df_old, novo_dado], ignore_index=True)
                conn.update(worksheet="auditoria_canteiro", data=df_final)
                st.success("Salvo com sucesso!")

    elif escolha == "Estoque":
        st.header("ESTOQUE", divider="orange")
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
            if st.form_submit_button("SALVAR", use_container_width=True, type="primary"):
                df_old = conn.read(worksheet="auditoria_estoque", ttl=0)
                novo_dado = pd.DataFrame([{
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "auditor": aud, "obra": obr, "grupo_insumo": grupo, "insumo_especifico": especifico,
                    "fvm_preenchida": q1, "nc_fvm_prazo": q2, "nf_numero": nf_num, "nf_prazo_lancamento": q3,
                    "armazenamento_tam": q4, "identificacao_tam": q6, "observacoes": obs
                }])
                df_final = pd.concat([df_old, novo_dado], ignore_index=True)
                conn.update(worksheet="auditoria_estoque", data=df_final)
                st.success("Salvo com sucesso!")

    elif escolha == "Habite-se":
        st.header("HABITE-SE", divider="orange")
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
            if st.form_submit_button("SALVAR", use_container_width=True, key="tip", type="primary"):
                df_old = conn.read(worksheet="auditoria_habitese", ttl=0)
                novo_dado = pd.DataFrame([{
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "auditor": aud, "obra": obr,
                    "placa_obra": q1, "projetos_disponiveis": q2, "arts_rrts_vigentes": q3, "afastamentos_projeto": q4,
                    "altura_projeto": q5, "aumento_area_nao_aprovado": q6, "taxas_ocupacao_permeabilidade": q7,
                    "estrutura_finalizada": q8, "revestimentos_acabados": q9, "itens_seguranca_instalados": q10,
                    "acessibilidade_executada": q11, "energia_definitiva": q12, "agua_esgoto": q13, "drenagens_executadas": q14,
                    "instalacoes_gas": q15, "rotas_fuga": q16, "extintores_projeto": q17, "extintores_validade": q18,
                    "sinalizacao_emergencia": q19, "calcada_projeto": q20, "vagas_garagem": q21, "acesso_imovel": q22,
                    "paisagismo": q23, "acumulo_residuos": q24, "destinacao_residuos": q25, "ligacoes_irregulares": q26,
                    "combate_incendio_testado": q27, "elevadores_conformidade": q28, "reservatorios_agua": q29
                }])
                df_final = pd.concat([df_old, novo_dado], ignore_index=True)
                conn.update(worksheet="auditoria_habitese", data=df_final)
                st.success("Salvo com sucesso!")

    elif escolha == "Seg. Documental":
        st.header("4. SEGURANÇA DO TRABALHO - DOCUMENTAL", divider="orange")
        with st.form("form_seg_doc"):
            aud = st.selectbox("Auditor interno responsável *", auditores)
            obr = st.selectbox("Obra auditada *", obras)

            st.subheader("Documentação Técnica e Programas")
            pgr = st.radio("Há PGR (Programa de Gerenciamento de Riscos) em obra? (Solicitar evidência) ", sim_nao, horizontal=True)
            pcmso = st.radio("Há PCMSO (Programa de Controle Médico de Saúde Ocupacional) em obra? (Solicitar evidência) ", sim_nao, horizontal=True)
            art_seg = st.radio("Há ART (Anotação de Responsabilidade Técnica) de segurança em obra? (Solicitar evidência) ", sim_nao, horizontal=True)
            art_exc = st.radio("Há ART de execução de obra e canteiro de obra? (Solicitar evidência) ", sim_nao, horizontal=True)
            art_cant = st.radio("Há ART e projeto de canteiro da obra (Atualizado)? (Solicitar evidência) ", sim_nao, horizontal=True)
            art_ele = st.radio("Há ART e projeto elétrico de canteiro da obra (Atualizado)? (Solicitar evidência) ", sim_nao, horizontal=True)
            art_inc = st.radio("Há ART e projeto de incêndio de canteiro da obra (Atualizado)? (Solicitar evidência) ", sim_nao, horizontal=True)
            spda = st.radio("Há projeto de SPDA (Sistema de proteção contra descarga atmosférica) ou laudo de despensa? (Solicitar evidência) ", sim_nao, horizontal=True)
            ergonomia = st.radio("Há relatório de análise ergonômica? (Solicitar evidência) ", sim_nao, horizontal=True)
            pca = st.radio("Há PCA (Programa de Proteção Auditiva)? (Solicitar evidência) ", sim_nao, horizontal=True)
            ppr = st.radio("Há PPR (Programa de Proteção Respiratória)? (Solicitar evidência) ", sim_nao, horizontal=True)
            mte = st.radio("Há comunicação prévia de início de obra cadastrado no MTE? (Solicitar evidência) ", sim_nao, horizontal=True)
            mapa_risco = st.radio("Há Mapa de risco aplicado ao canteiro? (Solicitar evidência) ", sim_nao, horizontal=True)
            cno = st.radio("Há CNO (Cadastro Nacional de Obra) - Receita Federal? (Solicitar evidência) ", sim_nao, horizontal=True)
        
            st.subheader("Laudos de Máquinas e Equipamentos")
            serra = st.radio("Há laudo de conformidade de instalação de Bancada de Serra? (Solicitar evidência) ", sim_nao_na, horizontal=True)
            betoneira = st.radio("Há laudo de conformidade de instalação de Betoneira? (Solicitar evidência) ", sim_nao_na, horizontal=True)
            grua = st.radio("Há laudo de conformidade de instalação de Grua? (Solicitar evidência) ", sim_nao_na, horizontal=True)
            cremalheira = st.radio("Há laudo de conformidade de instalação de Elevador Cremalheira? (Solicitar evidência) ", sim_nao_na, horizontal=True)
            policorte = st.radio("Há laudo de conformidade de Policorte? (Solicitar evidência) ", sim_nao_na, horizontal=True)
        
            obs_doc = st.text_area("Observações importantes")

            if st.form_submit_button("SALVAR", use_container_width=True, type="primary"):
                df_old = conn.read(worksheet="auditoria_seg_documental", ttl=0)
            
                novo_registro = pd.DataFrame([{
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "auditor": aud,
                    "obra": obr,
                    "pgr": pgr,
                    "pcmso": pcmso,
                    "art_seguranca": art_seg,
                    "art_execucao_canteiro": art_exc,
                    "art_projeto_canteiro": art_cant,
                    "art_projeto_eletrico": art_ele,
                    "art_projeto_incendio": art_inc,
                    "projeto_spda": spda,
                    "analise_ergonomica": ergonomia,
                    "pca": pca,
                    "ppr": ppr,
                    "comunicacao_mte": mte,
                    "mapa_risco": mapa_risco,
                    "cno": cno,
                    "laudo_serra": serra,
                    "laudo_betoneira": betoneira,
                    "laudo_grua": grua,
                    "laudo_cremalheira": cremalheira,
                    "laudo_policorte": policorte,
                    "observacoes": obs_doc
                }])
            
                df_final = pd.concat([df_old, novo_registro], ignore_index=True)
                conn.update(worksheet="auditoria_seg_documental", data=df_final)
                st.success("Auditoria documental salva com sucesso!")

    elif escolha == "Seg. Externo":
        st.header("SEGURANÇA DO TRABALHO - COLABORADOR EXTERNO", divider="orange")
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
            if st.form_submit_button("SALVAR", use_container_width=True, type="primary"):
                df_old = conn.read(worksheet="auditoria_seg_externo", ttl=0)
                novo_dado = pd.DataFrame([{
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "auditor": aud, "obra": obr,
                    "fornecedor": forn, "colaborador_nome": colab, "cargo": cargo, "pcmso_valido": q1,
                    "art_servico": q2, "ficha_epi": q3, "uso_epi_adequado": q4, "aso_validade": q5,
                    "os_assinada": q6, "treino_nr06": q7, "treino_nr12": q8, "treino_nr18": q9,
                    "treino_nr35": q10, "observacoes": obs
                }])
                df_final = pd.concat([df_old, novo_dado], ignore_index=True)
                conn.update(worksheet="auditoria_seg_externo", data=df_final)
                st.success("Salvo com sucesso!")

    elif escolha == "Seg. Interno":
        st.header("SEGURANÇA DO TRABALHO - COLABORADOR INTERNO", divider="orange")
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
            if st.form_submit_button("SALVAR", use_container_width=True, type="primary"):
                df_old = conn.read(worksheet="auditoria_seg_interno", ttl=0)
                novo_dado = pd.DataFrame([{
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "auditor": aud, "obra": obr,
                    "colaborador_nome": nome, "cargo": cargo, "uso_epi_adequado": q1, "url_imagem_epi": "",
                    "ficha_epi_pgr": q2, "quais_epis_uso": epis, "ponto_batido": q3, "aso_validade": q4,
                    "cesta_basica": q5, "os_assinada": q6, "treino_nr06": q7, "treino_nr12": q8,
                    "treino_nr18": q9, "treino_nr35": q10, "observacoes": obs
                }])
                df_final = pd.concat([df_old, novo_dado], ignore_index=True)
                conn.update(worksheet="auditoria_seg_interno", data=df_final)
                st.success("Salvo com sucesso!")

    elif escolha == "Qualidade":
        st.header("SETOR DE QUALIDADE", divider="orange")
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
            if st.form_submit_button("SALVAR", use_container_width=True, type="primary"):
                df_old = conn.read(worksheet="auditoria_qualidade", ttl=0)
                novo_dado = pd.DataFrame([{
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "auditor": aud, "obra": obr,
                    "colaborador_nome": nome, "cargo": cargo, "atividade_momento": ativ, "fvs_aberta": q1,
                    "local_servico": loc, "treino_pes": q2, "nc_fvs": q3, "plano_acao_nc": q4
                }])
                df_final = pd.concat([df_old, novo_dado], ignore_index=True)
                conn.update(worksheet="auditoria_qualidade", data=df_final)
                st.success("Salvo com sucesso!")

    elif escolha == "Acompanhamento":
        st.header("ACOMPANHAMENTO DE AUDITORIAS", divider="orange")
        
        abas_map = {
            "Canteiro": "auditoria_canteiro",
            "Estoque": "auditoria_estoque",
            "Habite-se": "auditoria_habitese",
            "Seg. Documental": "auditoria_seg_documental",
            "Seg. Externo": "auditoria_seg_externo",
            "Seg. Interno": "auditoria_seg_interno",
            "Qualidade": "auditoria_qualidade"
        }
        
        @st.dialog("Editar Registro")
        def dialog_editar(index_real, row_data, df_completo, nome_planilha):
            st.write(f"Editando registro de: **{row_data.get('obra', 'N/A')}**")
            st.caption(f"ID: {index_real} | Auditor: {row_data.get('auditor', 'N/A')}")
            
            novos_dados = {}
            cols = df_completo.columns.tolist()
            
            for col in cols:
                valor_atual = row_data[col]
                
                if col == "timestamp":
                    st.text_input(f"Data (Timestamp)", value=valor_atual, disabled=True, key=f"edit_{col}_{index_real}")
                    novos_dados[col] = valor_atual
                    continue

                if col == "auditor":
                    idx = auditores.index(valor_atual) if valor_atual in auditores else 0
                    novos_dados[col] = st.selectbox("Auditor", auditores, index=idx, key=f"sel_aud_{index_real}")
                
                elif col == "obra":
                    idx = obras.index(valor_atual) if valor_atual in obras else 0
                    novos_dados[col] = st.selectbox("Obra", obras, index=idx, key=f"sel_obr_{index_real}")

                elif str(valor_atual) in ["Sim", "Não", "Não se aplica"]:
                    opcoes = ["Sim", "Não", "Não se aplica"]
                    idx_sel = opcoes.index(valor_atual) if valor_atual in opcoes else 0
                    novos_dados[col] = st.selectbox(col.replace('_', ' ').title(), opcoes, index=idx_sel, key=f"sel_{col}_{index_real}")
                
                elif "observacoes" in col.lower() or len(str(valor_atual)) > 50:
                    novos_dados[col] = st.text_area(col.replace('_', ' ').title(), value=str(valor_atual), key=f"txt_{col}_{index_real}")
                
                else:
                    novos_dados[col] = st.text_input(col.replace('_', ' ').title(), value=str(valor_atual), key=f"inp_{col}_{index_real}")

            col_s1, col_s2 = st.columns(2)
            if col_s1.button("Salvar Alteracoes", type="primary", use_container_width=True):
                for k, v in novos_dados.items():
                    df_completo.at[index_real, k] = v
                
                try:
                    conn.update(worksheet=nome_planilha, data=df_completo)
                    st.toast("Registro atualizado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")

        @st.dialog("Confirmar Exclusao")
        def dialog_excluir(index_real, df_completo, nome_planilha):
            st.info("Tem certeza que deseja excluir este registro? Esta acao nao pode ser desfeita.")
            st.write(f"**Registro:** {df_completo.at[index_real, 'obra']} - {df_completo.at[index_real, 'timestamp']}")
            
            col_del1, col_del2 = st.columns(2)
            if col_del1.button("Sim, Excluir", type="primary", use_container_width=True):
                try:
                    df_final = df_completo.drop(index_real)
                    conn.update(worksheet=nome_planilha, data=df_final)
                    st.toast("Registro excluido com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir: {e}")
            
            if col_del2.button("Cancelar", use_container_width=True):
                st.rerun()

        form_ref = st.selectbox("Selecione o Formulario", list(abas_map.keys()))
        
        nome_worksheet = abas_map[form_ref]
        df_acompanhamento = conn.read(worksheet=nome_worksheet, ttl=0)

        if df_acompanhamento.empty:
            st.info("Nenhum dado encontrado.")
        else:
            col_f2, col_f3 = st.columns(2)
            obras_lista = sorted(df_acompanhamento["obra"].unique()) if "obra" in df_acompanhamento.columns else []
            auditores_lista = sorted(df_acompanhamento["auditor"].unique()) if "auditor" in df_acompanhamento.columns else []
            
            obra_f = col_f2.multiselect("Filtrar por Obra", options=obras_lista)
            auditor_f = col_f3.multiselect("Filtrar por Auditor", options=auditores_lista)
    
            df_view = df_acompanhamento.copy()
            if obra_f:
                df_view = df_view[df_view["obra"].isin(obra_f)]
            if auditor_f:
                df_view = df_view[df_view["auditor"].isin(auditor_f)]

            modo_visao = option_menu(None, ["Cards", "Tabela"], 
                icons=['grid-3x3-gap', 'table'], 
                default_index=0, orientation="horizontal",
                styles={
                    "container": {
                        "padding": "0!important", 
                        "background-color": "transparent",
                        "width": "100%",     
                        "max-width": "100%", 
                        "margin": "0"        
                    },
                    "icon": {"color": "white", "font-size": "16px"}, 
                    "nav-link": {
                        "font-size": "14px", 
                        "text-align": "center", 
                        "margin": "0px", 
                        "--hover-color": "rgba(227, 112, 38, 0.3)",
                        "color": "ffffff"
                    },
                    "nav-link-selected": {"background-color": "#E37026", "color": "white"},
                }
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if modo_visao == "Tabela":
                st.dataframe(df_view, use_container_width=True)
            else:
                if df_view.empty:
                    st.warning("Nenhum registro com os filtros selecionados.")
                
                for index, row in df_view.iterrows():
                    with st.container():
                        conteudo_card = ""
                        for col in df_view.columns:
                            val = row[col]
                            if pd.isna(val) or val == "": val = "-"
                            if len(str(val)) > 100: val = str(val)[:100] + "..."
                            
                            conteudo_card += f"<div style='margin-bottom: 4px;'><span style='color: #E37026; font-weight:600;'>{col.replace('_', ' ').title()}:</span> <span style='color: #ddd;'>{val}</span></div>"
        
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.03); padding: 20px; border-radius: 12px; border: 1px solid rgba(227, 112, 38, 0.2); margin-bottom: 10px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; margin-bottom: 10px;">
                                <span style="font-weight: bold; font-size: 1.1rem; color: #E37026;">{row.get('obra', 'OBRA')}</span>
                                <span style="font-size: 0.8rem; color: #888;">{row.get('timestamp', '')}</span>
                            </div>
                            <div style="font-size: 0.9rem; margin-bottom: 15px;">
                                {conteudo_card}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        c_edit, c_del = st.columns([1, 1])
                        
                        if c_edit.button("Editar", key=f"btn_edit_{index}", use_container_width=True):
                            dialog_editar(index, row, df_acompanhamento, nome_worksheet)
                            
                        if c_del.button("Excluir", key=f"btn_del_{index}", use_container_width=True):
                            dialog_excluir(index, df_acompanhamento, nome_worksheet)
                        
                        st.markdown("---")
    
    elif escolha == "Dashboards":
        import plotly.express as px
        import plotly.graph_objects as go
        from datetime import datetime
    
        st.header("DASHBOARD DE QUALIDADE E SEGURANÇA", divider="orange")
        
        abas_map = {
            "Canteiro": "auditoria_canteiro",
            "Estoque": "auditoria_estoque",
            "Seg. Documental": "auditoria_seg_documental",
            "Seg. Externo": "auditoria_seg_externo",
            "Seg. Interno": "auditoria_seg_interno",
            "Qualidade": "auditoria_qualidade"
        }
    
        escala_lavie = [[0, "rgb(139, 0, 0)"], [0.5, "rgb(0, 0, 0)"], [1, "rgb(0, 100, 0)"]]
    
        def calc_score(df):
            if df.empty: return 0.0
            cols_meta = ['timestamp', 'auditor', 'obra', 'observacoes', 'fornecedor', 'colaborador_nome', 'cargo', 'atividade_momento', 'local_servico', 'url_imagem_epi', 'quais_epis_uso', 'insumo_especifico', 'nf_numero', 'grupo_insumo']
            cols_q = [c for c in df.columns if c in df.columns and c not in cols_meta]
            if not cols_q: return 0.0
            vals = df[cols_q].astype(str).apply(lambda x: x.str.strip().str.lower())
            sim = (vals == 'sim').sum().sum()
            nao = (vals == 'não').sum().sum()
            if (sim + nao) == 0: return 0.0
            return (sim / (sim + nao)) * 100
    
        scores = {}
        total_audits = 0
        total_nao_conformidades = 0
        audits_mes_atual = 0
        auditor_counts = {}
        obras_scores = {}
        all_data = {}
        
        mes_atual_str = datetime.now().strftime("%Y-%m")
    
        for nome, ws in abas_map.items():
            try:
                data = conn.read(worksheet=ws, ttl=0)
                if data.empty:
                    all_data[nome] = pd.DataFrame()
                    scores[nome] = 0.0
                else:
                    all_data[nome] = data
                    scores[nome] = calc_score(data)
                    total_audits += len(data)
                    
                    cols_meta = ['timestamp', 'auditor', 'obra', 'observacoes', 'fornecedor', 'colaborador_nome', 'cargo', 'atividade_momento', 'local_servico', 'url_imagem_epi', 'quais_epis_uso', 'insumo_especifico', 'nf_numero', 'grupo_insumo']
                    cols_q = [c for c in data.columns if c not in cols_meta]
                    vals = data[cols_q].astype(str).apply(lambda x: x.str.strip().str.lower())
                    total_nao_conformidades += (vals == 'não').sum().sum()
    
                    if 'timestamp' in data.columns:
                        data['dt_mes'] = pd.to_datetime(data['timestamp'], dayfirst=True, errors='coerce').dt.to_period('M').astype(str)
                        audits_mes_atual += len(data[data['dt_mes'] == mes_atual_str])
    
                    if 'auditor' in data.columns:
                        vc = data['auditor'].value_counts().to_dict()
                        for aud, count in vc.items():
                            auditor_counts[aud] = auditor_counts.get(aud, 0) + count
                    
                    if 'obra' in data.columns:
                        for ob in data['obra'].unique():
                            s = calc_score(data[data['obra'] == ob])
                            if ob not in obras_scores:
                                obras_scores[ob] = []
                            obras_scores[ob].append(s)
    
            except Exception:
                all_data[nome] = pd.DataFrame()
                scores[nome] = 0.0
    
        avg_score = sum(scores.values()) / len(scores) if scores else 0
        
        dfs_para_contagem = [df['obra'] for df in all_data.values() if not df.empty]
        todas_obras_df = pd.concat(dfs_para_contagem) if dfs_para_contagem else pd.Series()
        obras_unicas = sorted(todas_obras_df.unique()) if not todas_obras_df.empty else []
        
        obra_critica = "-"
        menor_nota = 100.0
        for ob, notas in obras_scores.items():
            media_ob = sum(notas)/len(notas) if notas else 0
            if media_ob < menor_nota:
                menor_nota = media_ob
                obra_critica = ob
    
        top_auditor = max(auditor_counts, key=auditor_counts.get) if auditor_counts else "-"
    
        st.markdown("""
        <style>
        .kpi-card {
            background: linear-gradient(100deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%);
            border: 1px solid rgba(227, 112, 38, 0.2);
            border-radius: 10px;
            padding: 10px;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, border-color 0.3s ease;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .kpi-card:hover {
            border-color: rgba(227, 112, 38, 0.6);
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.05);
        }
        .kpi-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: #E37026;
        }
        .kpi-title {
            color: #aaa;
            font-size: 0.75rem;
            font-weight: 450;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 5px;
        }
        .kpi-value {
            color: #fff;
            font-size: 1.8rem;
            font-weight: 600;
            margin: 0px 0;
            padding: 5px;
        }
        .kpi-sub {
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.75rem;
            padding: 5px;
        }
        .kpi-icon {
            position: absolute;
            right: 0px;
            top: 0px;
            color: rgba(227, 112, 38, 0.1);
            font-size: 1rem;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
        def card(title, value, sub, icon_char):
            return f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon_char}</div>
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-sub">{sub}</div>
            </div>
            """
    
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(card("Total Auditorias", total_audits, "Histórico completo", ""), unsafe_allow_html=True)
        with c2: st.markdown(card("Conformidade Média", f"{avg_score:.1f}%", "Média global ponderada", ""), unsafe_allow_html=True)
        with c3: st.markdown(card("Auditorias (Mês)", audits_mes_atual, f"Referente a {datetime.now().strftime('%m/%Y')}", ""), unsafe_allow_html=True)
        with c4: st.markdown(card("Não Conformidades", total_nao_conformidades, "Itens reprovados (Risco)", ""), unsafe_allow_html=True)
    
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
    
        c5, c6, c7, c8 = st.columns(4)
        with c5: st.markdown(card("Obras Ativas", len(obras_unicas), "Unidades auditadas", ""), unsafe_allow_html=True)
        with c6: st.markdown(card("Setores", len([d for d in all_data.values() if not d.empty]), "Áreas monitoradas", ""), unsafe_allow_html=True)
        with c7: st.markdown(card("Obra em Alerta", obra_critica, f"Menor nota: {menor_nota:.1f}%", ""), unsafe_allow_html=True)
        with c8: st.markdown(card("Auditor", top_auditor, "Maior volume de registros", ""), unsafe_allow_html=True)
    
        st.markdown("---")
        st.subheader("Visão Geral")
        
        st.markdown("##### Evolução Mensal de Conformidade")
        evo_list = []
        for nome_setor, df_s in all_data.items():
            if not df_s.empty and 'timestamp' in df_s.columns:
                temp_dates = pd.to_datetime(df_s['timestamp'], dayfirst=True, errors='coerce')
                
                df_valid = df_s[temp_dates.notna()].copy()
                
                if not df_valid.empty:
                    df_valid['dt'] = temp_dates[temp_dates.notna()].dt.to_period('M').astype(str)
                    
                    for mes in sorted(df_valid['dt'].unique()):
                        df_mes = df_valid[df_valid['dt'] == mes]
                        score_mes = calc_score(df_mes)
                        evo_list.append({'Mês': mes, 'Setor': nome_setor, 'Conformidade': score_mes})
        
        if evo_list:
            df_evo = pd.DataFrame(evo_list).sort_values('Mês')
            fig_evo = px.line(df_evo, x='Mês', y='Conformidade', color='Setor', markers=True,
                             template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Prism)
            fig_evo.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis_range=[0, 115])
            st.plotly_chart(fig_evo, use_container_width=True)
        else:
            st.info("Dados insuficientes para gerar evolução temporal.")
    
        c1, c2 = st.columns([6, 4])
        
        with c1:
            st.markdown("##### Índice de Conformidade por Setor")
            df_scores = pd.DataFrame(list(scores.items()), columns=['Setor', 'Conformidade'])
            fig_bar = px.bar(df_scores, x='Setor', y='Conformidade', text_auto='.1f',
                            color='Conformidade', color_continuous_scale='RdBu',
                            template="plotly_dark")
            fig_bar.update_traces(textposition='outside')
            fig_bar.update_layout(yaxis_range=[0, 115], plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
    
        with c2:
            st.markdown("##### Volume de Auditorias")
            audit_dist = pd.DataFrame([{'Setor': k, 'Quantidade': len(v)} for k, v in all_data.items() if not v.empty])
            if not audit_dist.empty:
                fig_pie = px.pie(audit_dist, names='Setor', values='Quantidade', hole=0.4,
                                template="plotly_dark", color_discrete_sequence=px.colors.sequential.Oranges_r)
                fig_pie.update_traces(textinfo='value+percent')
                fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_pie, use_container_width=True)
    
        st.markdown("---")
    
        st.subheader("Análise Detalhada por Setor")
        setor_sel = st.selectbox("Selecione o Setor", list(abas_map.keys()))
        df_setor = all_data.get(setor_sel, pd.DataFrame())
        
        if not df_setor.empty:
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                st.markdown(f"##### Conformidade por Obra ({setor_sel})")
                conf_obra = []
                if 'obra' in df_setor.columns:
                    for ob in df_setor['obra'].unique():
                        val = calc_score(df_setor[df_setor['obra'] == ob])
                        conf_obra.append({'Obra': ob, 'Conformidade': val})
                    df_conf_ob = pd.DataFrame(conf_obra)
                    fig_ob = px.bar(df_conf_ob, x='Obra', y='Conformidade', text_auto='.1f',
                                   color='Conformidade', color_continuous_scale='RdBu', template="plotly_dark")
                    fig_ob.update_traces(textposition='outside')
                    fig_ob.update_layout(yaxis_range=[0, 115], plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_ob, use_container_width=True)
                
            with col_d2:
                st.markdown(f"##### Ranking de Requisitos ({setor_sel})")
                cols_meta = ['timestamp', 'auditor', 'obra', 'observacoes', 'fornecedor', 'colaborador_nome', 'cargo', 'atividade_momento', 'local_servico', 'url_imagem_epi', 'quais_epis_uso', 'insumo_especifico', 'nf_numero', 'grupo_insumo']
                qs = [c for c in df_setor.columns if c not in cols_meta]
                item_scores = []
                for q in qs:
                    s = (df_setor[q].astype(str).str.strip().str.lower() == 'sim').sum()
                    n = (df_setor[q].astype(str).str.strip().str.lower() == 'não').sum()
                    if (s + n) > 0:
                        perc = (s / (s + n) * 100)
                        item_scores.append({'Requisito': q, 'Conformidade': perc})
                
                if item_scores:
                    df_items = pd.DataFrame(item_scores).sort_values('Conformidade', ascending=True)
                    fig_items = px.bar(df_items, y='Requisito', x='Conformidade', orientation='h', text_auto='.1f',
                                      color='Conformidade', color_continuous_scale='RdBu', template="plotly_dark")
                    fig_items.update_traces(textposition='outside')
                    fig_items.update_layout(xaxis_range=[0, 115], plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_items, use_container_width=True)
                else:
                    st.info("Nenhum requisito avaliado encontrado.")
        else:
            st.warning(f"Sem dados para o setor {setor_sel}.")
    
        st.markdown("---")
    
        st.subheader("Análise Detalhada por Obra")
        if obras_unicas:
            obra_sel = st.selectbox("Selecione a Obra", obras_unicas)
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                st.markdown(f"##### Conformidade por Setor ({obra_sel})")
                conf_setor_obra = []
                for nome_setor, df_s in all_data.items():
                    if not df_s.empty and 'obra' in df_s.columns and obra_sel in df_s['obra'].values:
                        val = calc_score(df_s[df_s['obra'] == obra_sel])
                        conf_setor_obra.append({'Setor': nome_setor, 'Conformidade': val})
                
                df_conf_so = pd.DataFrame(conf_setor_obra)
                if not df_conf_so.empty:
                    fig_so = px.bar(df_conf_so, x='Setor', y='Conformidade', text_auto='.1f',
                                   color='Conformidade', color_continuous_scale='RdBu', template="plotly_dark")
                    fig_so.update_traces(textposition='outside')
                    fig_so.update_layout(yaxis_range=[0, 115], plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_so, use_container_width=True)
                else:
                    st.info("Esta obra não possui registros em nenhum setor.")
    
            with col_e2:
                st.markdown(f"##### Ranking Geral de Requisitos ({obra_sel})")
                resumo_reqs = []
                cols_meta = ['timestamp', 'auditor', 'obra', 'observacoes', 'fornecedor', 'colaborador_nome', 'cargo', 'atividade_momento', 'local_servico', 'url_imagem_epi', 'quais_epis_uso', 'insumo_especifico', 'nf_numero', 'grupo_insumo']
                
                for df_s in all_data.values():
                    if not df_s.empty and 'obra' in df_s.columns and obra_sel in df_s['obra'].values:
                        df_filtrado = df_s[df_s['obra'] == obra_sel]
                        qs = [c for c in df_filtrado.columns if c not in cols_meta]
                        for q in qs:
                            s = (df_filtrado[q].astype(str).str.strip().str.lower() == 'sim').sum()
                            n = (df_filtrado[q].astype(str).str.strip().str.lower() == 'não').sum()
                            if (s + n) > 0:
                                resumo_reqs.append({'Requisito': q, 'Sim': s, 'Nao': n})
                
                if resumo_reqs:
                    df_req_obra = pd.DataFrame(resumo_reqs).groupby('Requisito').sum().reset_index()
                    df_req_obra['Conformidade'] = (df_req_obra['Sim'] / (df_req_obra['Sim'] + df_req_obra['Nao'])) * 100
                    df_req_obra = df_req_obra.sort_values('Conformidade', ascending=True).head(20)
                    
                    fig_req_ob = px.bar(df_req_obra, y='Requisito', x='Conformidade', orientation='h', text_auto='.1f',
                                       color='Conformidade', color_continuous_scale='RdBu', template="plotly_dark")
                    fig_req_ob.update_traces(textposition='outside')
                    fig_req_ob.update_layout(xaxis_range=[0, 115], plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig_req_ob, use_container_width=True)
                else:
                    st.info("Nenhum requisito avaliado para esta obra.")
        else:
            st.warning("Nenhuma obra encontrada na base de dados.")
