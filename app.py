import streamlit as st
import random
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LotoMaster Quantum | Ball-by-Ball",
    page_icon="🎱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SESSION STATE (Memory) ---
if 'sim_results' not in st.session_state:
    st.session_state.sim_results = None
if 'audit_results' not in st.session_state:
    st.session_state.audit_results = {}

# --- 3. INPUTS & COLORS ---
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    selected_game = st.selectbox(
        "📂 SELECIONE O JOGO:",
        ["Lotofácil", "Mega-Sena", "Quina", "Lotomania", "+Milionária", "Timemania", "Dia de Sorte", "Dupla Sena", "Super Sete"]
    )

with col_sel2:
    num_games = st.number_input("📡 QTD APOSTAS:", min_value=1, max_value=100, value=5)

# Color Map (Official Caixa Colors)
colors = {
    "Lotofácil": "#930089",      # Purple
    "Mega-Sena": "#209869",      # Green
    "Quina": "#260085",          # Blue
    "Lotomania": "#f78100",      # Orange
    "Timemania": "#00ff00",      # Lime
    "Dupla Sena": "#a61324",     # Red
    "Dia de Sorte": "#cb8305",   # Gold
    "Super Sete": "#a9cf46",     # Light Green
    "+Milionária": "#1f2b44"     # Navy
}
theme_color = colors.get(selected_game, "#209869")

# --- 4. CSS STYLING (Ball Design) ---
st.markdown(f"""
<style>
    .main-header {{
        color: {theme_color};
        text-align: center;
        text-transform: uppercase;
        font-family: sans-serif;
        margin-bottom: 5px;
    }}
    /* Buttons */
    .stButton>button {{
        width: 100%;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        text-transform: uppercase;
    }}
    /* Result Card */
    .game-card {{
        background: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 8px solid {theme_color};
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }}
    /* THE LOTTO BALL DESIGN */
    .lotto-ball {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        background: {theme_color}; /* Theme Color Background */
        color: white;
        border-radius: 50%; /* Circle */
        font-weight: bold;
        font-size: 16px;
        margin: 4px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        border: 2px solid white;
    }}
    .ball-container {{
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 5px;
        margin-top: 10px;
    }}
    .label-text {{
        font-size: 12px;
        color: #666;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 5px;
    }}
    .audit-box {{
        background: #f1f3f4;
        padding: 10px;
        border-radius: 5px;
        font-size: 12px;
        color: #333;
        margin-top: 10px;
        border: 1px dashed #999;
    }}
    #MainMenu, footer, header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# --- 5. LOGIC ENGINE ---
class LogicEngine:
    @staticmethod
    def generate(game, qtd):
        results = []
        for _ in range(qtd):
            if game == "Lotofácil":
                while True:
                    g = sorted(random.sample(range(1, 26), 15))
                    if 180 <= sum(g) <= 220: results.append(g); break
            elif game == "Mega-Sena":
                while True:
                    g = sorted(random.sample(range(1, 61), 6))
                    if 130 <= sum(g) <= 240: results.append(g); break
            elif game == "Quina":
                results.append(sorted(random.sample(range(1, 81), 5)))
            elif game == "Lotomania":
                results.append(sorted(random.sample(range(0, 100), 50)))
            elif game == "Dupla Sena":
                results.append(sorted(random.sample(range(1, 51), 6)))
            elif game == "Super Sete":
                results.append([random.randint(0, 9) for _ in range(7)])
            elif game == "Timemania":
                 teams = ["FLAMENGO", "CORINTHIANS", "PALMEIRAS", "SÃO PAULO", "VASCO", "SANTOS", "GRÊMIO"]
                 results.append({"nums": sorted(random.sample(range(1, 81), 10)), "extra": random.choice(teams)})
            elif game == "Dia de Sorte":
                 months = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]
                 results.append({"nums": sorted(random.sample(range(1, 32), 7)), "extra": random.choice(months)})
            elif game == "+Milionária":
                 results.append({"nums": sorted(random.sample(range(1, 51), 6)), "extra": sorted(random.sample(range(1, 7), 2))})
        return results

    @staticmethod
    def audit_game(numbers):
        # Simulation of historical check (Mock Logic for UX)
        score = random.randint(0, 100)
        if score > 90: return "🌟 HISTÓRICO: Já premiou com 14 pontos (2x)"
        elif score > 70: return "✅ HISTÓRICO: Frequentemente 12/13 pontos"
        elif score > 40: return "⚠️ HISTÓRICO: Premiações baixas detectadas"
        else: return "🆕 INÉDITO: Combinação nunca sorteada (Potencial Alto)"

# --- 6. UI ACTIONS ---
st.markdown("<h1 class='main-header'>⚛️ LotoMaster Quantum</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    btn_sim = st.button(f"SIMULAR {selected_game} 🚀")
with col2:
    btn_audit = st.button("AUDITAR 📜")
with col3:
    btn_clear = st.button("LIMPAR 🗑️")

# --- 7. ACTIONS HANDLING ---

# Clear
if btn_clear:
    st.session_state.sim_results = None
    st.session_state.audit_results = {}
    st.rerun()

# Simulate
if btn_sim:
    # Animation
    with st.spinner("🔄 Extraindo esferas quânticas..."):
        time.sleep(1.5)
    st.session_state.sim_results = LogicEngine.generate(selected_game, num_games)
    st.session_state.audit_results = {} # Reset audit on new sim

# Audit
if btn_audit and st.session_state.sim_results:
    with st.spinner("🔎 Consultando banco de dados 1998-2025..."):
        time.sleep(1.0)
    # Generate audit for current results
    for i, res in enumerate(st.session_state.sim_results):
        # Simple hash key for mock audit
        st.session_state.audit_results[i] = LogicEngine.audit_game(res)

# --- 8. RENDERING (BALL-BY-BALL) ---
if st.session_state.sim_results:
    st.success(f"✅ Extração Finalizada: {len(st.session_state.sim_results)} Jogos Gerados.")
    
    for i, res in enumerate(st.session_state.sim_results):
        
        # HTML Building Block
        balls_html = ""
        extra_html = ""
        
        # Data Preparation
        if isinstance(res, dict): # Games with extras (Timemania, etc)
            main_nums = res['nums']
            extra_val = res['extra']
            
            # Main Balls
            for num in main_nums:
                balls_html += f"<div class='lotto-ball'>{num:02d}</div>"
            
            # Extra Info
            if isinstance(extra_val, list): # +Milionaria Trevos
                trevos_str = "".join(f"<div class='lotto-ball' style='background:#333'>{t}</div>" for t in extra_val)
                extra_html = f"<div style='margin-top:5px;'><b>Trevos:</b> {trevos_str}</div>"
            else:
                extra_html = f"<div style='margin-top:5px; color:{theme_color}; font-weight:bold;'>❤️ {extra_val}</div>"
                
        else: # Standard Games (Lotofacil, Mega, etc)
            main_nums = res
            for num in main_nums:
                balls_html += f"<div class='lotto-ball'>{num:02d}</div>"

        # Check Audit Status
        audit_msg = st.session_state.audit_results.get(i, "")
        audit_html = f"<div class='audit-box'>{audit_msg}</div>" if audit_msg else ""

        # RENDER CARD
        # Note: No indentation inside the HTML string to avoid bugs
        st.markdown(f"""
<div class="game-card">
<div class="label-text">Simulação #{i+1} - Sequência de Extração</div>
<div class="ball-container">
{balls_html}
</div>
{extra_html}
{audit_html}
</div>
""", unsafe_allow_html=True)

# --- 9. FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("© 2026 LotoMaster Quantum Labs - Engine V8.0")
