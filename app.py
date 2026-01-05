import streamlit as st
import random
import time
import pandas as pd

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="LotoMaster | Geometric Engine",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. COLORS & CONFIGURATION (Caixa Standards) ---
GAMES_CONFIG = {
    "Lotofácil": {"color": "#930089", "range": 25, "pick": 15},
    "Mega-Sena": {"color": "#209869", "range": 60, "pick": 6},
    "Quina": {"color": "#260085", "range": 80, "pick": 5},
    "Lotomania": {"color": "#f78100", "range": 100, "pick": 50},
    "Timemania": {"color": "#00ff00", "range": 80, "pick": 10},
    "Dupla Sena": {"color": "#a61324", "range": 50, "pick": 6},
    "Dia de Sorte": {"color": "#cb8305", "range": 31, "pick": 7},
    "Super Sete": {"color": "#a9cf46", "range": 10, "pick": 7},
    "+Milionária": {"color": "#1f2b44", "range": 50, "pick": 6}
}

# --- 3. CSS STYLING (Professional Dark/Clean Look) ---
st.markdown("""
<style>
    /* Main Layout */
    .stApp {background-color: #f4f6f9;}
    
    /* Header */
    .geo-header {
        font-family: 'Helvetica', sans-serif;
        text-transform: uppercase;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #1e1e1e, #333);
        color: #fff;
        border-radius: 10px;
        margin-bottom: 20px;
        border-bottom: 5px solid #00ff41; /* Tech Green */
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        height: 55px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        text-transform: uppercase;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Lotto Ball */
    .ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px; height: 40px;
        border-radius: 50%;
        color: white;
        font-weight: bold;
        font-size: 16px;
        margin: 4px;
        box-shadow: inset -3px -3px 5px rgba(0,0,0,0.3), 3px 3px 5px rgba(255,255,255,0.3);
        border: 2px solid rgba(255,255,255,0.8);
    }
    
    /* Result Card */
    .result-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-left: 8px solid #333; /* Dynamic */
        transition: transform 0.2s;
    }
    .result-card:hover {
        transform: translateY(-2px);
    }
    
    /* Tags */
    .tag {
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 10px;
        background: #eee;
        color: #555;
        font-weight: bold;
        margin-left: 10px;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 4. THE GEOMETRIC ENGINE (The Core Logic) ---
class GeometricEngine:
    
    @staticmethod
    def generate(game_name, last_draw_input=None):
        config = GAMES_CONFIG[game_name]
        
        # --- 1. LOTOFÁCIL (Frame & Core Geometry) ---
        if game_name == "Lotofácil":
            # Definition of Geometry
            moldura = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25] # 16 nums
            miolo   = [7, 8, 9, 12, 13, 14, 17, 18, 19] # 9 nums
            
            # Smart Logic: If last draw exists, use "Rule of 9"
            if last_draw_input:
                try:
                    last_nums = sorted([int(n) for n in last_draw_input.replace('-', ' ').split() if n.strip().isdigit()])
                    if len(last_nums) == 15:
                        # 9 Repeats + 6 New
                        all_nums = list(range(1, 26))
                        missing = list(set(all_nums) - set(last_nums))
                        
                        final = sorted(random.sample(last_nums, 9) + random.sample(missing, 6))
                        return {"n": final, "desc": "PADRÃO R9 (REPETIÇÃO)"}
                except:
                    pass # Fallback

            # Pure Geometric Logic (If no input)
            # Target: 10 Moldura + 5 Miolo (Ideal Balance)
            while True:
                sel_moldura = random.sample(moldura, 10)
                sel_miolo = random.sample(miolo, 5)
                final = sorted(sel_moldura + sel_miolo)
                
                # Filter: Sum check (180-220)
                if 180 <= sum(final) <= 220:
                    return {"n": final, "desc": "GEOMETRIA (10 MOLDURA / 5 MIOLO)"}

        # --- 2. MEGA-SENA (Quadrant Balance) ---
        elif game_name == "Mega-Sena":
            # Divide grid into 4 Quadrants
            q1 = [n for n in range(1, 61) if n % 10 in [1,2,3,4,5] and n <= 30]
            q2 = [n for n in range(1, 61) if n % 10 in [6,7,8,9,0] and n <= 30]
            q3 = [n for n in range(1, 61) if n % 10 in [1,2,3,4,5] and n > 30]
            q4 = [n for n in range(1, 61) if n % 10 in [6,7,8,9,0] and n > 30]
            
            while True:
                # Pick distributed numbers
                final = []
                # Ensure distribution
                final.extend(random.sample(q1, random.randint(1, 2)))
                final.extend(random.sample(q2, random.randint(1, 2)))
                final.extend(random.sample(q3, random.randint(1, 2)))
                final.extend(random.sample(q4, random.randint(0, 1))) # Remaining
                
                # Fill up to 6 if missing
                while len(final) < 6:
                    n = random.randint(1, 60)
                    if n not in final: final.append(n)
                
                final = sorted(final[:6])
                if 130 <= sum(final) <= 240: # Sum Filter
                    return {"n": final, "desc": "GEOMETRIA (QUADRANTES)"}

        # --- 3. QUINA (Vertical Spread) ---
        elif game_name == "Quina":
            while True:
                final = sorted(random.sample(range(1, 81), 5))
                # Avoid clustering (e.g., 1,2,3)
                if all(final[i+1] - final[i] > 1 for i in range(len(final)-1)):
                    return {"n": final, "desc": "ESPALHAMENTO VERTICAL"}

        # --- 4. LOTOMANIA (Mirror Logic) ---
        elif game_name == "Lotomania":
            # Pick 25 from 1-50, 25 from 51-100
            p1 = random.sample(range(0, 51), 25)
            p2 = random.sample(range(51, 100), 25)
            return {"n": sorted(p1 + p2), "desc": "ESPELHAMENTO 50/50"}

        # --- 5. TIMEMANIA ---
        elif game_name == "Timemania":
            nums = sorted(random.sample(range(1, 81), 10))
            teams = ["FLAMENGO", "CORINTHIANS", "PALMEIRAS", "SÃO PAULO", "VASCO", "SANTOS", "GRÊMIO", "INTER", "CRUZEIRO", "ATLÉTICO-MG"]
            return {"n": nums, "extra": random.choice(teams), "desc": "PADRÃO TIME"}

        # --- 6. DIA DE SORTE ---
        elif game_name == "Dia de Sorte":
            nums = sorted(random.sample(range(1, 32), 7))
            months = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
            return {"n": nums, "extra": random.choice(months), "desc": "PADRÃO MÊS"}

        # --- 7. +MILIONÁRIA ---
        elif game_name == "+Milionária":
            nums = sorted(random.sample(range(1, 51), 6))
            trevos = sorted(random.sample(range(1, 7), 2))
            return {"n": nums, "extra_list": trevos, "desc": "MATRIZ MILIONÁRIA"}
            
        # --- 8. SUPER SETE ---
        elif game_name == "Super Sete":
            # One number per column (0-9)
            cols = [random.randint(0, 9) for _ in range(7)]
            return {"n": cols, "desc": "COLUNAS INDEPENDENTES"}

        # --- FALLBACK (Dupla Sena, etc) ---
        else:
            final = sorted(random.sample(range(1, config['range']+1), config['pick']))
            return {"n": final, "desc": "RANDOMIZAÇÃO OTIMIZADA"}

# --- 5. UI LAYOUT ---

st.markdown("<div class='geo-header'>📐 LotoMaster | Geometric Engine V1</div>", unsafe_allow_html=True)

# Selection Panel
col1, col2 = st.columns([2, 1])
with col1:
    selected_game = st.selectbox("SELECIONE O MÓDULO:", list(GAMES_CONFIG.keys()))
with col2:
    qty = st.number_input("QUANTIDADE:", 1, 50, 5)

# Optional Last Draw Input (Crucial for Rule of 9)
with st.expander("🧬 ENTRADA DE DADOS (Último Resultado - Opcional)"):
    last_draw_val = st.text_input(f"Cole os números do último sorteio ({selected_game}):")

# Theme Color Setup
theme = GAMES_CONFIG[selected_game]['color']

# Actions
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    generate = st.button("PROJETAR JOGOS 🎲")
with col_btn2:
    clear = st.button("LIMPAR 🗑️")

# --- 6. LOGIC & DISPLAY ---

if 'results' not in st.session_state:
    st.session_state.results = []

if clear:
    st.session_state.results = []
    st.rerun()

if generate:
    st.session_state.results = []
    
    # Physics Simulation (The Globe Effect)
    status = st.empty()
    bar = st.progress(0)
    
    phases = [
        "🏗️ Construindo Malha Geométrica...",
        "📐 Aplicando Filtros Espaciais (Moldura/Miolo)...",
        "⚖️ Balanceando Cargas...",
        "💎 Finalizando Escultura..."
    ]
    
    for i, p in enumerate(phases):
        status.info(p)
        time.sleep(0.4)
        bar.progress((i+1)*25)
    
    bar.empty()
    status.empty()
    
    # Generate
    for _ in range(qty):
        res = GeometricEngine.generate(selected_game, last_draw_val)
        st.session_state.results.append(res)

# Render Results
if st.session_state.results:
    
    txt_export = f"LotoMaster - {selected_game}\n\n"
    
    for i, res in enumerate(st.session_state.results):
        
        # Determine content type
        main_nums = res['n']
        desc = res.get('desc', 'Standard')
        
        html_content = ""
        
        # Special Renderers
        if selected_game == "+Milionária":
            trevos = res['extra_list']
            balls = "".join([f"<div class='ball' style='background:{theme}'>{n:02d}</div>" for n in main_nums])
            trevos_html = "".join([f"<div class='ball' style='background:#333; border-color:#666'>{t}</div>" for t in trevos])
            html_content = f"<div>{balls}</div><div style='margin-top:8px'><b>Trevos:</b> {trevos_html}</div>"
            txt_export += f"Jogo {i+1}: {main_nums} + Trevos {trevos}\n"
            
        elif selected_game in ["Timemania", "Dia de Sorte"]:
            extra = res['extra']
            balls = "".join([f"<div class='ball' style='background:{theme}'>{n:02d}</div>" for n in main_nums])
            html_content = f"<div>{balls}</div><div style='margin-top:8px; color:{theme}; font-weight:bold;'>★ {extra}</div>"
            txt_export += f"Jogo {i+1}: {main_nums} + {extra}\n"
            
        elif selected_game == "Super Sete":
            # Vertical Columns visual
            cols_html = "".join([f"<div style='display:inline-block; text-align:center; margin:2px;'><div style='font-size:10px'>C{idx+1}</div><div class='ball' style='background:{theme}'>{n}</div></div>" for idx, n in enumerate(main_nums)])
            html_content = f"<div>{cols_html}</div>"
            txt_export += f"Jogo {i+1}: {main_nums}\n"
            
        else: # Standard (Lotofacil, Mega, etc)
            balls = "".join([f"<div class='ball' style='background:{theme}'>{n:02d}</div>" for n in main_nums])
            html_content = f"<div>{balls}</div>"
            txt_export += f"Jogo {i+1}: {main_nums}\n"

        # Card Render
        st.markdown(f"""
        <div class="result-card" style="border-left-color: {theme};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                <span style="font-weight:bold; color:#333;">JOGO #{i+1}</span>
                <span class="tag">{desc}</span>
            </div>
            <div style="display:flex; justify-content:center; flex-wrap:wrap;">
                {html_content}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Copy helper for list games
        if isinstance(main_nums, list) and selected_game not in ["Super Sete"]:
             st.code(" ".join([f"{n:02d}" for n in main_nums]), language="text")

    # Bottom Actions
    st.markdown("---")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button("📥 BAIXAR TXT", txt_export, file_name=f"LotoMaster_{selected_game}.txt")
    with col_d2:
        if st.button("LIMPAR TUDO 🗑️", key="btm_clear"):
            st.session_state.results = []
            st.rerun()

# --- 7. FOOTER ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 LotoMaster Geometric Engine - Tecnologia de Padrões Espaciais.")
