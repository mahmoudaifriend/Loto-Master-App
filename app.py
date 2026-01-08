import streamlit as st
import time
import random
import base64
import os
import plotly.graph_objects as go
from datetime import datetime

# --- 1. CONFIGURAÇÃO DO SISTEMA ---
st.set_page_config(
    page_title="Totoloto Algoritmia",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TRATAMENTO DA IMAGEM CENTRAL (GLOBO) ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_b64 = get_image_base64("globo.png")
globo_src = f"data:image/png;base64,{img_b64}" if img_b64 else ""

# --- 3. DATABASE DE JOGOS E CORES ---
GAMES = {
    "Lotofácil": {"id": "lotofacil", "color": "#930089", "draw": 15, "total": 25, "bg": "linear-gradient(180deg, #30002d 0%, #000 100%)"},
    "Mega-Sena": {"id": "mega-sena", "color": "#209869", "draw": 6, "total": 60, "bg": "linear-gradient(180deg, #0a2b1e 0%, #000 100%)"},
    "Quina": {"id": "quina", "color": "#260085", "draw": 5, "total": 80, "bg": "linear-gradient(180deg, #0d003d 0%, #000 100%)"},
    "Lotomania": {"id": "lotomania", "color": "#f78100", "draw": 20, "total": 100, "bg": "linear-gradient(180deg, #3d2100 0%, #000 100%)"}
}

# --- 4. DESIGN PREMIUM E RESPONSIVIDADE (CSS) ---
def inject_premium_ui(game_name):
    conf = GAMES[game_name]
    primary = conf["color"]
    
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@600&display=swap');
        
        .stApp {{
            background: {conf['bg']};
            font-family: 'Rajdhani', sans-serif;
            color: white;
        }}

        .main-header {{
            font-family: 'Orbitron', sans-serif;
            color: #ff4b00;
            text-align: center;
            font-size: 2.8rem;
            text-shadow: 0 0 25px #ff4b00;
            margin-top: 15px;
        }}

        /* GLOBO CENTRAL - O CORAÇÃO DO APP */
        .globo-container {{
            display: flex; justify-content: center; align-items: center;
            position: relative; width: 320px; height: 320px; margin: 0 auto;
        }}
        .globo-img {{
            width: 100%; z-index: 10;
            filter: drop-shadow(0 0 20px {primary});
        }}
        .ring-animation {{
            position: absolute; width: 240px; height: 240px;
            border: 4px dashed {primary}; border-radius: 50%;
            animation: spin 1s linear infinite; z-index: 5;
        }}
        @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

        /* FIX PARA CELULAR: WRAP DE BOLAS */
        .bet-card {{
            background: rgba(255, 255, 255, 0.04);
            border-left: 6px solid {primary};
            padding: 15px; border-radius: 15px; margin-bottom: 12px;
            display: flex; flex-wrap: wrap; align-items: center; gap: 10px;
        }}
        
        .ball-3d {{
            width: 50px; height: 50px; border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #ffffff 0%, {primary} 55%, #000000 100%);
            display: inline-flex; align-items: center; justify-content: center;
            color: white; font-family: 'Orbitron'; font-size: 1.2rem; font-weight: bold;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.8);
        }}

        .ball-x {{
            width: 50px; height: 50px; border-radius: 50%;
            background: #111; border: 2px dashed #ff4b00;
            display: inline-flex; align-items: center; justify-content: center;
            color: #ff4b00; font-size: 1.6rem; font-weight: bold;
            text-shadow: 0 0 10px #ff4b00;
        }}

        /* BOTÃO PREMIUM LARANJA */
        div.stButton > button {{
            background: linear-gradient(90deg, #ff4b00, #ff8700) !important;
            border: none; color: white; border-radius: 50px; padding: 20px;
            font-family: 'Orbitron'; font-size: 1.4rem; width: 100%;
            box-shadow: 0 0 20px rgba(255,75,0,0.5); transition: 0.3s;
        }}
        div.stButton > button:hover {{ transform: scale(1.02); }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- 5. MOTOR DE LÓGICA ---
class Engine:
    @staticmethod
    def generate_smart_bet(draw_count, total_balls, prev_list, lucky_factor):
        pool = list(range(1, total_balls + 1))
        # Peso baseado no histórico
        weights = [1.6 if i in prev_list else 0.7 for i in pool]
        # Peso baseado na sorte lógica
        if lucky_factor > 0:
            for i in range(len(weights)):
                weights[i] += random.uniform(0, lucky_factor/10)

        for _ in range(500):
            res = random.choices(pool, weights=weights, k=draw_count)
            res = sorted(list(set(res)))
            if len(res) == draw_count:
                return res
        return sorted(random.sample(pool, draw_count))

# --- 6. INTERFACE PRINCIPAL ---
def main():
    # Relógio Superior
    st.markdown(f"<p style='text-align:right; font-family:Orbitron; color:#444;'>{datetime.now().strftime('%H:%M:%S')} | BRAZIL</p>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-header'>TOTOLOTO ALGORITMIA</h1>", unsafe_allow_html=True)

    game_key = st.selectbox("QUAL É O DESAFIO DE HOJE?", list(GAMES.keys()))
    inject_premium_ui(game_key)
    conf = GAMES[game_key]

    # ESPAÇO DO GLOBO
    if globo_src:
        st.markdown(f"""
            <div class='globo-container'>
                <div class='ring-animation'></div>
                <img src='{globo_src}' class='globo-img'>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Aguardando o arquivo 'globo.png' para iniciar o motor...")

    # AS DUAS COLUNAS DE ENTRADA
    col_hist, col_luck = st.columns(2)
    with col_hist:
        st.markdown("### 📊 SINCRONIZAÇÃO HISTÓRICA")
        prev_input = st.text_input("ÚLTIMO RESULTADO (Obrigatório):", placeholder="Ex: 01,05,12,20...")
    
    with col_luck:
        st.markdown("### 🍀 SORTE LÓGICA")
        luck_val = st.slider("INTUIÇÃO DO ALGORITMO:", 0, 100, 50)
    
    n_jogos = st.slider("QNT. DE JOGOS:", 1, 50, 5)

    # VALIDAÇÃO DO BOTÃO
    ready = False
    try:
        p_list = [int(x.strip()) for x in prev_input.split(',') if x.strip()]
        if len(p_list) >= 5: ready = True
    except: pass

    if st.button("🚀 INICIAR EXTRAÇÃO", disabled=not ready):
        # Efeito Sonoro
        st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/misc/sounds/bingo-ball-machine-1.mp3"></audio>', unsafe_allow_html=True)
        
        # Geração de Apostas
        bets_data = [Engine.generate_smart_bet(conf["draw"], conf["total"], p_list, luck_val) for _ in range(n_jogos)]
        
        placeholders = [st.empty() for _ in range(n_jogos)]
        visual_memory = [[] for _ in range(n_jogos)]
        
        # Posições do X (Oculto) Aleatórias
        hidden_map = [random.randint(1, conf["draw"]-2) for _ in range(n_jogos)]

        # LOOP SEQUENCIAL (A grande mágica)
        for ball_idx in range(conf["draw"]):
            time.sleep(4.5) # O tempo exato que você pediu
            for bet_idx in range(n_jogos):
                # Lógica do X
                if ball_idx == hidden_map[bet_idx]:
                    ball_html = "<div class='ball-x'>X</div>"
                else:
                    num = bets_data[bet_idx][ball_idx]
                    ball_html = f"<div class='ball-3d'>{str(num).zfill(2)}</div>"
                
                visual_memory[bet_idx].append(ball_html)
                
                # Renderização com Wrap Fix
                placeholders[bet_idx].markdown(f"""
                    <div class='bet-card'>
                        <span style='min-width:80px; font-weight:bold; color:{conf['color']}'>JOGO {bet_idx+1}:</span>
                        {''.join(visual_memory[bet_idx])}
                    </div>
                """, unsafe_allow_html=True)
        
        st.success("SIMULAÇÃO ELITE FINALIZADA!")

    st.markdown("<br><hr><p style='text-align:center; color:#333; font-size:10px;'>TOTOLOTO ALGORITMIA - BRASIL 2026</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
