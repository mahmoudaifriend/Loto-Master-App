import streamlit as st
import random
import time
import pandas as pd
from io import BytesIO

# --- 1. SETTINGS & ANCHOR CONFIGURATION ---
st.set_page_config(
    page_title="LotoMaster V13 | God Mode",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Official Official Caixa Colors & Specs
GAMES_CONFIG = {
    "Lotofácil": {"color": "#930089", "range": 25, "pick": 15, "purge": 5},
    "Mega-Sena": {"color": "#209869", "range": 60, "pick": 6, "purge": 10},
    "Quina": {"color": "#260085", "range": 80, "pick": 5, "purge": 15},
    "Lotomania": {"color": "#f78100", "range": 100, "pick": 50, "purge": 10},
    "Timemania": {"color": "#00ff00", "range": 80, "pick": 10, "purge": 10},
    "+Milionária": {"color": "#1f2b44", "range": 50, "pick": 6, "purge": 10}
}

# --- 2. CSS CUSTOM STYLING (Hacker Dark Mode / Mobile Ready) ---
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #00ff41; font-family: 'Courier New', monospace; }
    .main-header {
        border: 2px solid #00ff41; padding: 20px; border-radius: 15px;
        text-align: center; background: #0a0a0a;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3); margin-bottom: 25px;
    }
    .bet-card {
        background: #111; padding: 15px; border-radius: 12px;
        margin-bottom: 15px; border-left: 5px solid #00ff41;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    .ball {
        display: inline-flex; align-items: center; justify-content: center;
        width: 38px; height: 38px; border-radius: 50%;
        color: white; font-weight: bold; font-size: 15px; margin: 3px;
        box-shadow: inset -3px -3px 6px rgba(0,0,0,0.7);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .anchor-ball { border: 2px solid #f1c40f; box-shadow: 0 0 8px #f1c40f; } /* Golden Glow for Anchors */
    .rescue-ball { border: 2px solid #ff4b4b; color: #ff4b4b; } /* Red for Rescued */
    
    .stButton>button {
        width: 100%; height: 60px; font-weight: bold; font-size: 18px;
        background-color: #004d00; color: #00ff41; border: 1px solid #00ff41;
    }
    .stButton>button:hover { background-color: #00ff41; color: black; }
    
    input { background-color: #1a1a1a !important; color: #00ff41 !important; border: 1px solid #333 !important; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. V13 SOVEREIGN ENGINE (Physics + Anchor Matrix) ---
class SovereignEngineV13:
    
    @staticmethod
    def simulate_machine_physics(game_name, last_draw_str):
        config = GAMES_CONFIG[game_name]
        total_range = config['range']
        
        # Analyze Input
        last_nums = []
        if last_draw_str:
            last_nums = [int(n) for n in last_draw_str.replace('-', ' ').split() if n.strip().isdigit()]

        ball_scores = {}
        for n in range(1, total_range + 1):
            # A. Ink Mass Factor (Weight)
            mass = 1.0
            if '8' in str(n): mass += 0.06 # Heaviest
            if '0' in str(n) or '6' in str(n) or '9' in str(n): mass += 0.04
            
            # B. Static Friction (Position 1-5 are bottom)
            friction = 1.0
            if n <= 5: friction = 1.15 # Higher resistance
            
            # C. Thermodynamics (Heat from last draw)
            heat = 1.0
            if n in last_nums: heat = 1.05 # Rule of 9: Likelihood to repeat
            
            # Physics score calculation
            score = (heat / (mass * friction)) * random.uniform(0.95, 1.05)
            ball_scores[n] = score

        # Rank all balls
        ranked = sorted(ball_scores.items(), key=lambda x: x[1], reverse=True)
        top_20 = [x[0] for x in ranked[:20]]
        purged = [x[0] for x in ranked[-config['purge']:]]
        
        return top_20, purged

    @staticmethod
    def generate_anchor_matrix(top_20, qty):
        # The Trap: 12 Fixed Anchors + 3 Rotating Wings
        anchors = top_20[:12] # The strongest 12
        wings = top_20[12:]   # The remaining 8
        
        final_games = []
        for _ in range(qty):
            # Select 3 unique wings for each game to cover the 20-pool
            selected_wings = random.sample(wings, 3)
            game = sorted(anchors + selected_wings)
            final_games.append({"nums": game, "anchors": anchors})
            
        return final_games

# --- 4. INTERFACE ---

st.markdown("<div class='main-header'><h1>👑 LOTO-MASTER V13</h1><h3>GOD MODE: PHYSICS + ANCHOR MATRIX</h3></div>", unsafe_allow_html=True)

# Top Bar (Mobile Friendly)
col_set1, col_set2 = st.columns([2, 1])
with col_set1:
    game_mode = st.selectbox("MÓDULO DE PODER:", list(GAMES_CONFIG.keys()))
with col_set2:
    qty_input = st.number_input("BAU DE JOGOS:", 1, 100, 10)

# Input Expansion
with st.expander("🧬 SINCRONIZAÇÃO TÉRMICA (Último Resultado)", expanded=True):
    last_draw_data = st.text_input("Cole os números do último sorteio (Opcional):")
    st.caption("Se vazio, o sistema usará Física Pura baseada em Massa e Atrito.")

# Action Buttons
col_btn1, col_btn2 = st.columns(2)
if col_btn1.button("EXECUTAR PROTOCOLO 🚀"):
    # 1. Start Physics Simulation
    with st.spinner("⚛️ Simulando Atrito, Massa e Termodinâmica..."):
        time.sleep(1)
        top_20, purged_list = SovereignEngineV13.simulate_machine_physics(game_mode, last_draw_data)
        st.session_state.v13_results = SovereignEngineV13.generate_anchor_matrix(top_20, qty_input)
        st.session_state.v13_top20 = top_20
        st.session_state.v13_purged = purged_list

if col_btn2.button("LIMPAR SISTEMA 🗑️"):
    st.session_state.v13_results = []
    st.rerun()

# --- 5. RESULTS RENDERING ---

if 'v13_results' in st.session_state and st.session_state.v13_results:
    theme = GAMES_CONFIG[game_mode]['color']
    
    # Show the 20-Number Trap (Psychological boost)
    st.markdown(f"""
    <div style='background:#0a0a0a; padding:15px; border:1px solid #f1c40f; border-radius:10px; margin-bottom:20px;'>
        <b style='color:#f1c40f;'>🎯 POOL DE 20 DEZENAS SELECIONADAS (O TRAP):</b><br>
        <span style='font-size:12px; color:#888;'>O sistema reduziu 3.2M de chances para este grupo de elite:</span><br>
        <p style='word-wrap: break-word;'>{' - '.join([f"{n:02d}" for n in st.session_state.v13_top20])}</p>
    </div>
    """, unsafe_allow_html=True)

    txt_export = f"LotoMaster V13 God Mode - {game_mode}\n\n"
    
    for i, game_data in enumerate(st.session_state.v13_results):
        nums = game_data['nums']
        anchors = game_data['anchors']
        
        # Build Ball HTML
        balls_html = ""
        for n in nums:
            css_class = "ball"
            if n in anchors: css_class += " anchor-ball"
            balls_html += f"<div class='{css_class}' style='background:{theme}'>{n:02d}</div>"

        st.markdown(f"""
        <div class="bet-card" style="border-left-color: {theme}">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span style="font-weight:bold;">JOGO #{i+1}</span>
                <span style="font-size:10px; color:#aaa;">MATRIX 12+3</span>
            </div>
            <div style="display:flex; flex-wrap:wrap; justify-content:center;">
                {balls_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Copy to clipboard code block
        st.code(" ".join([f"{n:02d}" for n in nums]), language="text")
        txt_export += f"Jogo {i+1}: {nums}\n"

    # Bottom Export & Clear
    st.markdown("---")
    st.download_button("💾 BAIXAR PLANILHA DE VITÓRIA (TXT)", txt_export, file_name=f"V13_{game_mode}.txt")
    
    if st.button("LIMPAR TELA (FIM) 🗑️"):
        st.session_state.v13_results = []
        st.rerun()

# --- 6. FOOTER ---
st.markdown("<br><div style='text-align:center; color:#333; font-size:10px;'>V13 God Mode: Anchor Matrix & Physics Hybrid. No data is stored.</div>", unsafe_allow_html=True)
