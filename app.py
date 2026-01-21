import streamlit as st
import time
import random
from collections import Counter

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TOTOLOTO SNIPER PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PROFISSIONAL (MANTIDO CONFORME SOLICITADO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');
    
    .stApp { background: radial-gradient(circle at top, #1a0022 0%, #000000 100%); color: #ffffff; font-family: 'Roboto', sans-serif; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 3rem; text-align: center; color: #fff; text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 40px #ff00ff; margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 0.9rem; color: #d100d1; margin-bottom: 30px; letter-spacing: 2px; font-weight: bold; text-shadow: 0 0 5px #d100d1; }
    
    .ball { 
        width: 38px; height: 38px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin: 3px; 
        font-weight: 800; font-size: 14px; color: white; 
        background: radial-gradient(circle at 35% 35%, #ffb3ff, #ff00ff 45%, #4b0082 90%);
        box-shadow: inset -4px -4px 10px rgba(0,0,0,0.8), inset 3px 3px 6px rgba(255,255,255,0.4), 0 5px 15px rgba(0,0,0,0.5);
        position: relative; transition: transform 0.2s ease;
    }
    
    .motor-outer { display: flex; justify-content: center; align-items: center; margin: 25px auto; width: 280px; height: 280px; border: 4px solid #ff00ff; border-radius: 50%; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(8px); box-shadow: 0 0 50px rgba(255, 0, 255, 0.3), inset 0 0 30px #000; overflow: hidden; position: relative; }
    .motor-inner { width: 100%; height: 100%; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; padding: 35px; }
    
    @keyframes chaos3d {
        0% { transform: translate(0, 0) scale(1) rotate(0deg); }
        25% { transform: translate(-20px, 15px) scale(1.1) rotate(90deg); }
        50% { transform: translate(20px, -20px) scale(0.9) rotate(180deg); }
        75% { transform: translate(-15px, -20px) scale(1.1) rotate(270deg); }
        100% { transform: translate(0, 0) scale(1) rotate(360deg); }
    }
    .chaos-active .ball { animation: chaos3d 0.4s infinite linear alternate; }
    
    .spin-fast { animation: shuffle 0.4s linear infinite; }
    .spin-slow { animation: shuffle 4s linear infinite; }
    @keyframes shuffle { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    
    .bet-card { background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(15px); border: 1px solid rgba(255,0,255,0.2); border-radius: 15px; padding: 12px; margin-bottom: 12px; display: flex; flex-wrap: wrap; align-items: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .range-info { font-size: 0.7rem; color: #ff00ff; border: 1px solid #ff00ff; padding: 2px 5px; border-radius: 4px; margin-right: 10px; opacity: 0.8; }

    div.stButton > button { background: linear-gradient(45deg, #4b0082, #ff00ff) !important; color: white !important; font-weight: bold !important; border-radius: 10px; border: none; transition: 0.3s; }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 0 20px #ff00ff; }
    
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(to right, #004d00, #00cc00) !important;
        color: white !important;
        border: 1px solid #00ff00 !important;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. NOVA LÓGICA SNIPER (SISTEMA 9+6) ---
def generate_sniper_bet(last_draw, start, end):
    pool = list(range(start, end + 1))
    last_in_pool = [n for n in last_draw if n in pool]
    missing_in_pool = [n for n in pool if n not in last_draw]
    
    # Adaptive 9+6 logic based on range constraints
    n_last = min(len(last_in_pool), 9)
    n_miss = 15 - n_last
    
    if len(missing_in_pool) < n_miss:
        n_miss = len(missing_in_pool)
        n_last = 15 - n_miss
        
    s_last = random.sample(last_in_pool, n_last)
    s_miss = random.sample(missing_in_pool, n_miss)
    return sorted(s_last + s_miss)

# --- 4. SESSION STATE ---
if 'sim_results' not in st.session_state: st.session_state.sim_results = []
if 'current_view' not in st.session_state: st.session_state.current_view = []
if 'last_draw' not in st.session_state: st.session_state.last_draw = []

# --- 5. INTERFACE ---
st.markdown('<div class="main-title">💎 TOTOLOTO PRO 💎</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SISTEMA SNIPER ALGORÍTMICO V2</div>', unsafe_allow_html=True)

# ENTRADA DO ÚLTIMO SORTEIO (OBRIGATÓRIO)
with st.container():
    last_draw_input = st.text_input("INSIRA O ÚLTIMO SORTEIO (15 números separados por espaço):", placeholder="Ex: 01 04 05 06 07 09 12 13 17 18 20 21 22 23 25")
    if last_draw_input:
        try:
            nums = sorted([int(n) for n in last_draw_input.split() if n.strip()])
            if len(nums) == 15:
                st.session_state.last_draw = nums
                st.success(f"✅ Sorteio de Base Carregado: {nums}")
            else:
                st.warning("⚠️ Insira exatamente 15 números.")
        except:
            st.error("❌ Formato inválido.")

st.markdown("---")
motor_placeholder = st.empty()

def update_globe(speed="spin-slow", chaos=""):
    balls_html = "".join([f'<div class="ball" style="opacity:0.4; width:18px; height:18px; font-size:10px;">X</div>' for _ in range(25)])
    motor_placeholder.markdown(f'<div class="motor-outer"><div class="motor-inner {speed} {chaos}">{balls_html}</div></div>', unsafe_allow_html=True)

update_globe()

if st.button("INICIAR SNIPER 🚀"):
    if len(st.session_state.last_draw) == 15:
        # Definir os 10 jogos conforme o sistema de ranges
        ranges = [(1,25)]*5 + [(2,25)]*2 + [(1,24)]*2 + [(3,25)]*1
        
        st.session_state.sim_results = []
        for r_start, r_end in ranges:
            game = generate_sniper_bet(st.session_state.last_draw, r_start, r_end)
            st.session_state.sim_results.append({"bet": game, "range": f"{r_start:02}-{r_end:02}"})
            
        st.session_state.current_view = [[] for _ in range(10)]
        
        placeholder = st.empty()
        for ball_idx in range(15):
            update_globe("spin-fast", "chaos-active")
            time.sleep(1.5) # Reduzi um pouco para fluidez, ajuste se necessário
            update_globe("spin-slow", "")
            for i in range(10):
                st.session_state.current_view[i].append(st.session_state.sim_results[i]["bet"][ball_idx])
            with placeholder.container():
                for i in range(10):
                    r_text = st.session_state.sim_results[i]["range"]
                    balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(st.session_state.current_view[i])])
                    st.markdown(f'<div class="bet-card"><span class="range-info">RANGE {r_text}</span><b>#{i+1:02}</b> &nbsp; {balls_html}</div>', unsafe_allow_html=True)
            time.sleep(0.5)
        st.balloons()
    else:
        st.error("❌ Erro: Insira o último sorteio primeiro!")

# --- 6. TOOLS & EXIBIÇÃO FINAL ---
if st.session_state.sim_results and len(st.session_state.current_view[0]) == 15:
    st.markdown("---")
    c_clr, c_dl = st.columns(2)
    with c_clr:
        if st.button("🧹 LIMPAR TUDO"):
            st.session_state.sim_results = []
            st.session_state.current_view = []
            st.rerun()
    with c_dl:
        out = "\n".join([" ".join([f"{n:02}" for n in item["bet"]]) for item in st.session_state.sim_results])
        st.download_button("📥 BAIXAR RESULTADOS SNIPER (.TXT)", out, file_name="lotofacil_sniper.txt")

st.markdown('<div style="text-align:center; margin-top:50px; opacity:0.6;"><p>⚠️ PROIBIDO PARA MENORES DE 21 ANOS.</p><p>© 2026 TOTOLOTO PRO - SNIPER EDITION</p></div>', unsafe_allow_html=True)
