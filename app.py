import streamlit as st
import time
import random
import requests
from collections import Counter

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PROFISSIONAL (ZOUQ TBI3 COMPLETO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');
    
    .stApp { background: radial-gradient(circle at top, #1a0022 0%, #000000 100%); color: #ffffff; font-family: 'Roboto', sans-serif; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 3rem; text-align: center; color: #fff; text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 40px #ff00ff; margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 0.9rem; color: #d100d1; margin-bottom: 30px; letter-spacing: 2px; font-weight: bold; text-shadow: 0 0 5px #d100d1; }
    
    /* BOLAS 3D REALISTAS */
    .ball { 
        width: 38px; height: 38px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin: 3px; 
        font-weight: 800; font-size: 14px; color: white; 
        background: radial-gradient(circle at 35% 35%, #ffb3ff, #ff00ff 45%, #4b0082 90%);
        box-shadow: inset -4px -4px 10px rgba(0,0,0,0.8), inset 3px 3px 6px rgba(255,255,255,0.4), 0 5px 15px rgba(0,0,0,0.5);
        position: relative; transition: transform 0.2s ease;
    }
    
    /* GLOBO ÚNICO PREMIUM (GLASSMORPHISM) */
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
    
    /* CARDS EM GLASSMORPHISM PURO */
    .bet-card { background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(15px); border: 1px solid rgba(255,0,255,0.2); border-radius: 15px; padding: 12px; margin-bottom: 12px; display: flex; flex-wrap: wrap; align-items: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }

    /* APOSTA DE OURO COM PULSO NEON DOURADO */
    @keyframes goldPulse { 0% { box-shadow: 0 0 10px #FFD700; } 50% { box-shadow: 0 0 30px #FFD700, inset 0 0 10px #FFD700; } 100% { box-shadow: 0 0 10px #FFD700; } }
    .gold-card { background: linear-gradient(145deg, #2b0035, #1a0022); border: 3px solid #FFD700 !important; animation: goldPulse 2s infinite; }
    .gold-text { color: #FFD700; font-weight: bold; font-family: 'Orbitron', sans-serif; text-align: center; margin-bottom: 10px; font-style: italic; font-size: 1.2rem; text-shadow: 0 0 8px #FFD700; }

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

# --- 3. LÓGICA DO SISTEMA ---
def fetch_last_10_draws():
    all_draws = []
    try:
        res = requests.get("https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil", timeout=5)
        latest_num = int(res.json()['numero'])
        for i in range(10):
            url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil/{latest_num - i}"
            draw_res = requests.get(url, timeout=5)
            if draw_res.status_code == 200:
                all_draws.append([int(n) for n in draw_res.json()['dezenas']])
        return all_draws
    except: return [random.sample(range(1, 26), 15) for _ in range(10)]

def get_sovereign_matrix_19(draws):
    flat_list = [n for sub in draws for n in sub]
    freq = Counter(flat_list)
    return sorted([item[0] for item in freq.most_common(19)])

def generate_sovereign_bet(matrix):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    while True:
        bet = sorted(random.sample(matrix, 15))
        if len([n for n in bet if n % 2 != 0]) not in [7, 8]: continue
        if len([n for n in bet if n in primes]) not in [5, 6]: continue
        if not (180 <= sum(bet) <= 210): continue
        return bet

# --- 4. SESSION STATE (PERSISTÊNCIA) ---
if 'matrix' not in st.session_state: st.session_state.matrix = []
if 'sim_results' not in st.session_state: st.session_state.sim_results = []
if 'current_view' not in st.session_state: st.session_state.current_view = []
if 'show_golden' not in st.session_state: st.session_state.show_golden = True

# --- 5. INTERFACE ---
st.markdown('<div class="main-title">💎 TOTOLOTO PRO 💎</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SISTEMA ALGORÍTMICO SOBERANO</div>', unsafe_allow_html=True)

if st.button("🔄 SINCRONIZAR ÚLTIMOS 10 SORTEIOS"):
    with st.spinner("Sincronizando..."):
        history = fetch_last_10_draws()
        st.session_state.matrix = get_sovereign_matrix_19(history)
        st.success("✅ OPERAÇÃO CONCLUÍDA: Matriz 19 Gerada!")

st.markdown("---")
motor_placeholder = st.empty()

def update_globe(speed="spin-slow", chaos=""):
    balls_html = "".join([f'<div class="ball" style="opacity:0.4; width:18px; height:18px; font-size:10px;">X</div>' for _ in range(25)])
    motor_placeholder.markdown(f'<div class="motor-outer"><div class="motor-inner {speed} {chaos}">{balls_html}</div></div>', unsafe_allow_html=True)

update_globe()

qty = st.selectbox("Quantidade de Apostas:", [10, 20])
if st.button("INICIAR VALENDO 🚀"):
    if st.session_state.matrix:
        st.session_state.show_golden = True
        st.session_state.sim_results = [generate_sovereign_bet(st.session_state.matrix) for _ in range(qty)]
        st.session_state.current_view = [[] for _ in range(qty)]
        
        placeholder = st.empty()
        for ball_idx in range(15):
            update_globe("spin-fast", "chaos-active")
            time.sleep(4.5)
            update_globe("spin-slow", "")
            for i in range(qty):
                st.session_state.current_view[i].append(st.session_state.sim_results[i][ball_idx])
            with placeholder.container():
                for i in range(qty):
                    balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(st.session_state.current_view[i])])
                    st.markdown(f'<div class="bet-card"><b>#{i+1:02}</b> &nbsp; {balls_html}</div>', unsafe_allow_html=True)
            time.sleep(2)
        st.balloons()
    else: st.error("Sincronize primeiro!")

# --- 6. APOSTA DE OURO & TOOLS ---
if st.session_state.sim_results:
    res_show = st.container()
    with res_show:
        for i, bet in enumerate(st.session_state.sim_results):
            if not st.session_state.current_view or len(st.session_state.current_view[i]) < 15:
                balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(bet)])
                st.markdown(f'<div class="bet-card"><b>#{i+1:02}</b> &nbsp; {balls_html}</div>', unsafe_allow_html=True)

    if st.session_state.show_golden:
        st.markdown("---")
        # LOCALIZAÇÃO DO RATING DE OURO
        golden_bet = min(st.session_state.sim_results, key=lambda x: abs(sum(x) - 195))
        # BUSCA DO NÚMERO ORIGINAL NA LISTA
        original_index = st.session_state.sim_results.index(golden_bet) + 1
        
        golden_balls = "".join([f'<div class="ball" style="border: 2px solid #FFD700; box-shadow: 0 0 10px #FFD700;">{n:02}</div>' for n in sorted(golden_bet)])
        
        # EXIBIÇÃO DO NÚMERO ORIGINAL NO TÍTULO
        st.markdown(f'<div class="gold-text">👑 Aposta de Ouro (Original #{original_index:02}): Que a sorte nos proteja!</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bet-card gold-card"><div style="width:100%; text-align:center;">{golden_balls}</div></div>', unsafe_allow_html=True)
        
        c_copy, c_rem = st.columns(2)
        with c_copy:
            if st.button("📋 COPIAR OURO"):
                st.toast(f"Aposta de Ouro #{original_index:02} Copiada!")
        with c_rem:
            if st.button("🗑️ REMOVER OURO"):
                st.session_state.show_golden = False
                st.rerun()

    st.markdown("---")
    col_y, col_n = st.columns(2)
    with col_y:
        st.markdown('<div style="background: linear-gradient(to right, #800080, #ff00ff); padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; border: 1px solid #ff00ff;">✅ Sim, confirmo</div>', unsafe_allow_html=True)
        st.button("CONFIRMAR TUDO", key="c_all")
    with col_n:
        st.markdown('<div style="background: linear-gradient(to right, #2b0035, #4b0082); padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; border: 1px solid #800080;">❌ Não, não confirmo</div>', unsafe_allow_html=True)
        if st.button("CANCELAR TUDO", key="can_all"):
            st.session_state.sim_results = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    c_clr, c_dl = st.columns(2)
    with c_clr:
        if st.button("🧹 LIMPAR TUDO"):
            st.session_state.clear()
            st.rerun()
    with c_dl:
        out = "\n".join([" ".join([f"{n:02}" for n in b]) for b in st.session_state.sim_results])
        st.download_button("📥 BAIXAR RESULTADOS (.TXT)", out, file_name="lotofacil_soberana.txt")

st.markdown('<div class="legal-footer"><p>⚠️ PROIBIDO PARA MENORES DE 21 ANOS.</p><p>© 2026 TOTOLOTO PRO</p></div>', unsafe_allow_html=True)
