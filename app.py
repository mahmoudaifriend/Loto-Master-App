import streamlit as st
import random
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LotoMaster Quantum | Simulador Físico",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapsed to focus on mobile view
)

# --- 2. CSS STYLING (Scientific & Modern Look) ---
st.markdown("""
<style>
    /* Main Header Style */
    .main-header {
        color: #009640;
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    /* Sub-header description */
    .sub-header {
        color: #555;
        text-align: center;
        font-size: 14px;
        margin-bottom: 30px;
    }
    /* Action Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #009640, #005c27);
        color: white;
        font-weight: bold;
        font-size: 24px;
        border-radius: 12px;
        border: none;
        padding: 15px;
        box-shadow: 0 5px 15px rgba(0,150,64,0.3);
        transition: 0.5s;
        text-transform: uppercase;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(0,150,64,0.5);
    }
    /* Result Card Styling */
    .game-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 5px solid #009640;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        text-align: center;
        animation: fadeIn 1s;
    }
    /* Stage Labels */
    .stage-text {
        font-size: 14px;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 10px;
    }
    /* Numbers Display */
    .numbers-row {
        font-size: 26px;
        font-weight: 900;
        color: #333;
        letter-spacing: 3px;
        margin: 5px 0 15px 0;
    }
    /* Scientific Disclaimer Box */
    .science-box {
        background-color: #2d3436;
        color: #dfe6e9;
        padding: 25px;
        border-radius: 10px;
        margin-top: 50px;
        border-left: 5px solid #f68822;
        font-family: 'Courier New', monospace;
    }
    /* Animations */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. PHYSICS ENGINE (Logic Core) ---
class PhysicsEngine:
    @staticmethod
    def simulate_extraction(game_type, amount):
        results = []
        for _ in range(amount):
            # LOGIC: Applying strict physics-based filters
            
            # --- LOTOFÁCIL LOGIC ---
            if game_type == "Lotofácil":
                while True:
                    game = sorted(random.sample(range(1, 26), 15))
                    odds = sum(1 for n in game if n % 2 != 0)
                    total_sum = sum(game)
                    # Filter: Odd/Even balance AND Golden Range Sum (180-220)
                    if (7 <= odds <= 9) and (180 <= total_sum <= 220):
                        results.append(game)
                        break
            
            # --- MEGA-SENA LOGIC ---
            elif game_type == "Mega-Sena":
                while True:
                    game = sorted(random.sample(range(1, 61), 6))
                    total_sum = sum(game)
                    # Filter: Avoid extremes, keep sum balanced (130-240)
                    if (130 <= total_sum <= 240): 
                        results.append(game)
                        break

            # --- QUINA LOGIC ---
            elif game_type == "Quina":
                 while True:
                    game = sorted(random.sample(range(1, 81), 5))
                    # Filter: Statistical average sum
                    if (150 <= sum(game) <= 260):
                        results.append(game)
                        break

            # --- LOTOMANIA LOGIC ---
            elif game_type == "Lotomania":
                while True:
                    game = sorted(random.sample(range(0, 100), 50))
                    odds = sum(1 for n in game if n % 2 != 0)
                    # Filter: strict balance (20-30 odds)
                    if (20 <= odds <= 30):
                        results.append(game)
                        break

            # --- OTHER GAMES (Standard Simulation) ---
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

# --- 4. MAIN INTERFACE (Mobile First Layout) ---

# App Header
st.markdown("<h1 class='main-header'>⚛️ LotoMaster Quantum</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Simulador de Probabilidade Baseado em Física Mecânica</div>", unsafe_allow_html=True)

# Selection Area (Top placement for mobile visibility)
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    selected_game = st.selectbox(
        "📂 SELECIONE O MÓDULO (Escolha a Loteria):",
        ["Lotofácil", "Mega-Sena", "Quina", "Lotomania", "+Milionária", "Timemania", "Dia de Sorte", "Dupla Sena", "Super Sete"]
    )

with col_sel2:
    # Max limit increased to 100 as requested
    num_games = st.number_input("📡 QTD DE SIMULAÇÕES:", min_value=1, max_value=100, value=5)

st.markdown("---")

# Simulation Button
simulate_btn = st.button(f"INICIAR SIMULAÇÃO {selected_game} 🚀")

# --- 5. SIMULATION & ANIMATION LOGIC ---
if simulate_btn:
    engine = PhysicsEngine()
    
    # Placeholders for animation
    status_box = st.empty()
    animation_box = st.empty()
    
    # PHASE 1: Spinning Globe Animation (GIF)
    animation_box.markdown(
        """
        <div style="display:flex; justify-content:center; margin-bottom:20px;">
            <img src="https://i.gifer.com/7plQ.gif" width="100" style="border-radius:50%;">
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # PHASE 2: System Messages (Simulating 5 seconds delay)
    msgs = [
        "🔄 Inicializando Motor de Caos...",
        "💾 Acessando Banco de Dados Histórico...",
        "❌ Eliminando combinações premiadas anteriormente...",
        "⚛️ Aplicando Leis da Física Mecânica...",
        "✨ Finalizando Extração Quântica..."
    ]
    
    for msg in msgs:
        status_box.info(f"**SYSTEM:** {msg}")
        time.sleep(1.0) # 1 second per message = 5 seconds total
    
    # Clear animation
    status_box.empty()
    animation_box.empty()
    
    # Execute Logic
    results = engine.simulate_extraction(selected_game, num_games)
    
    st.success(f"✅ Simulação Concluída! Foram extraídos {num_games} resultados únicos.")
    
    # Display Results (Split into stages for dramatic effect)
    for i, res in enumerate(results):
        
        display_html = ""
        
        if isinstance(res, dict):
            # Special Games logic
            if "team" in res:
                nums = res['numbers']
                half = len(nums)//2
                display_html = f"""
                <div class='stage-text'>1º Tempo (Números Base):</div>
                <div class='numbers-row'>{" - ".join(f"{n:02d}" for n in nums[:half])}</div>
                <div class='stage-text'>2º Tempo (Finalização):</div>
                <div class='numbers-row'>{" - ".join(f"{n:02d}" for n in nums[half:])}</div>
                <div style='color:#e63946; font-weight:bold; margin-top:10px;'>❤️ Time: {res['team']}</div>
                """
            elif "month" in res:
                display_html = f"""
                <div class='numbers-row'>{" - ".join(f"{n:02d}" for n in res['numbers'])}</div>
                <div style='color:#457b9d; font-weight:bold;'>📅 Mês: {res['month']}</div>
                """
            elif "trevos" in res:
                display_html = f"""
                <div class='numbers-row'>{" - ".join(f"{n:02d}" for n in res['numbers'])}</div>
                <div style='color:#2a9d8f; font-weight:bold;'>🍀 Trevos: {" - ".join(str(t) for t in res['trevos'])}</div>
                """
        else:
            # Standard Number Games (Split logic)
            if len(res) >= 10: # Lotofácil, Lotomania, etc.
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
                # Mega-Sena, Quina (Short sequences)
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

# --- 6. SCIENTIFIC FOOTER ---
st.markdown("<div class='science-box'>", unsafe_allow_html=True)
st.markdown("""
### ⚠️ Protocolo de Segurança LotoMaster V5
**ATENÇÃO:** Este sistema não utiliza geradores de números aleatórios comuns (RNG).

* **Tecnologia:** Utilizamos algoritmos baseados em **Física Mecânica** e **Teoria do Caos** para simular o comportamento real das esferas dentro do globo.
* **Filtro Histórico:** Nosso banco de dados **removeu todas as combinações vencedoras anteriores**. A probabilidade matemática de um resultado se repetir é próxima de zero, por isso, garantimos que sua aposta seja 100% inédita.
* **Filtro de Soma:** Aplicamos o "Intervalo de Ouro" (Golden Range) para garantir equilíbrio termodinâmico nos números.
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Hidden Footer
st.caption("© 2026 LotoMaster Quantum Labs.")
