import streamlit as st
import pandas as pd
import time
import random
import base64
import os
import plotly.graph_objects as go
from datetime import datetime

# --- SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Totoloto Algoritmia Master v8.0",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- FUNCTION TO CONVERT LOCAL IMAGE TO BASE64 ---
def get_image_base64(path):
    """Reads local image and returns base64 string to prevent broken links."""
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

# --- GAME DATA ---
GAMES = {
    "Lotofácil": {"color": "#930089", "draw": 15, "max": 20, "close": True},
    "Mega-Sena": {"color": "#209869", "draw": 6, "max": 20, "close": True},
    "Quina": {"color": "#260085", "draw": 5, "max": 15, "close": False},
    "Lotomania": {"color": "#f78100", "draw": 20, "max": 50, "close": False}
}

# --- PREMIUM CSS (MOBILE FIXES & IMAGE GLOBO) ---
def inject_ui(game_name):
    config = GAMES[game_name]
    primary = config["color"]
    
    # Load the local image 'globo.png'
    img_b64 = get_image_base64("globo.png")
    img_src = f"data:image/png;base64,{img_b64}" if img_b64 else ""

    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@600&display=swap');
        
        .stApp {{ background: #000; font-family: 'Rajdhani', sans-serif; color: white; }}
        .main-title {{ font-family: 'Orbitron'; color: #ff4b00; text-align: center; font-size: 2.2rem; text-shadow: 0 0 15px #ff4b00; }}

        /* CENTRAL GLOBO ENGINE (IMAGE) */
        .globo-box {{
            display: flex; justify-content: center; align-items: center;
            margin: 20px auto; width: 320px; height: 320px; position: relative;
        }}
        .globo-img {{
            width: 90%; z-index: 5; filter: drop-shadow(0 0 20px {primary});
        }}
        .globo-spin {{
            position: absolute; width: 220px; height: 220px;
            border: 4px dotted rgba(255,255,255,0.2); border-radius: 50%;
            animation: rotate 0.7s linear infinite; z-index: 1;
        }}
        @keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

        /* BALLS WRAPPING FOR MOBILE */
        .bet-row {{
            background: rgba(255, 255, 255, 0.05); border-left: 5px solid {primary};
            padding: 15px; border-radius: 12px; margin-bottom: 12px;
            display: flex; flex-wrap: wrap; align-items: center; gap: 10px;
        }}
        .ball-3d {{
            width: 52px; height: 52px; border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #fff, {primary}, #000);
            display: inline-flex; align-items: center; justify-content: center;
            color: white; font-family: 'Orbitron'; font-size: 1.2rem; font-weight: bold;
            box-shadow: 4px 4px 10px rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.1);
        }}
        .ball-x {{
            width: 52px; height: 52px; border-radius: 50%; background: #111;
            border: 2px dashed #ff4b00; display: inline-flex; align-items: center;
            justify-content: center; color: #ff4b00; font-size: 1.5rem; font-weight: bold;
        }}

        /* BUTTON STYLE */
        div.stButton > button {{
            background: linear-gradient(90deg, #ff4b00, #ff8700) !important;
            border: none; color: white; border-radius: 50px; padding: 18px;
            font-family: 'Orbitron'; width: 100%; box-shadow: 0 0 20px rgba(255,75,0,0.4);
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    return img_src

# --- MAIN APP ---
def main():
    # Top Clock
    st.markdown(f"<p style='text-align:right; color:#666;'>{datetime.now().strftime('%H:%M:%S')} | 2026</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='main-title'>TOTOLOTO ALGORITMIA MASTER</h1>", unsafe_allow_html=True)

    game = st.selectbox("SELECIONE A MODALIDADE:", list(GAMES.keys()))
    img_data = inject_ui(game)
    conf = GAMES[game]

    # GLOBO VISUAL
    st.markdown(f"""<div class='globo-box'>
                <div class='globo-spin'></div>
                <img src='{img_data}' class='globo-img'>
                </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        prev = st.text_input("ÚLTIMO RESULTADO (Obrigatório):", placeholder="Ex: 01,05,12...")
        n_bets = st.slider("QNT. DE JOGOS:", 1, 50, 5)
    with col2:
        use_f = st.checkbox("ATIVAR FECHAMENTO") if conf["close"] else False
        f_val = st.number_input("NÚMEROS NA MATRIZ:", conf["draw"]+1, conf["max"]) if use_f else conf["draw"]

    # VALIDATION
    ready = False
    try:
        p_list = [int(x.strip()) for x in prev.split(',') if x.strip()]
        if len(p_list) > 0: ready = True
    except: st.error("Insira os números corretamente.")

    if st.button("🚀 INICIAR EXTRAÇÃO", disabled=not ready):
        # Sound
        st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/misc/sounds/bingo-ball-machine-1.mp3"></audio>', unsafe_allow_html=True)
        
        # Generation Logic
        all_final_bets = []
        for _ in range(n_bets):
            pool = list(range(1, 26 if game == "Lotofácil" else 61)) # Simple pool for logic
            if use_f:
                base = sorted(random.sample(pool, f_val))
                all_final_bets.append(sorted(random.sample(base, conf["draw"])))
            else:
                all_final_bets.append(sorted(random.sample(pool, conf["draw"])))

        placeholders = [st.empty() for _ in range(n_bets)]
        visual_data = [[] for _ in range(n_bets)]
        x_pos = [random.randint(1, conf["draw"]-2) for _ in range(n_bets)]

        # Sequential Draw (4.5s delay)
        for b_idx in range(conf["draw"]):
            time.sleep(4.5)
            for j_idx in range(n_bets):
                if b_idx == x_pos[j_idx]:
                    ball = "<div class='ball-x'>X</div>"
                else:
                    num = all_final_bets[j_idx][b_idx]
                    ball = f"<div class='ball-3d'>{str(num).zfill(2)}</div>"
                
                visual_data[j_idx].append(ball)
                placeholders[j_idx].markdown(f"""<div class='bet-row'>
                    <span style='min-width:70px; font-weight:bold; color:{conf['color']}'>JOGO {j_idx+1}</span>
                    {''.join(visual_data[j_idx])}</div>""", unsafe_allow_html=True)
        
        st.success("SIMULAÇÃO ELITE CONCLUÍDA!")

if __name__ == "__main__":
    main()
