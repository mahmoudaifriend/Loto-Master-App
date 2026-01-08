import streamlit as st
import time
import random
import base64
import os
import plotly.graph_objects as go
from datetime import datetime

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="Totoloto Algoritmia",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. IMAGE HANDLING (GLOBO) ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Convert local 'globo.png' to base64 for embedding
img_base64 = get_base64_image("globo.png")
globo_src = f"data:image/png;base64,{img_base64}" if img_base64 else ""

# --- 3. GAME DATABASE ---
GAMES = {
    "Lotofácil": {"color": "#930089", "draw": 15, "total": 25, "bg": "linear-gradient(180deg, #4b0046 0%, #000000 100%)"},
    "Mega-Sena": {"color": "#209869", "draw": 6, "total": 60, "bg": "linear-gradient(180deg, #0d3d2a 0%, #000000 100%)"},
    "Quina": {"color": "#260085", "draw": 5, "total": 80, "bg": "linear-gradient(180deg, #11003d 0%, #000000 100%)"},
    "Lotomania": {"color": "#f78100", "draw": 20, "total": 100, "bg": "linear-gradient(180deg, #5e3100 0%, #000000 100%)"}
}

# --- 4. PREMIUM UI/UX DESIGN (CSS) ---
def inject_ui(game_name):
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
            font-size: 2.5rem;
            text-shadow: 0 0 20px #ff4b00;
            margin-top: 10px;
        }}

        /* CENTRAL ENGINE (GLOBO) */
        .globo-area {{
            display: flex; justify-content: center; align-items: center;
            position: relative; width: 300px; height: 300px; margin: 0 auto;
        }}
        .globo-image {{
            width: 100%; z-index: 10;
            filter: drop-shadow(0 0 20px {primary});
        }}
        .spinning-ring {{
            position: absolute; width: 220px; height: 220px;
            border: 4px dotted {primary}; border-radius: 50%;
            animation: rotate 0.8s linear infinite; z-index: 5;
        }}
        @keyframes rotate {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

        /* MOBILE OPTIMIZED RESULTS */
        .result-box {{
            background: rgba(255, 255, 255, 0.05);
            border-left: 6px solid {primary};
            padding: 15px; border-radius: 15px; margin-bottom: 12,px;
            display: flex; flex-wrap: wrap; align-items: center; gap: 8px;
        }}
        
        .ball-3d {{
            width: 50px; height: 50px; border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #ffffff 0%, {primary} 55%, #000000 100%);
            display: inline-flex; align-items: center; justify-content: center;
            color: white; font-family: 'Orbitron'; font-size: 1.2rem; font-weight: bold;
            box-shadow: 4px 4px 12px rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.1);
        }}

        .ball-hidden {{
            width: 50px; height: 50px; border-radius: 50%;
            background: #111; border: 2px dashed #ff4b00;
            display: inline-flex; align-items: center; justify-content: center;
            color: #ff4b00; font-size: 1.6rem; font-weight: bold;
        }}

        /* BUTTON STYLE */
        div.stButton > button {{
            background: linear-gradient(90deg, #ff4b00, #ff8700) !important;
            border: none; color: white; border-radius: 50px; padding: 18px;
            font-family: 'Orbitron'; font-size: 1.2rem; width: 100%;
            box-shadow: 0 0 20px rgba(255,75,0,0.5);
        }}
        
        /* INPUT FIELDS CUSTOMIZATION */
        .stTextInput input {{
            background-color: #111 !important;
            color: {primary} !important;
            border: 1px solid {primary} !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- 5. LOGIC ENGINE ---
class Logic:
    @staticmethod
    def generate_balanced_bet(draw_count, total_balls, prev_list, luck_factor):
        pool = list(range(1, total_balls + 1))
        # Logic 1: Historical weight
        weights = [1.5 if i in prev_list else 0.8 for i in pool]
        
        # Logic 2: Lucky Logic (Random fluctuation based on luck_factor)
        if luck_factor > 0:
            for i in range(len(weights)):
                weights[i] += random.uniform(0, luck_factor/10)

        for _ in range(1000):
            selection = random.choices(pool, weights=weights, k=draw_count)
            selection = sorted(list(set(selection)))
            if len(selection) == draw_count:
                return selection
        return sorted(random.sample(pool, draw_count))

# --- 6. MAIN APP ---
def main():
    # Real-time Clock at the Top
    st.markdown(f"<p style='text-align:right; font-family:Orbitron; color:#666;'>{datetime.now().strftime('%H:%M:%S')} | BRAZIL</p>", unsafe_allow_html=True)
    
    # Static App Name
    st.markdown("<h1 class='main-header'>TOTOLOTO ALGORITMIA</h1>", unsafe_allow_html=True)

    game_choice = st.selectbox("SELECIONE A MODALIDADE:", list(GAMES.keys()))
    inject_ui(game_choice)
    conf = GAMES[game_choice]

    # GLOBO VISUAL
    if globo_src:
        st.markdown(f"""
            <div class='globo-area'>
                <div class='spinning-ring'></div>
                <img src='{globo_src}' class='globo-image'>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Aguardando arquivo 'globo.png' para carregar o motor...")

    # TWO MAIN INPUT CHANNELS
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 SINCRONIZAÇÃO HISTÓRICA")
        prev_input = st.text_input("RESULTADO ANTERIOR (OBRIGATÓRIO):", placeholder="Ex: 01,05,12,15...")
    
    with col2:
        st.markdown("### 🍀 SORTE LÓGICA")
        luck_level = st.slider("NÍVEL DE INTUIÇÃO DO SISTEMA:", 0, 100, 50)
    
    n_bets = st.slider("QUANTIDADE DE JOGOS:", 1, 50, 5)

    # ACTION VALIDATION
    ready = False
    try:
        p_list = [int(x.strip()) for x in prev_input.split(',') if x.strip()]
        if len(p_list) >= 5: # Minimum valid input check
            ready = True
    except: pass

    if st.button("🚀 INICIAR EXTRAÇÃO", disabled=not ready):
        # Sound Effect (External link)
        st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/misc/sounds/bingo-ball-machine-1.mp3"></audio>', unsafe_allow_html=True)
        
        # Generation
        final_bets = [Logic.generate_balanced_bet(conf["draw"], conf["total"], p_list, luck_level) for _ in range(n_bets)]
        
        placeholders = [st.empty() for _ in range(n_bets)]
        visual_data = [[] for _ in range(n_bets)]
        
        # Random position for the hidden 'X'
        x_indices = [random.randint(1, conf["draw"]-2) for _ in range(n_bets)]

        # SEQUENTIAL DRAW (4.5s Delay)
        for b_idx in range(conf["draw"]):
            time.sleep(4.5) # Physical Pulse
            for j_idx in range(n_bets):
                if b_idx == x_indices[j_idx]:
                    ball = "<div class='ball-hidden'>X</div>"
                else:
                    num = final_bets[j_idx][b_idx]
                    ball = f"<div class='ball-3d'>{str(num).zfill(2)}</div>"
                
                visual_data[j_idx].append(ball)
                placeholders[j_idx].markdown(f"""
                    <div class='result-box'>
                        <span style='min-width:70px; font-weight:bold; color:{conf['color']}'>JOGO {j_idx+1}:</span>
                        {''.join(visual_data[j_idx])}
                    </div>
                """, unsafe_allow_html=True)
        
        st.success("SIMULAÇÃO CONCLUÍDA!")

    # LEGAL
    st.markdown("<br><hr><p style='text-align:center; color:#444; font-size:10px;'>TOTOLOTO ALGORITMIA - MAIORES DE 21 ANOS</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
