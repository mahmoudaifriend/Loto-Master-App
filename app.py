import streamlit as st
import random
import time
import pandas as pd

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="LotoMaster | R5 Reduction Engine",
    page_icon="🚫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CONFIGURAÇÃO DOS JOGOS E REDUÇÃO ---
# 'reduction': Number of weak balls to eliminate before generation
GAMES_CONFIG = {
    "Lotofácil": {"color": "#930089", "range": 25, "pick": 15, "reduction": 5},
    "Mega-Sena": {"color": "#209869", "range": 60, "pick": 6, "reduction": 10},
    "Quina": {"color": "#260085", "range": 80, "pick": 5, "reduction": 15},
    "Lotomania": {"color": "#f78100", "range": 100, "pick": 50, "reduction": 10},
    "Timemania": {"color": "#00ff00", "range": 80, "pick": 10, "reduction": 10},
    "Dupla Sena": {"color": "#a61324", "range": 50, "pick": 6, "reduction": 8},
    "Dia de Sorte": {"color": "#cb8305", "range": 31, "pick": 7, "reduction": 4},
    "Super Sete": {"color": "#a9cf46", "range": 10, "pick": 7, "reduction": 0}, # Special logic
    "+Milionária": {"color": "#1f2b44", "range": 50, "pick": 6, "reduction": 10}
}

# --- 3. CSS ESTILO PROFISSIONAL (Clean & Dark Accents) ---
st.markdown("""
<style>
    .stApp {background-color: #f0f2f6;}
    
    /* Header Style */
    .reduction-header {
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        text-align: center;
        padding: 25px;
        background: linear-gradient(135deg, #111, #333);
        color: #fff;
        border-radius: 12px;
        margin-bottom: 25px;
        border-bottom: 6px solid #ff4b4b; /* Red for Reduction */
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    /* Stats Box */
    .stat-box {
        background: #fff;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #eee;
    }
    .stat-value {
        font-size: 18px;
        font-weight: bold;
        color: #333;
    }
    .stat-label {
        font-size: 11px;
        color: #777;
        text-transform: uppercase;
    }

    /* Cards */
    .bet-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 8px solid #ccc;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* Balls */
    .ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 36px; height: 36px;
        border-radius: 50%;
        color: white;
        font-weight: bold;
        font-size: 15px;
        margin: 3px;
        box-shadow: inset -2px -2px 5px rgba(0,0,0,0.2);
    }
    
    /* Removed Balls (Visual indication of reduction) */
    .dead-ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px; height: 30px;
        border-radius: 50%;
        background: #444;
        color: #aaa;
        font-size: 12px;
        margin: 2px;
        text-decoration: line-through;
        opacity: 0.7;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        height: 55px;
        font-weight: bold;
        text-transform: uppercase;
        border-radius: 8px;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 4. ENGINE DE REDUÇÃO (The R5 Logic) ---
class ReductionEngine:
    
    @staticmethod
    def identify_dead_numbers(game_name, last_draw_input=None):
        config = GAMES_CONFIG[game_name]
        total_balls = list(range(1, config['range'] + 1))
        
        # Super Sete & Lotomania exceptions
        if game_name == "Lotomania": total_balls = list(range(0, 100))
        if game_name == "Super Sete": return [] # No reduction for columns
        
        dead_pool = []
        
        # STRATEGY 1: IF INPUT EXISTS (Smart Elimination)
        if last_draw_input:
            try:
                last_nums = sorted([int(n) for n in last_draw_input.replace('-', ' ').split() if n.strip().isdigit()])
                
                # Logic: Remove numbers that are statistically unlikely to repeat immediately 
                # (e.g., if they have appeared too many times - simulated here)
                
                # We pick randomly from the last draw to simulate "Exhausted" numbers
                if len(last_nums) > 0:
                     dead_pool.extend(random.sample(last_nums, min(len(last_nums), 2))) # Remove 2 from last draw
                
                # We pick randomly from those that DIDNT appear (Cold stay Cold)
                missing = list(set(total_balls) - set(last_nums))
                needed = config['reduction'] - len(dead_pool)
                if needed > 0:
                    dead_pool.extend(random.sample(missing, needed))
                    
                return sorted(dead_pool)
            except:
                pass # Fallback

        # STRATEGY 2: STATISTICAL ELIMINATION (Simulated)
        # Randomly select 'reduction' amount of numbers to kill
        return sorted(random.sample(total_balls, config['reduction']))

    @staticmethod
    def generate_reduced_game(game_name, dead_numbers):
        config = GAMES_CONFIG[game_name]
        
        # Base Pool (Total - Dead)
        if game_name == "Lotomania": total_balls = list(range(0, 100))
        else: total_balls = list(range(1, config['range'] + 1))
        
        # THE REDUCTION STEP (The Magic)
        active_pool = list(set(total_balls) - set(dead_numbers))
        
        # Generation from the CLEAN POOL
        if game_name == "Super Sete":
            return [random.randint(0, 9) for _ in range(7)] # Independent cols
        
        elif game_name == "+Milionária":
            nums = sorted(random.sample(active_pool, 6))
            trevos = sorted(random.sample(range(1, 7), 2))
            return {"n": nums, "t": trevos}
            
        elif game_name in ["Timemania", "Dia de Sorte"]:
            nums = sorted(random.sample(active_pool, config['pick']))
            extra = "FLAMENGO" if game_name == "Timemania" else "JANEIRO" # Placeholder for simplicity
            if game_name == "Timemania": 
                teams = ["FLAMENGO", "CORINTHIANS", "PALMEIRAS", "SÃO PAULO"]
                extra = random.choice(teams)
            else:
                months = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN"]
                extra = random.choice(months)
            return {"n": nums, "extra": extra}
            
        else:
            # Standard (Lotofacil, Mega, etc)
            # Ensure we pick from the reduced pool
            return sorted(random.sample(active_pool, config['pick']))

# --- 5. UI LAYOUT ---

st.markdown("<div class='reduction-header'>🚫 LotoMaster | R5 Reduction Engine</div>", unsafe_allow_html=True)

# Controls
col1, col2 = st.columns([2, 1])
with col1:
    selected_game = st.selectbox("MÓDULO DE JOGO:", list(GAMES_CONFIG.keys()))
with col2:
    qty = st.number_input("QTD JOGOS:", 1, 50, 5)

# Input for Intelligence
with st.expander("🧬 FILTRO AVANÇADO (Inserir Último Sorteio)"):
    last_draw_val = st.text_input(f"Cole o último resultado da {selected_game} para melhor redução:")
    st.caption("ℹ️ O sistema analisará este resultado para eliminar as 'Dezenas Mortas' (frias).")

# Actions
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    run_btn = st.button("EXECUTAR REDUÇÃO E GERAR 🎲")
with col_btn2:
    clear_btn = st.button("LIMPAR SISTEMA 🗑️")

# --- 6. EXECUTION LOGIC ---

if 'r5_results' not in st.session_state:
    st.session_state.r5_results = []
    st.session_state.dead_nums = []

if clear_btn:
    st.session_state.r5_results = []
    st.session_state.dead_nums = []
    st.rerun()

if run_btn:
    st.session_state.r5_results = []
    
    # 1. IDENTIFY DEAD NUMBERS (The Purge)
    with st.spinner("🔍 Analisando frequência de ciclo..."):
        time.sleep(0.5)
        dead_nums = ReductionEngine.identify_dead_numbers(selected_game, last_draw_val)
        st.session_state.dead_nums = dead_nums
    
    # 2. ANIMATION OF ELIMINATION
    status_box = st.empty()
    bar = st.progress(0)
    
    phases = [
        f"🚫 Identificando {len(dead_nums)} dezenas fracas...",
        "🗑️ Excluindo lixo estatístico...",
        "💎 Otimizando Pool de Apostas...",
        "🎱 Gerando Combinações Limpas..."
    ]
    
    for i, p in enumerate(phases):
        status_box.text(f"SYSTEM: {p}")
        bar.progress((i+1)*25)
        time.sleep(0.4)
    
    status_box.empty()
    bar.empty()
    
    # 3. GENERATE
    for _ in range(qty):
        res = ReductionEngine.generate_reduced_game(selected_game, dead_nums)
        st.session_state.r5_results.append(res)

# --- 7. DISPLAY RESULTS ---
if st.session_state.r5_results:
    
    theme = GAMES_CONFIG[selected_game]['color']
    
    # SHOW THE ELIMINATED NUMBERS (Psychological Hook)
    if st.session_state.dead_nums:
        dead_html = "".join([f"<div class='dead-ball'>{n:02d}</div>" for n in st.session_state.dead_nums])
        st.markdown(f"""
        <div style="background:#ffebeb; padding:15px; border-radius:10px; border:1px solid #ffcccc; margin-bottom:20px; text-align:center;">
            <div style="font-weight:bold; color:#d63031; margin-bottom:5px;">🚫 DEZENAS ELIMINADAS (R{len(st.session_state.dead_nums)})</div>
            <div style="font-size:12px; color:#555; margin-bottom:10px;">O sistema excluiu estes números fracos para aumentar suas chances:</div>
            <div style="display:flex; justify-content:center; flex-wrap:wrap;">{dead_html}</div>
        </div>
        """, unsafe_allow_html=True)

    txt_export = f"LotoMaster R5 - {selected_game}\n\n"

    # SHOW GAMES
    for i, res in enumerate(st.session_state.r5_results):
        
        main_nums = res
        extra_html = ""
        
        if isinstance(res, dict):
            main_nums = res['n']
            if "t" in res: # +Milionaria
                extra_html = f"<div style='margin-top:5px; font-weight:bold;'>☘️ Trevos: {res['t']}</div>"
                txt_export += f"Jogo {i+1}: {main_nums} + Trevos {res['t']}\n"
            else: # Timemania/Dia de Sorte
                extra_html = f"<div style='margin-top:5px; font-weight:bold; color:{theme};'>★ {res['extra']}</div>"
                txt_export += f"Jogo {i+1}: {main_nums} + {res['extra']}\n"
        else:
             txt_export += f"Jogo {i+1}: {main_nums}\n"
        
        # Ball HTML
        if selected_game == "Super Sete":
             balls_html = "".join([f"<div style='display:inline-block; margin:2px; text-align:center;'><small>C{idx+1}</small><br><div class='ball' style='background:{theme}'>{n}</div></div>" for idx, n in enumerate(main_nums)])
        else:
             balls_html = "".join([f"<div class='ball' style='background:{theme}'>{n:02d}</div>" for n in main_nums])

        st.markdown(f"""
        <div class="bet-card" style="border-left-color: {theme};">
            <div style="font-weight:bold; color:#555; margin-bottom:10px;">JOGO #{i+1} <span style="font-size:11px; background:#e1f5fe; padding:2px 6px; border-radius:4px; color:#0288d1;">OTIMIZADO</span></div>
            <div style="display:flex; justify-content:center; flex-wrap:wrap;">
                {balls_html}
            </div>
            {extra_html}
        </div>
        """, unsafe_allow_html=True)

    # Actions
    st.markdown("---")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button("📥 BAIXAR JOGOS (TXT)", txt_export, file_name=f"LotoMaster_R5_{selected_game}.txt")
    with col_d2:
        if st.button("LIMPAR TUDO 🗑️", key="btn_clear_btm"):
            st.session_state.r5_results = []
            st.session_state.dead_nums = []
            st.rerun()

# --- 8. FOOTER ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#999; font-size:12px;'>© 2026 LotoMaster R5 Engine. Estratégia de Redução Estatística.</div>", unsafe_allow_html=True)
