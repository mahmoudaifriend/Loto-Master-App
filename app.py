import streamlit as st
import time
import random

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA", layout="wide", initial_sidebar_state="collapsed")

# --- 2. PROFESSIONAL CASINO CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');

    /* Global Style */
    .stApp {
        background: radial-gradient(circle at top, #2b0035 0%, #000000 100%);
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }

    /* Professional Titles */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: clamp(1.8rem, 5vw, 3.5rem);
        font-weight: 700;
        text-align: center;
        color: #ff00ff;
        text-shadow: 0 0 20px #ff00ff;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        font-size: clamp(0.9rem, 3vw, 1.2rem);
        color: #d100d1;
        margin-bottom: 25px;
        font-weight: 300;
    }

    /* 3D Balls Style */
    .ball {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 4px;
        font-weight: 700;
        font-size: 16px;
        color: white;
        background: radial-gradient(circle at 12px 12px, #ff55ff, #4b0082);
        box-shadow: inset -4px -4px 8px rgba(0,0,0,0.6), 4px 4px 10px rgba(0,0,0,0.4);
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    .ball-motor {
        width: 30px;
        height: 30px;
        background: radial-gradient(circle at 8px 8px, #ffffff, #800080);
        color: #2b0035;
        font-size: 12px;
        margin: 2px;
    }

    /* Simulation Motor (The Big One) */
    .motor-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 40px auto;
        position: relative;
    }
    .big-motor {
        width: 280px;
        height: 280px;
        border: 8px double #ff00ff;
        border-radius: 50%;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding: 15px;
        background: rgba(255, 0, 255, 0.05);
        box-shadow: 0 0 30px rgba(255, 0, 255, 0.2);
    }
    
    .spin-slow { animation: rotate 10s linear infinite; }
    .spin-fast { animation: rotate 0.5s linear infinite; }

    @keyframes rotate { 100% { transform: rotate(360deg); } }

    /* Inputs & Buttons */
    .stTextInput input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #ff00ff !important;
        border: 2px solid #800080 !important;
        border-radius: 10px !important;
        font-size: 22px !important;
        text-align: center;
    }
    
    .stButton button {
        background: linear-gradient(145deg, #800080, #ff00ff);
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        width: 100%;
    }

    /* Result Containers (Mobile Friendly) */
    .result-box {
        background: rgba(43, 0, 53, 0.7);
        border: 1px solid #ff00ff;
        border-radius: 12px;
        padding: 12px;
        margin: 10px 0;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }

    /* Footer Warning */
    .legal-footer {
        font-size: 0.75rem;
        text-align: center;
        color: #888;
        border-top: 1px solid #444;
        margin-top: 50px;
        padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE INIT ---
if 'processed' not in st.session_state: st.session_state.processed = False
if 'final_list' not in st.session_state: st.session_state.final_list = []

# --- 4. ENGINE (Logic) ---
def matrix_19_logic(draw_list):
    # Fixed algorithmic logic for matrix 19
    missing = [n for n in range(1, 26) if n not in draw_list]
    # Strongest 9 from previous draw (simulated for UI)
    strong = random.sample(draw_list, 9)
    return sorted(missing + strong)

def generate_filtered_bet(matrix):
    # Simulates the 8 filters mentioned in road-map
    while True:
        bet = sorted(random.sample(matrix, 15))
        # Basic filters check (Odd/Even, Sum)
        odds = len([n for n in bet if n % 2 != 0])
        if odds in [7, 8] and 180 <= sum(bet) <= 210:
            return bet

# --- 5. HEADER ---
st.markdown('<div class="main-title">TOTOLOTO ALGORITMIA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Jogue com inteligência</div>', unsafe_allow_html=True)

# Central Logo
st.markdown("<div style='text-align:center; margin-bottom:20px;'><span style='font-size:60px;'>💠</span></div>", unsafe_allow_html=True)

# --- 6. INPUT SECTION ---
input_col, clear_col = st.columns([5, 1])
with input_col:
    last_draw_raw = st.text_input("", placeholder="Insira o último sorteio (ex: 01 02 04...)", label_visibility="collapsed")
with clear_col:
    if st.button("🗑️"): 
        st.session_state.processed = False
        st.rerun()

if last_draw_raw:
    try:
        draw_nums = [int(n) for n in last_draw_raw.split()]
        if len(draw_nums) == 15:
            balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(draw_nums)])
            st.markdown(f'<div style="text-align:center; padding:15px;">{balls_html}</div>', unsafe_allow_html=True)
            st.session_state.valid_draw = draw_nums
        else:
            st.warning("⚠️ Insira 15 números.")
    except:
        st.error("⚠️ Erro no formato.")

# --- 7. FILTERING SECTION ---
st.markdown("---")
filter_col1, filter_col2, filter_col3 = st.columns([1, 2, 1])
with filter_col2:
    st.markdown("<h4 style='text-align:center;'>Telas de Filtração (19 Números)</h4>", unsafe_allow_html=True)
    f_btn_col, f_motor_col = st.columns([3, 1])
    with f_btn_col:
        filter_btn = st.button("EXECUTAR TAREFA")
    with f_motor_col:
        motor_placeholder = st.empty()
    
    if filter_btn:
        if 'valid_draw' in st.session_state:
            # Small motor animation
            for _ in range(15):
                motor_placeholder.markdown('<div style="width:30px; height:30px; border:3px solid #ff00ff; border-radius:50%; border-top:3px solid transparent; animation: rotate 0.5s linear infinite;"></div>', unsafe_allow_html=True)
                time.sleep(1)
            motor_placeholder.empty()
            st.session_state.m19 = matrix_19_logic(st.session_state.valid_draw)
            st.session_state.processed = True
            st.markdown("<p style='color:#00ff00; text-align:center;'>✅ Têm sido filtrado com sucesso!</p>", unsafe_allow_html=True)
        else:
            st.error("⚠️ Adicione o sorteio primeiro.")

# --- 8. BIG MOTOR & SIMULATION ---
st.markdown("---")
# The Big Wheel UI
wheel_area = st.empty()
def draw_wheel(style="spin-slow"):
    balls_inside = "".join(['<div class="ball ball-motor">X</div>' for _ in range(25)])
    wheel_area.markdown(f'<div class="motor-container"><div class="big-motor {style}">{balls_inside}</div></div>', unsafe_allow_html=True)

draw_wheel() # Initial state

num_bets = st.selectbox("Escolha o número de رهانات:", [10, 20, 30, 40, 50, 100, 200], index=0)

if st.button("محاكاة"):
    if st.session_state.processed:
        st.session_state.final_list = []
        # Simulation Logic
        for i in range(num_bets):
            # 4.5s Fast
            draw_wheel("spin-fast")
            time.sleep(4.5)
            # 2s Slow (Pop-out effect)
            draw_wheel("spin-slow")
            time.sleep(2)
            # Generate bet
            st.session_state.final_list.append(generate_filtered_bet(st.session_state.m19))
        st.rerun() # Refresh to show results
    else:
        st.error("⚠️ Execute a filtração antes da simulação.")

# --- 9. RESULTS ---
if st.session_state.final_list:
    st.markdown("### 🏆 Apostas Geradas")
    full_output = ""
    for idx, b in enumerate(st.session_state.final_list):
        b_str = " ".join([f"{n:02}" for n in b])
        full_output += b_str + "\n"
        
        # Display Box with Copy Icon
        col_res, col_copy = st.columns([5, 1])
        with col_res:
            res_balls = "".join([f'<div class="ball">{n:02}</div>' for n in b])
            st.markdown(f'<div class="result-box">{res_balls}</div>', unsafe_allow_html=True)
        with col_copy:
            st.write("##")
            st.button("📋", key=f"copy_{idx}", help="Copiar Aposta")

    # Final Actions
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.download_button("Baixar TXT", full_output, file_name="totoloto.txt")
    with c2: 
        if st.button("Limpar Tudo"):
            st.session_state.final_list = []
            st.rerun()
    with c3: st.code(full_output, language='text')

# --- 10. LEGAL FOOTER ---
st.markdown(f"""
    <div class="legal-footer">
        <p>⚠️ PROIBIDO PARA MENORES DE 21 ANOS.</p>
        <p>Este aplicativo é estritamente estatístico e educativo. Não garantimos nem prometemos lucros. Jogue com responsabilidade.</p>
        <p>TOTOLOTO ALGORITMIA © 2026</p>
    </div>
""", unsafe_allow_html=True)
