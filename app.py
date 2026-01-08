import streamlit as st
import pandas as pd
import time
import random
import plotly.graph_objects as go
from datetime import datetime

# --- SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Totoloto Algoritmia v6.0",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- GAME CONSTANTS (CAIXA BRASIL) ---
GAMES = {
    "Lotofácil": {
        "id": "lotofacil",
        "color": "#930089", 
        "gradient": "linear-gradient(180deg, #4b0046 0%, #000000 100%)",
        "total_balls": 25, 
        "draw_count": 15,
        "max_range": 20
    },
    "Mega-Sena": {
        "id": "mega-sena",
        "color": "#209869", 
        "gradient": "linear-gradient(180deg, #0d3d2a 0%, #000000 100%)",
        "total_balls": 60, 
        "draw_count": 6,
        "max_range": 20
    },
    "Quina": {
        "id": "quina",
        "color": "#260085", 
        "gradient": "linear-gradient(180deg, #11003d 0%, #000000 100%)",
        "total_balls": 80, 
        "draw_count": 5,
        "max_range": 15
    },
    "Lotomania": {
        "id": "lotomania",
        "color": "#f78100", 
        "gradient": "linear-gradient(180deg, #5e3100 0%, #000000 100%)",
        "total_balls": 100, 
        "draw_count": 20,
        "max_range": 50
    }
}

# --- ADVANCED PREMIUM CSS INJECTION ---
def inject_premium_styles(game_name):
    config = GAMES[game_name]
    primary = config["color"]
    bg_gradient = config["gradient"]
    
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
        
        /* Global Background & Font */
        .stApp {{
            background: {bg_gradient};
            font-family: 'Rajdhani', sans-serif;
            color: #ffffff;
        }}

        /* Header Title */
        .main-title {{
            font-family: 'Orbitron', sans-serif;
            color: #ff4b00;
            text-align: center;
            font-size: 3rem;
            text-shadow: 0 0 20px #ff4b00;
            margin-bottom: 0px;
        }}

        /* Central Globe (Globo) Animation */
        .globo-wrapper {{
            display: flex; justify-content: center; margin: 20px 0;
        }}
        .globo-sphere {{
            width: 180px; height: 180px;
            border: 4px solid {primary};
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.1), rgba(0,0,0,0.9));
            box-shadow: 0 0 40px {primary}, inset 0 0 30px {primary};
            display: flex; align-items: center; justify-content: center;
            position: relative;
        }}
        .globo-core {{
            width: 120px; height: 120px;
            border: 2px dashed rgba(255,255,255,0.4);
            border-radius: 50%;
            animation: spinGlobo 1.2s linear infinite;
        }}
        @keyframes spinGlobo {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}

        /* Premium 3D Balls */
        .ball-3d {{
            width: 55px; height: 55px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #ffffff 0%, {primary} 50%, #000000 100%);
            display: inline-flex; align-items: center; justify-content: center;
            color: white; font-family: 'Orbitron', sans-serif; font-size: 1.2rem;
            font-weight: bold; margin: 8px;
            box-shadow: 6px 6px 15px rgba(0,0,0,0.8), inset -3px -3px 10px rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.2);
            animation: ballPop 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275), ballRotate 1s ease-out;
        }}
        
        @keyframes ballPop {{
            0% {{ transform: scale(0); }}
            100% {{ transform: scale(1); }}
        }}
        @keyframes ballRotate {{
            0% {{ transform: rotateY(0deg); }}
            100% {{ transform: rotateY(360deg); }}
        }}

        /* Hidden Ball (Last One) */
        .ball-hidden {{
            width: 55px; height: 55px; border-radius: 50%;
            background: #1a1a1a; border: 2px dashed #444;
            display: inline-flex; align-items: center; justify-content: center;
            color: #ff4b00; font-size: 1.5rem; font-weight: bold; margin: 8px;
            text-shadow: 0 0 10px #ff4b00;
        }}

        /* Orange Premium Button */
        div.stButton > button {{
            background: linear-gradient(90deg, #ff4b00 0%, #ff8700 100%) !important;
            border: none; color: white; border-radius: 50px;
            font-family: 'Orbitron', sans-serif; font-size: 1.2rem;
            padding: 15px 30px; transition: 0.4s;
            box-shadow: 0 0 15px rgba(255, 75, 0, 0.6);
            width: 100%; text-transform: uppercase;
        }}
        div.stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 0 30px rgba(255, 75, 0, 0.9);
            color: white;
        }}

        /* Sidebar & Inputs */
        [data-testid="stSidebar"] {{ background: #050505; }}
        .stTextInput input, .stTextArea textarea {{
            background: #111 !important; color: {primary} !important;
            border: 1px solid {primary} !important; border-radius: 10px;
        }}
        
        /* Prediction Row */
        .bet-row {{
            background: rgba(255, 255, 255, 0.03);
            border-left: 4px solid {primary};
            padding: 15px; border-radius: 15px; margin-bottom: 10px;
            display: flex; align-items: center;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- ENGINE: LOGIC & PHYSICS ---
class TotolotoLogic:
    @staticmethod
    def calculate_sync_gauge(game_name):
        # Generates a pseudo-random sync percentage for UX
        return random.randint(72, 98)

    @staticmethod
    def generate_elite_bet(game_name, previous_draw_list):
        config = GAMES[game_name]
        pool = list(range(1, config["total_balls"] + 1))
        
        # Applying weights based on previous machine history
        weights = []
        for n in pool:
            if n in previous_draw_list: weights.append(1.5) # Hot numbers
            else: weights.append(0.8) # Cold numbers
            
        attempts = 0
        while attempts < 1000:
            selection = random.choices(pool, weights=weights, k=config["draw_count"])
            selection = sorted(list(set(selection)))
            
            if len(selection) == config["draw_count"]:
                # Logic: Golden Range Filter for Lotofácil
                if game_name == "Lotofácil":
                    if 180 <= sum(selection) <= 210: return selection
                else:
                    return selection
            attempts += 1
        return sorted(random.sample(pool, config["draw_count"]))

# --- MAIN INTERFACE ---
def main():
    # Top Bar: Logo and Master Clear
    col_header, col_reset = st.columns([10, 1])
    with col_header:
        st.markdown('<h1 class="main-title">TOTOLOTO ALGORITMIA</h1>', unsafe_allow_html=True)
    with col_reset:
        if st.button("🗑️", help="Limpar Todo o Cache"):
            st.session_state.clear()
            st.rerun()

    # Game Selection
    selected_game = st.selectbox(
        "MODALIDADE DE ANÁLISE:",
        options=list(GAMES.keys()),
        index=0
    )
    inject_premium_styles(selected_game)

    st.markdown("---")

    # Inputs Layout
    col_inputs, col_gauge = st.columns([2, 1])
    
    with col_inputs:
        st.markdown("### 📥 CONFIGURAÇÃO DO MOTOR")
        raw_prev = st.text_input("RESULTADO ANTERIOR (Ex: 01, 12, 15...):", placeholder="Obrigatório para sincronização...")
        num_bets = st.slider("QUANTIDADE DE JOGOS (SIMULAÇÃO):", 1, 50, 5)
        
    with col_gauge:
        # Gauge Chart for Probability Analysis
        sync_val = TotolotoLogic.calculate_sync_gauge(selected_game)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = sync_val,
            title = {'text': "SINCRONIA DA MÁQUINA", 'font': {'size': 18, 'family': 'Orbitron'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#ff4b00"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': GAMES[selected_game]["color"],
                'steps': [
                    {'range': [0, 50], 'color': '#333'},
                    {'range': [50, 100], 'color': '#111'}
                ],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Rajdhani"}, height=250, margin=dict(t=50, b=0, l=30, r=30))
        st.plotly_chart(fig, use_container_width=True)

    # The Visual Globo (Central Engine)
    st.markdown(f"""
        <div class="globo-wrapper">
            <div class="globo-sphere">
                <div class="globo-core"></div>
            </div>
        </div>
        <p style="text-align:center; color:#555; font-size:12px;">MOTOR DINÂMICO DE SUCÇÃO ATIVO</p>
    """, unsafe_allow_html=True)

    # SIMULATION ACTION (ORANGE BUTTON)
    if st.button("🚀 INICIAR SIMULAÇÃO SEQUENCIAL"):
        # Sound integration (Browser side)
        st.markdown('<audio autoplay><source src="https://www.soundjay.com/misc/sounds/bingo-ball-machine-1.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
        
        # Data preparation
        try:
            prev_list = [int(x.strip()) for x in raw_prev.split(',') if x.strip()]
        except:
            prev_list = []
            st.warning("Aviso: Sincronização rodando sem dados históricos...")

        draw_limit = GAMES[selected_game]["draw_count"]
        
        # 1. Generate all bets first in memory
        all_bets_data = []
        for _ in range(num_bets):
            all_bets_data.append(TotolotoLogic.generate_elite_bet(selected_game, prev_list))

        # 2. Sequential Animation (The requested logic)
        placeholders = [st.empty() for _ in range(num_bets)]
        visual_rows = [[] for _ in range(num_bets)]

        # Loop through each ball slot (1 to N)
        for ball_idx in range(draw_limit):
            # For each bet in the list
            for bet_idx in range(num_bets):
                
                # Hidden Ball Logic (Last one is "?")
                if ball_idx == draw_limit - 1:
                    ball_html = '<div class="ball-hidden">?</div>'
                else:
                    val = all_bets_data[bet_idx][ball_idx]
                    ball_html = f'<div class="ball-3d">{str(val).zfill(2)}</div>'
                
                visual_rows[bet_idx].append(ball_html)
                
                # Update the row live
                placeholders[bet_idx].markdown(
                    f"""<div class="bet-row">
                        <span style="color:{GAMES[selected_game]["color"]}; min-width:80px; font-weight:bold;">JOGO {bet_idx+1}:</span>
                        {' '.join(visual_rows[bet_idx])}
                    </div>""", 
                    unsafe_allow_html=True
                )
            
            # The 4.5 seconds delay between BALL SESSIONS
            if ball_idx < draw_limit - 1:
                time.sleep(4.5)

        st.success("SIMULAÇÃO ELITE CONCLUÍDA! COMPLETE A ÚLTIMA DEZENA COM SUA INTUIÇÃO.")

    # FOOTER & LEGAL
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style="border-top: 1px solid #222; padding: 20px; text-align: center; color: #444; font-size: 12px;">
            <p>TOTOLOTO ALGORITMIA - SISTEMA DE ANÁLISE ESTATÍSTICA E FÍSICA</p>
            <p>FERRAMENTA EDUCACIONAL PARA MAIORES DE 21 ANOS NO BRASIL</p>
            <p>O SUCESSO EM SIMULAÇÕES NÃO GARANTE RESULTADOS EM SORTEIOS REAIS.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
