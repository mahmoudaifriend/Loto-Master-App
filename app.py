import streamlit as st
import time
import random

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PROFISSIONAL (ESTILO CASINO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');

    .stApp {
        background: radial-gradient(circle at top, #1a0022 0%, #000000 100%);
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }

    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #ff00ff;
        text-shadow: 0 0 15px #ff00ff;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 0.9rem;
        color: #d100d1;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }

    .ball {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 2px;
        font-weight: 700;
        font-size: 14px;
        color: white;
        background: radial-gradient(circle at 10px 10px, #ff55ff, #4b0082);
        box-shadow: inset -3px -3px 6px rgba(0,0,0,0.7), 3px 3px 8px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.2);
    }

    .motor-outer {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px auto;
        width: 260px;
        height: 260px;
        border: 5px solid #800080;
        border-radius: 50%;
        position: relative;
        background: rgba(43, 0, 53, 0.4);
        box-shadow: 0 0 40px rgba(255, 0, 255, 0.3);
        overflow: hidden;
    }

    .motor-inner {
        width: 100%;
        height: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }

    .spin-fast { animation: shuffle 0.4s linear infinite; }
    .spin-slow { animation: shuffle 4s linear infinite; }

    @keyframes shuffle {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .bet-card {
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid #4b0082;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        min-height: 60px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
    }

    .stButton button {
        background: linear-gradient(to right, #4b0082, #ff00ff) !important;
        color: white !important;
        border-radius: 5px !important;
        font-weight: bold !important;
    }

    .legal-footer {
        font-size: 0.7rem;
        text-align: center;
        color: #666;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #222;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGICA DO SISTEMA SOBERANO ---
def get_sovereign_matrix(last_draw):
    all_n = list(range(1, 26))
    missing = [n for n in all_n if n not in last_draw]
    strong_prev = random.sample(last_draw, 9)
    return sorted(missing + strong_prev)

def generate_sovereign_bet(matrix):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    fib = [1, 2, 3, 5, 8, 13, 21]
    while True:
        bet = sorted(random.sample(matrix, 15))
        if len([n for n in bet if n % 2 != 0]) not in [7, 8]: continue
        if len([n for n in bet if n in primes]) not in [5, 6]: continue
        if not (180 <= sum(bet) <= 210): continue
        if len([n for n in bet if n in fib]) not in [3, 4, 5]: continue
        gaps = [bet[i+1] - bet[i] for i in range(len(bet)-1)]
        if any(g > 7 for g in gaps): continue
        return bet

# --- 4. SESSION STATE ---
if 'matrix' not in st.session_state: st.session_state.matrix = []
if 'sim_results' not in st.session_state: st.session_state.sim_results = []
if 'current_view' not in st.session_state: st.session_state.current_view = []

# --- 5. INTERFACE ---
st.markdown('<div class="main-title">TOTOLOTO ALGORITMIA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">JOGUE COM INTELIGÊNCIA</div>', unsafe_allow_html=True)

col_in, col_clr = st.columns([5, 1])
with col_in:
    draw_input = st.text_input("Último Sorteio:", placeholder="01 02 04...", label_visibility="collapsed")
with col_clr:
    if st.button("🗑️"):
        st.session_state.clear()
        st.rerun()

if draw_input:
    try:
        nums = [int(x) for x in draw_input.split()]
        if len(nums) == 15:
            st.session_state.valid_draw = nums
            balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(nums)])
            st.markdown(f'<div style="text-align:center;">{balls_html}</div>', unsafe_allow_html=True)
        else: st.warning("Insira 15 números.")
    except: st.error("Erro no formato.")

st.markdown("---")
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    f_col_l, f_col_r = st.columns([3, 1])
    with f_col_l: btn_f = st.button("EXECUTAR TAREFA DE FILTRAGEM")
    with f_col_r: motor_f = st.empty()
    
    if btn_f:
        if 'valid_draw' in st.session_state:
            for _ in range(15):
                motor_f.markdown('<div style="width:25px; height:25px; border:3px solid #ff00ff; border-top:3px solid transparent; border-radius:50%; animation: shuffle 0.5s linear infinite;"></div>', unsafe_allow_html=True)
                time.sleep(1)
            motor_f.empty()
            st.session_state.matrix = get_sovereign_matrix(st.session_state.valid_draw)
            st.success("✅ Têm sido filtrado com sucesso!")
        else: st.error("Insira o sorteio primeiro.")

st.markdown("---")
motor_area = st.empty()
def update_big_motor(speed="spin-slow"):
    balls = "".join(['<div class="ball" style="opacity:0.4; width:18px; height:18px;">X</div>' for _ in range(25)])
    motor_area.markdown(f'<div class="motor-outer"><div class="motor-inner {speed}">{balls}</div></div>', unsafe_allow_html=True)

update_big_motor()

qty = st.selectbox("Quantidade de Apostas:", [10, 20])
sim_btn = st.button("SIMULAR AGORA 🚀")
results_placeholder = st.empty()

if sim_btn:
    if st.session_state.matrix:
        # Pre-geração usando o Sistema Soberano
        st.session_state.sim_results = [generate_sovereign_bet(st.session_state.matrix) for _ in range(qty)]
        st.session_state.current_view = [[] for _ in range(qty)]
        
        for ball_idx in range(15):
            # Fase 1: Rápida (4.5s)
            update_big_motor("spin-fast")
            time.sleep(4.5)
            
            # Fase 2: Lenta/Ejeção (2s)
            update_big_motor("spin-slow")
            
            # Atualiza visualização das bolas
            for bet_idx in range(qty):
                st.session_state.current_view[bet_idx].append(st.session_state.sim_results[bet_idx][ball_idx])
            
            with results_placeholder.container():
                for i in range(qty):
                    current_balls = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(st.session_state.current_view[i])])
                    st.markdown(f'<div class="bet-card"><b>#{i+1:02}</b> &nbsp; {current_balls}</div>', unsafe_allow_html=True)
            
            time.sleep(2)
        st.balloons()
    else:
        st.error("Execute a filtragem primeiro.")

st.markdown("""
<div class="legal-footer">
    <p>⚠️ PROIBIDO PARA MENORES DE 21 ANOS.</p>
    <p>Ferramenta estatística e educativa. Sem garantia de lucro. Jogue com responsabilidade.</p>
    <p>TOTOLOTO ALGORITMIA © 2026</p>
</div>
""", unsafe_allow_html=True)
