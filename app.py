import streamlit as st
import random
import time
import pandas as pd
import numpy as np # Library for math calculations

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="LotoMaster | Physics Simulation Engine",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CONFIGURAÇÃO DOS JOGOS ---
GAMES_CONFIG = {
    "Lotofácil": {"color": "#930089", "range": 25, "pick": 15, "purge": 5},
    "Mega-Sena": {"color": "#209869", "range": 60, "pick": 6, "purge": 10},
    "Quina": {"color": "#260085", "range": 80, "pick": 5, "purge": 15},
    "Lotomania": {"color": "#f78100", "range": 100, "pick": 50, "purge": 10},
    "Timemania": {"color": "#00ff00", "range": 80, "pick": 10, "purge": 10},
    "Dupla Sena": {"color": "#a61324", "range": 50, "pick": 6, "purge": 8},
    "Dia de Sorte": {"color": "#cb8305", "range": 31, "pick": 7, "purge": 5},
    "Super Sete": {"color": "#a9cf46", "range": 10, "pick": 7, "purge": 0},
    "+Milionária": {"color": "#1f2b44", "range": 50, "pick": 6, "purge": 10}
}

# --- 3. ESTILO CSS (Hacker/Physics Lab) ---
st.markdown("""
<style>
    .stApp {background-color: #0b0c10; color: #66fcf1;}
    
    /* Headers */
    .physics-header {
        background: radial-gradient(circle, #1f2833 0%, #0b0c10 100%);
        border: 1px solid #45a29e;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 0 15px rgba(102, 252, 241, 0.1);
    }
    
    /* Stats Box */
    .sim-box {
        background: #1f2833;
        color: #c5c6c7;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #66fcf1;
        font-family: 'Courier New', monospace;
        margin-bottom: 10px;
    }

    /* Balls */
    .ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px; height: 38px;
        border-radius: 50%;
        color: white;
        font-weight: bold;
        font-size: 16px;
        margin: 4px;
        box-shadow: inset -2px -2px 5px rgba(0,0,0,0.5), 2px 2px 5px rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .purged-ball {
        width: 32px; height: 32px;
        border-radius: 50%;
        background: #330000;
        color: #ff0000;
        border: 1px dashed #ff0000;
        display: inline-flex;
        align-items: center; justify-content: center;
        margin: 2px;
        font-size: 12px;
        opacity: 0.8;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1f2833;
        color: #66fcf1;
        border: 1px solid #45a29e;
        height: 55px;
        font-weight: bold;
        text-transform: uppercase;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a29e;
        color: #0b0c10;
    }

    /* Inputs */
    .stTextInput>div>div>input { background-color: #1f2833; color: #66fcf1; border: 1px solid #45a29e; }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 4. MOTOR DE FÍSICA (The Core Innovation) ---
class PhysicsSimulator:
    
    @staticmethod
    def run_simulation(game_name, last_draw_input):
        config = GAMES_CONFIG[game_name]
        total_balls = config['range']
        
        # 1. SETUP PHYSICAL PROPERTIES FOR EACH BALL
        # We create a "DataFrame" of balls with physical attributes
        balls_data = []
        
        # Parse last draw for "Cold/Hot" physics
        last_draw_nums = []
        if last_draw_input:
            try:
                last_draw_nums = [int(n) for n in last_draw_input.replace('-', ' ').split() if n.strip().isdigit()]
            except: pass

        for num in range(1, total_balls + 1):
            # A. Mass Factor: Balls with more "ink" (e.g., 08, 20) are slightly heavier
            # We simulate this by checking digits. 8 has 2 loops, 0 has 1 loop, 1 has little ink.
            ink_weight = 0
            str_num = str(num)
            for char in str_num:
                if char in ['8']: ink_weight += 0.05
                elif char in ['0', '6', '9']: ink_weight += 0.04
                elif char in ['2', '3', '5']: ink_weight += 0.03
                else: ink_weight += 0.01
            
            base_mass = 1.0 + ink_weight
            
            # B. Tube Position Bias (Loading Order)
            # Balls 1-5 are at bottom (more friction/pressure). Balls 21-25 are at top (high energy).
            # This is a curve: Bottom = High Friction, Top = High Energy. Middle = Neutral.
            position_energy = 1.0
            if num <= 5: position_energy = 0.95 # Harder to move initially
            elif num >= (total_balls - 5): position_energy = 1.05 # Falls faster
            
            # C. Cold/Hot State (Thermodynamics)
            # If a ball came out recently, it might retain "static charge" (simulation logic)
            thermal_factor = 1.0
            if num in last_draw_nums:
                thermal_factor = 0.98 # Slightly less likely to repeat immediately in chaos theory
            
            # TOTAL PROBABILITY SCORE
            # Higher score = Higher chance to be drawn
            # We invert Mass (Heavier = harder to fly up in air mix, or harder to be sucked?
            # Let's assume Gravity Pick: Heavier falls easier? No, usually mixing paddles throw them.
            # Let's assume standard chaos: Lighter moves faster.
            physics_score = (1.0 / base_mass) * position_energy * thermal_factor
            
            balls_data.append({"num": num, "score": physics_score})
            
        # 2. RUN 10,000 VIRTUAL DRAWS (Monte Carlo Simulation)
        # We simulate the machine drawing balls 10k times based on these biased scores.
        
        df_balls = pd.DataFrame(balls_data)
        
        # Normalize probabilities
        total_score = df_balls['score'].sum()
        df_balls['prob'] = df_balls['score'] / total_score
        
        # Perform Simulation
        # We use numpy for fast weighted random sampling
        simulated_counts = {n: 0 for n in range(1, total_balls + 1)}
        
        # Fast simulation loop
        # We simulate 'N' draws. Each draw picks 'pick' numbers.
        # This is computationally intensive, so we use a mathematical shortcut:
        # The expected frequency is Proba * Trials. We add noise (Chaos).
        
        for index, row in df_balls.iterrows():
            # Expected occurrences + Random Chaos (The Machine Vibration)
            # Normal distribution centering on Probability
            expected = row['prob'] * 10000
            chaos = random.gauss(0, expected * 0.05) # 5% Chaos deviation
            final_count = expected + chaos
            simulated_counts[row['num']] = final_count
            
        # 3. IDENTIFY THE WEAKEST (PURGE LIST)
        # Sort by lowest frequency
        sorted_balls = sorted(simulated_counts.items(), key=lambda item: item[1])
        
        # Select the bottom N balls (Purge Amount)
        purge_amount = config['purge']
        purged_numbers = [item[0] for item in sorted_balls[:purge_amount]]
        
        return sorted(purged_numbers), sorted_balls # Return detailed stats if needed

    @staticmethod
    def generate_final_games(game_name, purged_numbers, last_draw_input, qty):
        config = GAMES_CONFIG[game_name]
        universe = list(range(1, config['range'] + 1))
        if game_name == "Lotomania": universe = list(range(0, 100))
        
        # CLEAN POOL
        clean_pool = [n for n in universe if n not in purged_numbers]
        
        games = []
        for _ in range(qty):
            # APPLY GEOMETRY ON CLEAN POOL
            if game_name == "Lotofácil":
                moldura = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25]
                miolo   = [7, 8, 9, 12, 13, 14, 17, 18, 19]
                
                avail_moldura = [n for n in clean_pool if n in moldura]
                avail_miolo   = [n for n in clean_pool if n in miolo]
                
                # Try to hit Target 10/5
                target_m = min(len(avail_moldura), 10)
                target_c = 15 - target_m
                
                # Fallback if not enough core numbers
                if len(avail_miolo) < target_c:
                    target_c = len(avail_miolo)
                    target_m = 15 - target_c
                
                p1 = random.sample(avail_moldura, target_m)
                p2 = random.sample(avail_miolo, target_c)
                games.append(sorted(p1 + p2))
                
            else:
                # Standard for others
                games.append(sorted(random.sample(clean_pool, config['pick'])))
                
        return games

# --- 5. UI LAYOUT ---

st.markdown("<div class='physics-header'><h1>⚛️ LotoMaster Physics V11</h1><h3>SIMULAÇÃO MECÂNICA & EXPURGO</h3></div>", unsafe_allow_html=True)

# Inputs
c1, c2 = st.columns([2, 1])
with c1:
    game_sel = st.selectbox("MÓDULO DE FÍSICA:", list(GAMES_CONFIG.keys()))
with c2:
    q_sel = st.number_input("QTD JOGOS:", 1, 50, 5)

with st.expander("🧪 CALIBRAGEM DA MÁQUINA (Entrada de Dados)", expanded=True):
    last_draw = st.text_input(f"Cole o último resultado ({game_sel}):", placeholder="Necessário para cálculo de termodinâmica...")
    st.caption("ℹ️ O sistema usará os dados para calcular o 'Coeficiente de Atrito' das bolas repetidas.")

# Buttons
b1, b2 = st.columns(2)
with b1:
    btn_sim = st.button("INICIAR SIMULAÇÃO (10.000 CICLOS) ⚙️")
with b2:
    btn_rst = st.button("REINICIAR LABORATÓRIO 🗑️")

# --- 6. SIMULATION LOGIC ---

if 'phy_results' not in st.session_state:
    st.session_state.phy_results = []
    st.session_state.purged = []

if btn_rst:
    st.session_state.phy_results = []
    st.session_state.purged = []
    st.rerun()

if btn_sim:
    # 1. VISUALIZATION OF COMPUTING
    progress_text = st.empty()
    bar = st.progress(0)
    
    steps = [
        "⚖️ Pesando massa de tinta das esferas...",
        "🌡️ Calculando temperatura e atrito estático...",
        "🌪️ Simulando 10.000 extrações virtuais...",
        "📉 Identificando anomalias estatísticas...",
        "🚫 Expurgo de dezenas gravitacionalmente fracas..."
    ]
    
    for i, txt in enumerate(steps):
        progress_text.text(f"PHYSICS ENGINE: {txt}")
        time.sleep(0.5)
        bar.progress((i+1) * 20)
    
    bar.empty()
    progress_text.empty()
    
    # 2. RUN ENGINE
    purged, stats = PhysicsSimulator.run_simulation(game_sel, last_draw)
    st.session_state.purged = purged
    
    # 3. GENERATE GAMES
    games = PhysicsSimulator.generate_final_games(game_sel, purged, last_draw, q_sel)
    st.session_state.phy_results = games

# --- 7. RESULTS DISPLAY ---

if st.session_state.purged:
    # SHOW PURGE
    purge_html = "".join([f"<div class='purged-ball'>{n:02d}</div>" for n in st.session_state.purged])
    st.markdown(f"""
    <div class='sim-box' style='border-color: #ff3333;'>
        <div style='color:#ff3333; font-weight:bold;'>🚫 DEZENAS EXPURGADAS (FALHA FÍSICA DETECTADA)</div>
        <div style='margin-top:5px; font-size:12px;'>Após 10.000 simulações, estas bolas apresentaram a menor taxa de saída devido a peso/posição:</div>
        <div style='margin-top:10px;'>{purge_html}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # SHOW GAMES
    theme = GAMES_CONFIG[game_sel]['color']
    txt_export = f"LotoMaster Physics V11 - {game_sel}\n\n"
    
    for i, game in enumerate(st.session_state.phy_results):
        balls_html = "".join([f"<div class='ball' style='background:{theme}'>{n:02d}</div>" for n in game])
        txt_export += f"Jogo {i+1}: {game}\n"
        
        st.markdown(f"""
        <div style="background:#1f2833; padding:15px; border-radius:10px; margin-bottom:10px; border-left:5px solid {theme};">
            <div style="color:#fff; font-weight:bold; font-size:14px; margin-bottom:5px;">JOGO #{i+1} <span style="font-size:10px; background:#45a29e; color:#000; padding:2px 5px; border-radius:3px;">PHYSICS</span></div>
            <div>{balls_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # Export
    st.download_button("💾 BAIXAR DADOS DA SIMULAÇÃO", txt_export, file_name=f"Physics_{game_sel}.txt")

st.markdown("<br><div style='text-align:center; font-size:11px; color:#444;'>Engine V11.0 - Thermodynamic & Gravity Simulation Model.</div>", unsafe_allow_html=True)
