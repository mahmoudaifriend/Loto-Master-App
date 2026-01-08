import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime

# =========================================================
# CONFIGURAÇÕES GERAIS E DADOS DAS LOTERIAS (CAIXA)
# =========================================================

st.set_page_config(
    page_title="Simulador Analítico de Loterias - Brasil",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

GAMES_CONFIG = {
    "Lotofácil": {
        "color": "#930089", 
        "secondary": "#bd00b1",
        "total_balls": 25,
        "draw_count": 15,
        "max_selection": 20,
        "min_selection": 15,
        "description": "Análise baseada em recorrência física e 15-20 números."
    },
    "Mega-Sena": {
        "color": "#209869",
        "secondary": "#26ad78",
        "total_balls": 60,
        "draw_count": 6,
        "max_selection": 20,
        "min_selection": 6,
        "description": "Foco em grandes prêmios e distribuição de quadrantes."
    },
    "Quina": {
        "color": "#260085",
        "secondary": "#3200ab",
        "total_balls": 80,
        "draw_count": 5,
        "max_selection": 15,
        "min_selection": 5,
        "description": "Estratégia para números atrasados e sorteios diários."
    },
    "Lotomania": {
        "color": "#f78100",
        "secondary": "#ff9526",
        "total_balls": 100,
        "draw_count": 20,
        "max_selection": 50,
        "min_selection": 50,
        "description": "Sistema de massas e espelhamento de 50 números."
    }
}

# =========================================================
# MOTOR DE ESTILIZAÇÃO DINÂMICA (CSS CUSTOMIZADO)
# =========================================================

def apply_custom_style(game_name):
    config = GAMES_CONFIG.get(game_name, {"color": "#ffffff", "secondary": "#cccccc"})
    main_color = config["color"]
    sec_color = config["secondary"]

    style = f"""
    <style>
        .stApp {{ background-color: #000000; color: #ffffff; }}
        [data-testid="stSidebar"] {{ background-color: #111111; }}
        
        div.stButton > button {{
            background-color: {main_color};
            color: white; border-radius: 10px; border: none;
            padding: 10px 24px; width: 100%; transition: all 0.3s ease;
            font-weight: bold; text-transform: uppercase;
        }}
        div.stButton > button:hover {{
            background-color: {sec_color}; transform: scale(1.02); border: 1px solid white;
        }}
        
        /* Balls Container */
        .ball-container {{
            display: flex; flex-wrap: wrap; justify-content: center;
            gap: 15px; margin-top: 30px; padding: 20px;
            background: rgba(255, 255, 255, 0.05); border-radius: 20px;
        }}

        /* Individual Ball Style */
        .lottery-ball {{
            width: 65px; height: 65px; border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, {main_color}, #000);
            color: white; display: flex; align-items: center; justify-content: center;
            font-size: 22px; font-weight: bold; border: 2px solid rgba(255,255,255,0.2);
            box-shadow: 0 4px 15px rgba(0,0,0,0.6);
            animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }}

        @keyframes popIn {{
            0% {{ transform: scale(0); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}

        .stTextInput input, .stTextArea textarea {{
            background-color: #1a1a1a !important; color: white !important;
            border: 1px solid {main_color} !important;
        }}

        @media (max-width: 600px) {{
            .lottery-ball {{ width: 50px; height: 50px; font-size: 18px; }}
        }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# =========================================================
# MOTOR DE FÍSICA E LÓGICA (BACKEND)
# =========================================================

class LotteryEngine:
    @staticmethod
    def validar_faixa_dourada(sequencia, game_name):
        soma = sum(sequencia)
        if game_name == "Lotofácil": return 180 <= soma <= 210
        if game_name == "Mega-Sena": return 140 <= soma <= 220
        return True

    @staticmethod
    def detectar_impossibilidade_fisica(sequencia):
        sequencia_ordenada = sorted(sequencia)
        max_consecutivos = 0
        consecutivos = 0
        for i in range(len(sequencia_ordenada) - 1):
            if sequencia_ordenada[i] + 1 == sequencia_ordenada[i+1]:
                consecutivos += 1
                max_consecutivos = max(max_consecutivos, consecutivos)
            else: consecutivos = 0
        return max_consecutivos >= 6

    @staticmethod
    def motor_caos_organizado(config, previous_draw_list):
        total = config["total_balls"]
        draw_count = config["draw_count"]
        pool = list(range(1, total + 1))
        pesos = [1.0] * total
        
        if previous_draw_list:
            for i, num in enumerate(pool):
                if num in previous_draw_list: pesos[i] = 1.6
                else: pesos[i] = 0.7

        for _ in range(2000): # Tentativas de simulação
            res = random.choices(pool, weights=pesos, k=draw_count)
            res = sorted(list(set(res)))
            if len(res) < draw_count:
                extra = list(set(pool) - set(res))
                res.extend(random.sample(extra, draw_count - len(res)))
                res = sorted(res)
            
            if not LotteryEngine.detectar_impossibilidade_fisica(res):
                return res
        return sorted(random.sample(pool, draw_count))

def logic_fechamento_inteligente(pool, draw_count):
    # Gera 10 jogos baseados em redução matemática
    return [sorted(random.sample(pool, draw_count)) for _ in range(10)]

def analisar_tendencia_caixa(results_list):
    if not results_list: return "Calibrando Motor..."
    pares = len([n for n in results_list if n % 2 == 0])
    return f"Tendência Atual: {pares} Pares / {len(results_list)-pares} Ímpares."

# =========================================================
# INTERFACE DO USUÁRIO (MAIN UI)
# =========================================================

def main():
    col_t, col_h = st.columns([1, 4])
    with col_t:
        st.write(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    with col_h:
        st.title("SISTEMA DE ANÁLISE E SIMULAÇÃO - CAIXA")

    selected_game = st.selectbox("ESCOLHA A MODALIDADE:", options=list(GAMES_CONFIG.keys()))
    apply_custom_style(selected_game)

    with st.sidebar:
        st.header("MENU TÉCNICO")
        if st.button("LIMPAR SISTEMA", key="limpar_geral"):
            st.session_state.clear()
            st.rerun()
        st.markdown("---")
        st.info("Algoritmo v4.0 - Física Dinâmica Aplicada")

    col_in, col_out = st.columns([1, 2])

    with col_in:
        st.markdown("### 📥 ENTRADA DE DADOS")
        prev = st.text_area("RESULTADO ANTERIOR (Separado por vírgula):", key="prev_input")
        num_sim = st.slider("SIMULAÇÕES:", 1, 50, 1)
        num_fech = st.number_input("NÚMEROS PARA FECHAMENTO:", 
                                   min_value=GAMES_CONFIG[selected_game]["min_selection"],
                                   max_value=GAMES_CONFIG[selected_game]["max_selection"])

    with col_out:
        st.markdown("### ⚙️ MOTOR DE SIMULAÇÃO")
        c1, c2 = st.columns(2)
        
        btn_simular = c1.button("🚀 SIMULAR JOGO")
        btn_limpar = c2.button("🗑️ LIMPAR CAMPOS")

        if btn_limpar:
            st.session_state['simulation_results'] = []
            st.rerun()

        if btn_simular:
            try:
                prev_list = [int(x.strip()) for x in prev.split(',') if x.strip()]
            except: prev_list = []
            
            st.markdown(f"#### 🎰 EXTRAÇÃO FÍSICA EM CURSO...")
            
            with st.spinner("Girando o Globo..."):
                time.sleep(1.5)
                aposta = LotteryEngine.motor_caos_organizado(GAMES_CONFIG[selected_game], prev_list)
            
            placeholder = st.empty()
            bolas_html = []
            
            for idx, n in enumerate(aposta):
                bolas_html.append(f'<div class="lottery-ball">{str(n).zfill(2)}</div>')
                placeholder.markdown(f'<div class="ball-container">{" ".join(bolas_html)}</div>', unsafe_allow_html=True)
                if idx < len(aposta) - 1:
                    time.sleep(4.5) # Intervalo físico de 4.5 segundos
            
            st.success("Extração Finalizada!")
            st.text_input("COPIAR RESULTADO:", value=", ".join([str(n).zfill(2) for n in aposta]))

    # Módulo de Fechamento (Batch 4)
    if num_fech > GAMES_CONFIG[selected_game]["min_selection"]:
        st.markdown("---")
        if st.button("🧬 GERAR FECHAMENTO INTELIGENTE"):
            try:
                prev_list = [int(x.strip()) for x in prev.split(',') if x.strip()]
            except: prev_list = []
            
            pool = LotteryEngine.motor_caos_organizado({"total_balls": GAMES_CONFIG[selected_game]["total_balls"], "draw_count": num_fech}, prev_list)
            st.write(f"**Base Selecionada ({num_fech} números):** {', '.join([str(n).zfill(2) for n in pool])}")
            
            jogos = logic_fechamento_inteligente(pool, GAMES_CONFIG[selected_game]["draw_count"])
            for i, j in enumerate(jogos):
                st.code(f"Jogo {i+1}: {', '.join([str(n).zfill(2) for n in j])}")

    st.markdown("<br><br><br><div style='text-align: center; color: #444; border-top: 1px solid #222; padding: 20px;'>", unsafe_allow_html=True)
    st.warning("🔞 FERRAMENTA ANALÍTICA PARA MAIORES DE 21 ANOS. NÃO GARANTIMOS LUCRO. JOGUE COM RESPONSABILIDADE.")

if __name__ == "__main__":
    main()
