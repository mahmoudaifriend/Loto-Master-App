import streamlit as st
import random
import time
import pandas as pd
import numpy as np

# --- 1. CONFIGURAÇÃO (V12: SAFETY VALVE) ---
st.set_page_config(
    page_title="LotoMaster | Physics V12 (Safe-Guard)",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Purge is now "Warning List", not "Delete List"
GAMES_CONFIG = {
    "Lotofácil": {"color": "#930089", "range": 25, "pick": 15, "purge_count": 3}, 
    "Mega-Sena": {"color": "#209869", "range": 60, "pick": 6, "purge_count": 6},
    "Quina": {"color": "#260085", "range": 80, "pick": 5, "purge_count": 10},
    "Lotomania": {"color": "#f78100", "range": 100, "pick": 50, "purge_count": 5},
    "Timemania": {"color": "#00ff00", "range": 80, "pick": 10, "purge_count": 5},
    "Dia de Sorte": {"color": "#cb8305", "range": 31, "pick": 7, "purge_count": 3},
    "Super Sete": {"color": "#a9cf46", "range": 10, "pick": 7, "purge_count": 0},
    "+Milionária": {"color": "#1f2b44", "range": 50, "pick": 6, "purge_count": 6}
}

# --- 2. CSS ---
st.markdown("""
<style>
    .stApp {background-color: #050505; color: #00ff00;}
    
    /* V12 Header */
    .v12-header {
        border: 2px solid #00ff00;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        background: #001100;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.2);
        margin-bottom: 20px;
    }
    
    /* Ball Styles */
    .ball {
        display: inline-flex; align-items: center; justify-content: center;
        width: 40px; height: 40px; border-radius: 50%;
        font-weight: bold; margin: 3px;
        box-shadow: inset -2px -2px 5px rgba(0,0,0,0.8);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* The Safety Valve Ball (Was Purged, Now Rescued) */
    .rescued-ball {
        border: 2px solid #ff4444; /* Red Border indicating Risk */
        color: #ff4444;
        background: #220000;
        box-shadow: 0 0 5px #ff0000;
    }
    
    .stButton>button {
        background-color: #003300; color: #00ff00; border: 1px solid #00ff00;
        height: 50px; font-weight: bold; text-transform: uppercase;
    }
    .stTextInput>div>div>input { background-color: #111; color: #00ff00; border: 1px solid #333; }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. PHYSICS ENGINE V12 (WITH SAFETY VALVE) ---
class PhysicsEngineV12:
    
    @staticmethod
    def identify_weak_numbers(game_name, last_draw_input):
        config = GAMES_CONFIG[game_name]
        total_balls = config['range']
        
        # 1. Physics Simulation (Same as V11 but specifically to flag, NOT delete)
        balls_score = {}
        
        last_nums = []
        if last_draw_input:
            try:
                last_nums = [int(n) for n in last_draw_input.replace('-', ' ').split() if n.strip().isdigit()]
            except: pass

        for num in range(1, total_balls + 1):
            mass = 1.0
            # Heavier ink logic
            s_num = str(num)
            if '8' in s_num or '0' in s_num: mass += 0.05 
            
            # Position logic
            energy = 1.0
            if num <= 5: energy = 0.90 # Bottom friction
            
            # Cycle logic
            thermal = 1.0
            if num in last_nums: thermal = 0.95 # Retained heat
            
            score = (1.0 / mass) * energy * thermal
            balls_score[num] = score
            
        # Sort by weakest
        sorted_balls = sorted(balls_score.items(), key=lambda item: item[1])
        cutoff = config['purge_count']
        
        # RETURN THE WARNING LIST (Don't delete yet)
        weak_list = [item[0] for item in sorted_balls[:cutoff]]
        return weak_list

    @staticmethod
    def generate_safe_games(game_name, weak_numbers, qty):
        config = GAMES_CONFIG[game_name]
        universe = list(range(1, config['range'] + 1))
        if game_name == "Lotomania": universe = list(range(0, 100))
        
        # SEPARATE POOLS
        clean_pool = [n for n in universe if n not in weak_numbers]
        risk_pool = weak_numbers # The "Purged" ones
        
        games = []
        
        for _ in range(qty):
            # LOGIC: 85% Clean Numbers, 15% Risk Numbers (Safety Valve)
            # This ensures if 04 or 21 are in 'risk_pool', they can still be picked!
            
            current_game = []
            
            # How many risky numbers to inject? (0, 1, or 2 max)
            # We use chaos to decide.
            risk_injection = 0
            chaos_roll = random.random()
            if chaos_roll < 0.30: risk_injection = 1 # 30% chance to save 1 number
            if chaos_roll < 0.05: risk_injection = 2 # 5% chance to save 2 numbers
            
            # Pick from Risk Pool
            if risk_injection > 0 and len(risk_pool) > 0:
                rescued = random.sample(risk_pool, min(risk_injection, len(risk_pool)))
                current_game.extend(rescued)
            
            # Fill rest from Clean Pool
            needed = config['pick'] - len(current_game)
            core = random.sample(clean_pool, needed)
            current_game.extend(core)
            
            games.append(sorted(current_game))
            
        return games

# --- 4. UI ---

st.markdown("<div class='v12-header'><h1>🛡️ LotoMaster V12</h1><h3>PHYSICS + SAFETY VALVE (NO DELETE)</h3></div>", unsafe_allow_html=True)

c1, c2 = st.columns([2,1])
game_sel = c1.selectbox("MÓDULO:", list(GAMES_CONFIG.keys()))
qty_sel = c2.number_input("JOGOS:", 1, 50, 5)

with st.expander("🧬 CALIBRAGEM (Último Resultado)"):
    last_input = st.text_input("Cole o último sorteio:")

if st.button("GERAR COM PROTEÇÃO DE ERRO 🚀"):
    
    # 1. Identify Weak Numbers
    weak = PhysicsEngineV12.identify_weak_numbers(game_sel, last_input)
    
    # SHOW WARNING (Not Purge)
    weak_html = " - ".join([f"{n:02d}" for n in weak])
    st.error(f"⚠️ ZONA DE RISCO (PESO ALTO): {weak_html}")
    st.caption("O sistema identificou estes números como fracos, mas irá INJETÁ-LOS em alguns jogos para garantir 15 pontos caso a física falhe.")
    
    # 2. Generate
    games = PhysicsEngineV12.generate_safe_games(game_sel, weak, qty_sel)
    
    # 3. Display
    txt_out = "LotoMaster V12 - SafeGuard\n\n"
    theme = GAMES_CONFIG[game_sel]['color']
    
    for i, g in enumerate(games):
        txt_out += f"Jogo {i+1}: {g}\n"
        
        # Visual Logic to highlight Rescued numbers
        balls_html = ""
        for n in g:
            style_class = "ball"
            style_col = f"background:{theme}"
            
            if n in weak: # Highlight the saved number!
                style_class = "ball rescued-ball"
                style_col = "" # Red is in CSS
            
            balls_html += f"<div class='{style_class}' style='{style_col}'>{n:02d}</div>"
            
        st.markdown(f"""
        <div style="background:#111; padding:10px; border-radius:10px; margin-bottom:10px; border-left:4px solid {theme}">
            <div style="color:#888; font-size:12px;">JOGO #{i+1}</div>
            <div>{balls_html}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.download_button("💾 BAIXAR JOGOS SEGUROS", txt_out, file_name="V12_Safe.txt")
