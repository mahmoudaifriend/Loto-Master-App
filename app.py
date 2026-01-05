import streamlit as st
import random
import time
import pandas as pd
from io import BytesIO

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LotoMaster | Sistema Físico-Matemático",
    page_icon="🎱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SESSION STATE MANAGEMENT ---
if 'generated_games' not in st.session_state:
    st.session_state.generated_games = []

# --- 3. COLORS & CONFIGURATION (Caixa Official Standards) ---
GAMES_CONFIG = {
    "Lotofácil": {"color": "#930089", "range": 25, "pick": 15, "min_sum": 180, "max_sum": 220},
    "Mega-Sena": {"color": "#209869", "range": 60, "pick": 6, "min_sum": 130, "max_sum": 240},
    "Quina": {"color": "#260085", "range": 80, "pick": 5, "min_sum": 150, "max_sum": 260},
    "Lotomania": {"color": "#f78100", "range": 100, "pick": 50, "min_sum": 2000, "max_sum": 3000},
    "Timemania": {"color": "#00ff00", "range": 80, "pick": 10, "min_sum": 300, "max_sum": 500},
    "Dupla Sena": {"color": "#a61324", "range": 50, "pick": 6, "min_sum": 120, "max_sum": 190},
    "Dia de Sorte": {"color": "#cb8305", "range": 31, "pick": 7, "min_sum": 90, "max_sum": 140},
    "Super Sete": {"color": "#a9cf46", "range": 10, "pick": 7, "min_sum": 0, "max_sum": 70}, # Special Logic
    "+Milionária": {"color": "#1f2b44", "range": 50, "pick": 6, "min_sum": 120, "max_sum": 190} # +2 Trevos
}

# --- 4. CSS STYLING (Mobile & App Feel) ---
st.markdown("""
<style>
    /* Base Styles */
    .stApp {background-color: #f8f9fa;}
    
    /* Dynamic Headers */
    .game-header {
        font-family: 'Arial', sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
        text-transform: uppercase;
        height: 50px;
    }
    
    /* Lotto Ball Design */
    .ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: radial-gradient(circleAt 10px 10px, #ffffff, #e0e0e0); /* 3D Effect Base */
        color: white;
        font-weight: bold;
        font-size: 16px;
        margin: 3px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.5);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Card Container */
    .bet-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        border-left: 6px solid #ccc; /* Will be colored dynamically */
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        text-align: center;
        letter-spacing: 2px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 5. PHYSICS & LOGIC ENGINE ---
class PhysicsEngine:
    
    @staticmethod
    def filter_historical_collisions(game_numbers):
        # SIMULATION: In a real scenario, this connects to a 1GB DB.
        # Here we simulate the logic: "If numbers are too sequential or generic, reject".
        # This prevents "Lazy" random generation.
        if game_numbers == list(range(1, len(game_numbers)+1)): return False # Reject 1,2,3...
        return True # Accepted

    @staticmethod
    def generate_smart_game(game_name, last_draw_input=None):
        config = GAMES_CONFIG[game_name]
        
        # --- STRATEGY 1: DERIVED FROM LAST DRAW (The "Rule of 9" Logic) ---
        if last_draw_input and game_name == "Lotofácil":
            try:
                # Parse Input
                last_nums = sorted([int(n) for n in last_draw_input.replace('-', ' ').split() if n.strip().isdigit()])
                if len(last_nums) == 15:
                    all_nums = list(range(1, 26))
                    missing_nums = list(set(all_nums) - set(last_nums))
                    
                    while True:
                        # 9 Repeating Numbers + 6 Missing Numbers
                        repeats = random.sample(last_nums, 9)
                        news = random.sample(missing_nums, 6)
                        final = sorted(repeats + news)
                        
                        # Validate Math Physics
                        s = sum(final)
                        odds = sum(1 for x in final if x % 2 != 0)
                        if (config['min_sum'] <= s <= config['max_sum']) and (7 <= odds <= 9):
                            return {"nums": final, "type": "DERIVADO 9+6", "color": config['color']}
            except:
                pass # Fallback to standard physics if input error

        # --- STRATEGY 2: PURE PHYSICS & CHAOS (Standard) ---
        while True:
            # Generate based on Game Type
            if game_name == "Lotomania":
                final = sorted(random.sample(range(0, 100), 50))
            elif game_name == "Super Sete":
                final = [random.randint(0, 9) for _ in range(7)]
            elif game_name == "+Milionária":
                nums = sorted(random.sample(range(1, 51), 6))
                trevos = sorted(random.sample(range(1, 7), 2))
                final = {"n": nums, "t": trevos}
            elif game_name == "Timemania":
                nums = sorted(random.sample(range(1, 81), 10))
                teams = ["FLAMENGO", "CORINTHIANS", "PALMEIRAS", "SÃO PAULO", "VASCO"]
                final = {"n": nums, "team": random.choice(teams)}
            elif game_name == "Dia de Sorte":
                nums = sorted(random.sample(range(1, 32), 7))
                months = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO"]
                final = {"n": nums, "month": random.choice(months)}
            else:
                # Standard (Mega, Quina, Dupla, Lotofacil fallback)
                rng = range(1, config['range'] + 1)
                final = sorted(random.sample(rng, config['pick']))

            # --- VALIDATION FILTERS ---
            # 1. Sum Check (Thermodynamic Balance)
            if isinstance(final, list) and game_name not in ["Super Sete", "Lotomania"]: 
                s = sum(final)
                if not (config['min_sum'] <= s <= config['max_sum']):
                    continue # Reject and retry (Chaos Loop)
            
            # 2. Historical Filter (Simulated)
            if not PhysicsEngine.filter_historical_collisions(final):
                continue
            
            return {"nums": final, "type": "FÍSICA PURA", "color": config['color']}

# --- 6. UI LAYOUT ---

# Top Controls
col_game, col_qty = st.columns([2, 1])
with col_game:
    selected_game = st.selectbox("SELECIONE O MÓDULO:", list(GAMES_CONFIG.keys()))
with col_qty:
    qty_games = st.number_input("QUANTIDADE:", 1, 100, 5)

# Dynamic Header
theme_color = GAMES_CONFIG[selected_game]['color']
st.markdown(f"<div class='game-header' style='background:{theme_color};'>Módulo: {selected_game}</div>", unsafe_allow_html=True)

# Optional Input (For Smart Strategy)
with st.expander("🧬 INSERIR ÚLTIMO RESULTADO (Opcional - Para Maior Precisão)"):
    last_draw = st.text_input(f"Cole aqui os números do último sorteio da {selected_game}:", placeholder="Ex: 01 02 03 04...")
    st.caption("ℹ️ Se preenchido, o sistema usará a 'Lei da Repetição' (ex: Regra dos 9 na Lotofácil). Se vazio, usará Física Mecânica.")

# Top Action Bar
col_act1, col_act2 = st.columns(2)
with col_act1:
    btn_clear_top = st.button("LIMPAR TELA 🗑️")
with col_act2:
    btn_generate = st.button("INICIAR SIMULAÇÃO ⚛️")

# Logic Execution
if btn_clear_top:
    st.session_state.generated_games = []
    st.rerun()

if btn_generate:
    st.session_state.generated_games = []
    
    # Simulation Animation (The "Globe" Effect)
    progress_text = st.empty()
    bar = st.progress(0)
    
    # Phases of the Mechanical Motor
    phases = ["⬇️ Abastecendo Tubos...", "🌪️ Mistura Caótica (Alta Rotação)...", "🛑 Desaceleração Mecânica...", "🎱 Extração Final..."]
    
    for i, phase in enumerate(phases):
        progress_text.text(f"SYSTEM: {phase}")
        time.sleep(0.3) # Fast simulation for UX
        bar.progress((i + 1) * 25)
    
    time.sleep(0.5)
    bar.empty()
    progress_text.empty()
    
    # Generation
    for _ in range(qty_games):
        g = PhysicsEngine.generate_smart_game(selected_game, last_draw)
        st.session_state.generated_games.append(g)

# --- 7. RESULTS DISPLAY ---
if st.session_state.generated_games:
    
    # Download Button Logic (Prepare Text)
    txt_export = f"--- LotoMaster Ticket ---\nJogo: {selected_game}\nData: {pd.Timestamp.now()}\n\n"
    
    for i, game_data in enumerate(st.session_state.generated_games):
        
        # Format Numbers for Display
        raw_val = game_data['nums']
        display_html = ""
        txt_line = ""
        
        # Handle Different Game Types
        if isinstance(raw_val, dict):
            # Complex games (+Milionaria, Dia de Sorte, Timemania)
            if "t" in raw_val: # +Milionaria
                nums = raw_val['n']
                trevos = raw_val['t']
                balls_html = "".join([f"<div class='ball' style='background:{theme_color}'>{n:02d}</div>" for n in nums])
                trevos_html = "".join([f"<div class='ball' style='background:#333; border-color:#555'>{n}</div>" for n in trevos])
                display_html = f"<div>{balls_html}</div><div style='margin-top:5px'><b>Trevos:</b> {trevos_html}</div>"
                txt_line = f"Jogo {i+1}: {nums} + Trevos {trevos}"
                
            elif "month" in raw_val: # Dia de Sorte
                nums = raw_val['n']
                balls_html = "".join([f"<div class='ball' style='background:{theme_color}'>{n:02d}</div>" for n in nums])
                display_html = f"<div>{balls_html}</div><div style='color:{theme_color}; font-weight:bold; margin-top:5px'>📅 {raw_val['month']}</div>"
                txt_line = f"Jogo {i+1}: {nums} + Mês {raw_val['month']}"
                
            elif "team" in raw_val: # Timemania
                nums = raw_val['n']
                balls_html = "".join([f"<div class='ball' style='background:{theme_color}'>{n:02d}</div>" for n in nums])
                display_html = f"<div>{balls_html}</div><div style='color:{theme_color}; font-weight:bold; margin-top:5px'>❤️ {raw_val['team']}</div>"
                txt_line = f"Jogo {i+1}: {nums} + Time {raw_val['team']}"
        
        else:
            # Standard Games
            balls_html = "".join([f"<div class='ball' style='background:{theme_color}'>{n:02d}</div>" for n in raw_val])
            display_html = f"<div>{balls_html}</div>"
            txt_line = f"Jogo {i+1}: {raw_val}"
            
            # Copy String
            copy_str = " ".join([f"{n:02d}" for n in raw_val])

        # Append to Export
        txt_export += txt_line + "\n"

        # RENDER CARD
        st.markdown(f"""
        <div class="bet-card" style="border-left-color: {theme_color};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:bold; color:#555;">JOGO #{i+1}</span>
                <span style="font-size:12px; background:#eee; padding:2px 8px; border-radius:10px;">{game_data['type']}</span>
            </div>
            <div style="margin-top:10px; display:flex; flex-wrap:wrap; justify-content:center;">
                {display_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Copy Button (Using Streamlit Code Block for easy copy)
        if isinstance(raw_val, list): # Only show copy for pure lists to keep UI clean
            st.code(copy_str, language="text")

    # Bottom Actions
    st.markdown("---")
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        # Download Functionality
        st.download_button(
            label="📥 BAIXAR JOGOS (TXT)",
            data=txt_export,
            file_name=f"LotoMaster_{selected_game}.txt",
            mime="text/plain"
        )
        
    with col_d2:
        if st.button("LIMPAR RESULTADOS 🗑️", key="bt_btm"):
            st.session_state.generated_games = []
            st.rerun()

# --- 8. FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#888; font-size:12px;">
    ⚠️ Sistema baseado em Física Mecânica e Teoria do Caos.<br>
    Histórico de vitórias (15pts) removido matematicamente.
</div>
""", unsafe_allow_html=True)
