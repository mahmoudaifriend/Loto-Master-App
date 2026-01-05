import streamlit as st
import random
import time
import pandas as pd

# --- 1. CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="LotoMaster | Hybrid Engine (Geo+Red)",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Game Configurations (Color, Range, Pick, Reduction Amount)
GAMES_CONFIG = {
    "Lotofácil": {"color": "#930089", "range": 25, "pick": 15, "purge": 4},
    "Mega-Sena": {"color": "#209869", "range": 60, "pick": 6, "purge": 10},
    "Quina": {"color": "#260085", "range": 80, "pick": 5, "purge": 15},
    "Lotomania": {"color": "#f78100", "range": 100, "pick": 50, "purge": 10},
    "Timemania": {"color": "#00ff00", "range": 80, "pick": 10, "purge": 10},
    "Dupla Sena": {"color": "#a61324", "range": 50, "pick": 6, "purge": 8},
    "Dia de Sorte": {"color": "#cb8305", "range": 31, "pick": 7, "purge": 5},
    "Super Sete": {"color": "#a9cf46", "range": 10, "pick": 7, "purge": 0},
    "+Milionária": {"color": "#1f2b44", "range": 50, "pick": 6, "purge": 10}
}

# --- 2. CSS STYLING (Premium Dark Interface) ---
st.markdown("""
<style>
    .stApp {background-color: #121212; color: #e0e0e0;}
    
    /* Hybrid Header */
    .hybrid-header {
        background: linear-gradient(90deg, #000428, #004e92);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        border-bottom: 4px solid #00ff41;
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
        margin-bottom: 25px;
    }
    
    /* Stats Panel */
    .stats-panel {
        background: #1e1e1e;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #333;
        text-align: center;
    }
    
    /* Bet Card */
    .bet-card {
        background: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #555;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .bet-card:hover { transform: scale(1.01); }
    
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
    
    /* Purged Ball Style */
    .purged-ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px; height: 30px;
        border-radius: 50%;
        background: #2d0000;
        color: #ff4444;
        border: 1px solid #ff4444;
        margin: 2px;
        font-size: 12px;
        text-decoration: line-through;
    }

    /* Inputs & Buttons */
    .stTextInput>div>div>input { background-color: #2c2c2c; color: white; border: 1px solid #444; }
    .stButton>button { width: 100%; height: 55px; font-weight: bold; text-transform: uppercase; border-radius: 8px; }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. THE HYBRID ENGINE (Reduction + Geometry) ---
class HybridEngine:
    
    @staticmethod
    def get_dead_numbers(game_name, last_draw_input):
        config = GAMES_CONFIG[game_name]
        
        # Define Universe
        if game_name == "Lotomania": universe = list(range(0, 100))
        elif game_name == "Super Sete": return [] 
        else: universe = list(range(1, config['range'] + 1))
        
        dead_pool = []
        
        # INTELLIGENT REDUCTION
        if last_draw_input:
            try:
                last_nums = sorted([int(n) for n in last_draw_input.replace('-', ' ').split() if n.strip().isdigit()])
                
                # Logic: Remove 2 "Exhausted" (from last draw) + Rest "Cold" (from missing)
                if len(last_nums) > 0:
                    dead_pool.extend(random.sample(last_nums, min(len(last_nums), 2))) 
                
                missing = list(set(universe) - set(last_nums))
                needed = config['purge'] - len(dead_pool)
                
                if needed > 0 and len(missing) >= needed:
                    dead_pool.extend(random.sample(missing, needed))
                    
                return sorted(dead_pool)
            except:
                pass 

        # Fallback: Random Purge
        return sorted(random.sample(universe, config['purge']))

    @staticmethod
    def generate_hybrid_game(game_name, dead_numbers, last_draw_input=None):
        config = GAMES_CONFIG[game_name]
        
        # Universe Setup
        if game_name == "Lotomania": universe = list(range(0, 100))
        else: universe = list(range(1, config['range'] + 1))
        
        # 1. APPLY REDUCTION (Clean Pool)
        clean_pool = list(set(universe) - set(dead_numbers))
        
        # 2. APPLY GEOMETRY & LOGIC
        
        # --- LOTOFÁCIL SPECIAL LOGIC ---
        if game_name == "Lotofácil":
            moldura = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25]
            miolo   = [7, 8, 9, 12, 13, 14, 17, 18, 19]
            
            # Intersection with Clean Pool
            clean_moldura = [n for n in clean_pool if n in moldura]
            clean_miolo   = [n for n in clean_pool if n in miolo]
            
            # Hybrid Strategy: Rule of 9 + Geometry
            if last_draw_input:
                try:
                    last_nums = sorted([int(n) for n in last_draw_input.replace('-', ' ').split() if n.strip().isdigit()])
                    # Try to keep ~9 repeats from clean pool
                    clean_repeats = [n for n in clean_pool if n in last_nums]
                    clean_missing = [n for n in clean_pool if n not in last_nums]
                    
                    # Chaos Factor: Sometimes take 8 or 10 repeats
                    k_rep = random.choice([8, 9, 10])
                    if len(clean_repeats) < k_rep: k_rep = len(clean_repeats)
                    
                    p1 = random.sample(clean_repeats, k_rep)
                    p2 = random.sample(clean_missing, 15 - k_rep)
                    return sorted(p1 + p2)
                except:
                    pass
            
            # Pure Geometry (Balance 10/5)
            # Adjust target based on available clean numbers
            target_m = 10 if len(clean_moldura) >= 10 else len(clean_moldura)
            target_c = 15 - target_m
            
            p1 = random.sample(clean_moldura, target_m)
            p2 = random.sample(clean_miolo, target_c)
            return sorted(p1 + p2)

        # --- MEGA-SENA (Quadrants) ---
        elif game_name == "Mega-Sena":
            # Quadrants logic on Clean Pool
            while True:
                final = sorted(random.sample(clean_pool, 6))
                # Simple spread check
                if final[-1] - final[0] > 15: # Avoid extreme clamping
                    return final

        # --- STANDARD (Others) ---
        elif game_name == "+Milionária":
            nums = sorted(random.sample(clean_pool, 6))
            trevos = sorted(random.sample(range(1, 7), 2))
            return {"n": nums, "t": trevos}
            
        elif game_name in ["Timemania", "Dia de Sorte"]:
            nums = sorted(random.sample(clean_pool, config['pick']))
            extra = "DATA"
            if game_name == "Timemania": 
                teams = ["FLAMENGO", "CORINTHIANS", "PALMEIRAS", "SÃO PAULO"]
                extra = random.choice(teams)
            else:
                months = ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN"]
                extra = random.choice(months)
            return {"n": nums, "extra": extra}
            
        elif game_name == "Super Sete":
            return [random.randint(0, 9) for _ in range(7)]

        else:
            return sorted(random.sample(clean_pool, config['pick']))

# --- 4. UI LAYOUT ---

st.markdown("<div class='hybrid-header'><h1>🧬 LotoMaster Hybrid</h1><h3>GEOMETRIA + REDUÇÃO R5</h3></div>", unsafe_allow_html=True)

# Main Controls
c1, c2 = st.columns([2, 1])
with c1:
    game_select = st.selectbox("SELECIONE O MÓDULO:", list(GAMES_CONFIG.keys()))
with c2:
    qty_select = st.number_input("QUANTIDADE:", 1, 50, 5)

# Intelligence Input
with st.expander("🧠 CÉREBRO DA IA (Entrada de Dados)", expanded=True):
    last_draw = st.text_input(f"Cole o último resultado ({game_select}):", placeholder="Ex: 01 02 03...")
    st.caption("ℹ️ Obrigatório para ativar o Modo Híbrido Completo (Repetição + Geometria).")

# Action Bar
cb1, cb2 = st.columns(2)
with cb1:
    btn_run = st.button("EXECUTAR PROTOCOLO 🚀")
with cb2:
    btn_clean = st.button("REINICIAR SISTEMA 🗑️")

# --- 5. EXECUTION ---

if 'hybrid_results' not in st.session_state:
    st.session_state.hybrid_results = []
    st.session_state.dead_list = []

if btn_clean:
    st.session_state.hybrid_results = []
    st.session_state.dead_list = []
    st.rerun()

if btn_run:
    # 1. PURGE PHASE
    dead = HybridEngine.get_dead_numbers(game_select, last_draw)
    st.session_state.dead_list = dead
    
    # Simulation
    with st.spinner("⚛️ Fundindo algoritmos geométricos com redução estatística..."):
        time.sleep(1.0)
    
    # 2. GENERATION PHASE
    results = []
    for _ in range(qty_select):
        res = HybridEngine.generate_hybrid_game(game_select, dead, last_draw)
        results.append(res)
    st.session_state.hybrid_results = results

# --- 6. DISPLAY ---

if st.session_state.hybrid_results:
    theme = GAMES_CONFIG[game_select]['color']
    
    # Show Purged Numbers
    if st.session_state.dead_list:
        purged_html = "".join([f"<div class='purged-ball'>{n:02d}</div>" for n in st.session_state.dead_list])
        st.markdown(f"""
        <div class="stats-panel" style="border-color: #ff4444; margin-bottom: 20px;">
            <div style="color:#ff4444; font-weight:bold; margin-bottom:5px;">🚫 DEZENAS ELIMINADAS (PURGE)</div>
            <div>{purged_html}</div>
            <div style="font-size:11px; color:#888; margin-top:5px;">Estas dezenas foram removidas matematicamente para limpar o pool.</div>
        </div>
        """, unsafe_allow_html=True)

    txt_export = f"LotoMaster Hybrid - {game_select}\nData: {pd.Timestamp.now()}\n\n"

    for i, res in enumerate(st.session_state.hybrid_results):
        
        main = res
        extra_html = ""
        
        if isinstance(res, dict):
            main = res['n']
            if "t" in res:
                extra_html = f"<div style='margin-top:8px;'><b>🍀 Trevos:</b> {res['t']}</div>"
                txt_export += f"Jogo {i+1}: {main} + Trevos {res['t']}\n"
            else:
                extra_html = f"<div style='margin-top:8px; color:{theme}; font-weight:bold;'>★ {res['extra']}</div>"
                txt_export += f"Jogo {i+1}: {main} + {res['extra']}\n"
        else:
            txt_export += f"Jogo {i+1}: {main}\n"
            
        # HTML Balls
        if game_select == "Super Sete":
             balls_html = "".join([f"<div style='display:inline-block; margin:2px; text-align:center;'><small style='color:#666'>C{idx+1}</small><br><div class='ball' style='border-color:{theme}; background:transparent;'>{n}</div></div>" for idx, n in enumerate(main)])
        else:
             balls_html = "".join([f"<div class='ball' style='background:{theme}'>{n:02d}</div>" for n in main])

        st.markdown(f"""
        <div class="bet-card" style="border-left-color: {theme};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-weight:bold; color:#fff;">JOGO #{i+1}</span>
                <span style="font-size:10px; background:#00ff41; color:#000; padding:2px 8px; border-radius:10px; font-weight:bold;">HYBRID</span>
            </div>
            <div style="display:flex; justify-content:center; flex-wrap:wrap;">
                {balls_html}
            </div>
            {extra_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c_d1, c_d2 = st.columns(2)
    with c_d1:
        st.download_button("📥 BAIXAR RESULTADOS (TXT)", txt_export, file_name=f"Hybrid_{game_select}.txt")
    with c_d2:
        if st.button("LIMPAR TELA 🗑️", key="b_clr"):
            st.session_state.hybrid_results = []
            st.session_state.dead_list = []
            st.rerun()

# --- 7. FOOTER ---
st.markdown("<br><div style='text-align:center; color:#555; font-size:12px;'>© 2026 LotoMaster Hybrid Technology.</div>", unsafe_allow_html=True)
