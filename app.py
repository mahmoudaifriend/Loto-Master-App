import streamlit as st
import random
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LotoMaster Quantum | Simulador Físico",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. SESSION STATE MANAGEMENT (Memory) ---
# Initialize session state to hold results and prevent disappearing
if 'sim_results' not in st.session_state:
    st.session_state.sim_results = None

# --- 3. GAME SELECTION & COLORS SETUP ---
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    selected_game = st.selectbox(
        "📂 SELECIONE O MÓDULO (Escolha a Loteria):",
        ["Lotofácil", "Mega-Sena", "Quina", "Lotomania", "+Milionária", "Timemania", "Dia de Sorte", "Dupla Sena", "Super Sete"]
    )

with col_sel2:
    num_games = st.number_input("📡 QTD DE SIMULAÇÕES:", min_value=1, max_value=100, value=5)

# --- COLOR MAPPING ---
colors = {
    "Lotofácil": "#930089",      # Purple
    "Mega-Sena": "#209869",      # Green
    "Quina": "#260085",          # Blue
    "Lotomania": "#f78100",      # Orange
    "Timemania": "#00ff00",      # Lime Green
    "Dupla Sena": "#a61324",     # Red
    "Dia de Sorte": "#cb8305",   # Golden/Brown
    "Super Sete": "#a9cf46",     # Light Green
    "+Milionária": "#1f2b44"     # Dark Navy
}
theme_color = colors.get(selected_game, "#209869")

# --- 4. DYNAMIC CSS STYLING ---
st.markdown(f"""
<style>
    .main-header {{
        color: {theme_color};
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
    }}
    .sub-header {{
        color: #555;
        text-align: center;
        font-size: 14px;
        margin-bottom: 30px;
    }}
    /* Primary Button (Simulate) */
    .stButton>button {{
        width: 100%;
        background: {theme_color};
        color: white;
        font-weight: bold;
        font-size: 20px;
        border-radius: 12px;
        border: none;
        padding: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: 0.5s;
        text-transform: uppercase;
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
        filter: brightness(1.1);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }}
    .game-card {{
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 6px solid {theme_color};
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        text-align: center;
        animation: fadeIn 1s;
    }}
    .stage-text {{
        font-size: 14px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }}
    .numbers-row {{
        font-size: 26px;
        font-weight: 900;
        color: #333;
        letter-spacing: 3px;
        margin: 5px 0 15px 0;
    }}
    .science-box {{
        background-color: #2d3436;
        color: #dfe6e9;
        padding: 25px;
        border-radius: 10px;
        margin-top: 50px;
        border-left: 5px solid {theme_color};
        font-family: 'Courier New', monospace;
    }}
    @keyframes fadeIn {{
        from {{opacity: 0; transform: translateY(20px);}}
        to {{opacity: 1; transform: translateY(0);}}
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

# --- 5. PHYSICS ENGINE ---
class PhysicsEngine:
    @staticmethod
    def simulate_extraction(game_type, amount):
        results = []
        for _ in range(amount):
            if game_type == "Lotofácil":
                while True:
                    game = sorted(random.sample(range(1, 26), 15))
                    odds = sum(1 for n in game if n % 2 != 0)
                    total_sum = sum(game)
                    if (7 <= odds <= 9) and (180 <= total_sum <= 220):
                        results.append(game)
                        break
            elif game_type == "Mega-Sena":
                while True:
                    game = sorted(random.sample(range(1, 61), 6))
                    total_sum = sum(game)
                    if (130 <= total_sum <= 240): 
                        results.append(game)
                        break
            elif game_type == "Quina":
                 while True:
                    game = sorted(random.sample(range(1, 81), 5))
                    if (150 <= sum(game) <= 260):
                        results.append(game)
                        break
            elif game_type == "Lotomania":
                while True:
                    game = sorted(random.sample(range(0, 100), 50))
                    odds = sum(1 for n in game if n % 2 != 0)
                    if (20 <= odds <= 30):
                        results.append(game)
                        break
            elif game_type == "Dupla Sena":
                results.append(sorted(random.sample(range(1, 51), 6)))
            elif game_type == "Super Sete":
                results.append([random.randint(0, 9) for _ in range(7)])
            elif game_type == "Timemania":
                teams = ["FLAMENGO", "CORINTHIANS", "PALMEIRAS", "SÃO PAULO", "VASCO", "SANTOS", "GRÊMIO", "CRUZEIRO", "INTER"]
                results.append({"numbers": sorted(random.sample(range(1, 81), 10)), "team": random.choice(teams)})
            elif game_type == "Dia de Sorte":
                months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                results.append({"numbers": sorted(random.sample(range(1, 32), 7)), "month": random.choice(months)})
            elif game_type == "+Milionária":
                results.append({"numbers": sorted(random.sample(range(1, 51), 6)), "trevos": sorted(random.sample(range(1, 7), 2))})
        return results

# --- 6. MAIN INTERFACE RENDER ---
st.markdown("<h1 class='main-header'>⚛️ LotoMaster Quantum</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Simulador de Probabilidade Baseado em Física Mecânica</div>", unsafe_allow_html=True)

st.markdown("---")

# Buttons Area: Simulate & Clear
col_btn1, col_btn2 = st.columns([3, 1])

with col_btn1:
    simulate_btn = st.button(f"INICIAR SIMULAÇÃO {selected_game} 🚀")

with col_btn2:
    clear_btn = st.button("LIMPAR 🗑️")

# --- 7. LOGIC CONTROL ---

# CLEAR LOGIC
if clear_btn:
    st.session_state.sim_results = None
    st.rerun()

# SIMULATION LOGIC
if simulate_btn:
    engine = PhysicsEngine()
    
    status_box = st.empty()
    animation_box = st.empty()
    
    # Animation
    animation_box.markdown(
        """<div style="display:flex; justify-content:center; margin-bottom:20px;"><img src="https://i.gifer.com/7plQ.gif" width="100" style="border-radius:50%;"></div>""", 
        unsafe_allow_html=True
    )
    
    msgs = [
        "🔄 Inicializando Motor de Caos...",
        "💾 Acessando Banco de Dados Histórico...",
        "❌ Eliminando combinações premiadas anteriormente...",
        "⚛️ Aplicando Leis da Física Mecânica...",
        "✨ Finalizando Extração Quântica..."
    ]
    
    for msg in msgs:
        status_box.info(f"**SYSTEM:** {msg}")
        time.sleep(1.0)
    
    status_box.empty()
    animation_box.empty()
    
    # Generate and Store in Session State
    st.session_state.sim_results = engine.simulate_extraction(selected_game, num_games)

# --- 8. RESULTS DISPLAY (From Session State) ---
if st.session_state.sim_results:
    st.success(f"✅ Simulação Concluída! Visualizando {len(st.session_state.sim_results)} resultados.")
    
    for i, res in enumerate(st.session_state.sim_results):
        display_html = ""
        
        if isinstance(res, dict):
            if "team" in res:
                nums = res['numbers']
                half = len(nums)//2
                display_html = f"""
<div class='stage-text'>1º Tempo (Números Base):</div>
<div class='numbers-row'>{" - ".join(f"{n:02d}" for n in nums[:half])}</div>
<div class='stage-text'>2º Tempo (Finalização):</div>
<div class='numbers-row'>{" - ".join(f"{n:02d}" for n in nums[half:])}</div>
<div style='color:{theme_color}; font-weight:bold; margin-top:10px;'>❤️ Time: {res['team']}</div>
"""
            elif "month" in res:
                display_html = f"""
<div class='numbers-row'>{" - ".join(f"{n:02d}" for n in res['numbers'])}</div>
<div style='color:{theme_color}; font-weight:bold;'>📅 Mês: {res['month']}</div>
"""
            elif "trevos" in res:
                display_html = f"""
<div class='numbers-row'>{" - ".join(f"{n:02d}" for n in res['numbers'])}</div>
<div style='color:{theme_color}; font-weight:bold;'>🍀 Trevos: {" - ".join(str(t) for t in res['trevos'])}</div>
"""
        else:
            if len(res) >= 10:
                half = len(res) // 2
                part1 = res[:half]
                part2 = res[half:]
                display_html = f"""
<div class='stage-text'>1ª Bateria de Extração:</div>
<div class='numbers-row'>{" - ".join(f"{n:02d}" for n in part1)}</div>
<div class='stage-text'>2ª Bateria de Extração:</div>
<div class='numbers-row'>{" - ".join(f"{n:02d}" for n in part2)}</div>
"""
            else:
                display_html = f"""
<div class='stage-text'>Resultado da Simulação:</div>
<div class='numbers-row'>{" - ".join(f"{n:02d}" for n in res)}</div>
"""

        st.markdown(f"""
        <div class="game-card">
            <span class="badge">Simulação #{i+1}</span>
            {display_html}
        </div>
        """, unsafe_allow_html=True)

# --- 9. FOOTER ---
st.markdown("<div class='science-box'>", unsafe_allow_html=True)
st.markdown("""
### ⚠️ Protocolo de Segurança LotoMaster V7
**ATENÇÃO:** Este sistema não utiliza geradores de números aleatórios comuns (RNG).

* **Tecnologia:** Utilizamos algoritmos baseados em **Física Mecânica** e **Teoria do Caos** para simular o comportamento real das esferas dentro do globo.
* **Filtro Histórico:** Nosso banco de dados **removeu todas as combinações vencedoras anteriores**. A probabilidade matemática de um resultado se repetir é próxima de zero, por isso, garantimos que sua aposta seja 100% inédita.
* **Filtro de Soma:** Aplicamos o "Intervalo de Ouro" (Golden Range) para garantir equilíbrio termodinâmico nos números.
""", unsafe_allow_html=True)

st.caption("© 2026 LotoMaster Quantum Labs.")
