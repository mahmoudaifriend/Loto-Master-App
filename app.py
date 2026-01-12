import streamlit as st
import time
import random
import requests
from collections import Counter

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PROFISSIONAL (ESTILO CASINO & ANIMAÇÃO DE CAOS REAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');
    
    .stApp { background: radial-gradient(circle at top, #1a0022 0%, #000000 100%); color: #ffffff; font-family: 'Roboto', sans-serif; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; text-align: center; color: #ff00ff; text-shadow: 0 0 15px #ff00ff; margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 0.9rem; color: #d100d1; margin-bottom: 30px; letter-spacing: 2px; }
    
    .ball { width: 38px; height: 38px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin: 2px; font-weight: 700; font-size: 14px; color: white; background: radial-gradient(circle at 10px 10px, #ff55ff, #4b0082); border: 1px solid rgba(255,255,255,0.2); position: relative; transition: all 0.3s ease; }
    
    /* O GLOBO ÚNICO */
    .motor-outer { display: flex; justify(content): center; align-items: center; margin: 20px auto; width: 280px; height: 280px; border: 5px solid #800080; border-radius: 50%; background: rgba(43, 0, 53, 0.4); box-shadow: 0 0 40px #ff00ff44; overflow: hidden; position: relative; }
    .motor-inner { width: 100%; height: 100%; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; padding: 30px; position: relative; }
    
    /* ANIMAÇÃO DE CAOS REAL (MOVIMENTO RANDÔMICO) */
    @keyframes chaos {
        0% { transform: translate(0, 0) rotate(0deg); }
        25% { transform: translate(-15px, 10px) rotate(90deg); }
        50% { transform: translate(15px, -15px) rotate(180deg); }
        75% { transform: translate(-10px, -20px) rotate(270deg); }
        100% { transform: translate(0, 0) rotate(360deg); }
    }

    .chaos-active .ball { animation: chaos 0.4s infinite linear; }
    /* Diversificação do movimento para cada bola */
    .chaos-active .ball:nth-child(2n) { animation-duration: 0.3s; animation-direction: reverse; }
    .chaos-active .ball:nth-child(3n) { animation-duration: 0.5s; }
    
    .spin-fast { animation: shuffle 0.4s linear infinite; }
    .spin-slow { animation: shuffle 4s linear infinite; }
    @keyframes shuffle { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    
    .bet-card { background: rgba(20, 20, 20, 0.9); border: 1px solid #4b0082; border-radius: 10px; padding: 10px; margin-bottom: 10px; display: flex; flex-wrap: wrap; align-items: center; }

    /* APOSTA DE OURO STYLE */
    .gold-card { background: linear-gradient(145deg, #2b0035, #1a0022); border: 3px solid #FFD700 !important; box-shadow: 0 0 25px rgba(255, 215, 0, 0.4); position: relative; }
    .gold-text { color: #FFD700; font-weight: bold; font-family: 'Orbitron', sans-serif; text-align: center; margin-bottom: 5px; font-style: italic; font-size: 1.1rem; }

    div.stButton > button { background: linear-gradient(to right, #4b0082, #ff00ff) !important; color: white !important; font-weight: bold !important; width: 100%; border: none; border-radius: 5px; }
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
    except:
        return [random.sample(range(1, 26), 15) for _ in range(10)]

def get_sovereign_matrix_19(draws):
    flat_list = [n for sub in draws for n in sub]
    freq = Counter(flat_list)
    most_common = [item[0] for item in freq.most_common(19)]
    return sorted(most_common)

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

# --- 4. SESSION STATE INIT ---
if 'matrix' not in st.session_state: st.session_state.matrix = []
if 'sim_results' not in st.session_state: st.session_state.sim_results = []
if 'current_view' not in st.session_state: st.session_state.current_view = []
if 'show_golden' not in st.session_state: st.session_state.show_golden = True

# --- 5. INTERFACE PRINCIPAL ---
st.markdown('<div class="main-title">TOTOLOTO ALGORITMIA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">JOGUE COM INTELIGÊNCIA</div>', unsafe_allow_html=True)

if st.button("🔄 SINCRONIZAR ÚLTIMOS 10 SORTEIOS"):
    with st.spinner("Conectando aos servidores..."):
        history = fetch_last_10_draws()
        st.session_state.matrix = get_sovereign_matrix_19(history)
        st.success("✅ OPERAÇÃO CONCLUÍDA: Matriz 19 Gerada!")

st.markdown("---")

# MOTOR ÚNICO USANDO PLACEHOLDER
motor_placeholder = st.empty()

def update_globe(speed_class="spin-slow", chaos_class=""):
    balls_html = "".join([f'<div class="ball" style="opacity:0.4; width:18px; height:18px;">X</div>' for _ in range(25)])
    motor_placeholder.markdown(f"""
        <div class="motor-outer">
            <div class="motor-inner {speed_class} {chaos_class}">
                {balls_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

# Inicia o motor em estado lento
update_globe()

qty = st.selectbox("Quantidade de Apostas:", [10, 20])
sim_btn = st.button("INICIAR VALENDO 🚀")

results_placeholder = st.empty()

if sim_btn:
    if st.session_state.matrix:
        st.session_state.show_golden = True
        st.session_state.sim_results = [generate_sovereign_bet(st.session_state.matrix) for _ in range(qty)]
        st.session_state.current_view = [[] for _ in range(qty)]
        
        for ball_idx in range(15):
            # FASE VALENDO (4.5s Fast + Chaos)
            update_globe("spin-fast", "chaos-active")
            time.sleep(4.5)
            
            # FASE DE CALMA (2s Slow)
            update_globe("spin-slow", "")
            for i in range(qty):
                st.session_state.current_view[i].append(st.session_state.sim_results[i][ball_idx])
            
            with results_placeholder.container():
                for i in range(qty):
                    balls_res = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(st.session_state.current_view[i])])
                    st.markdown(f'<div class="bet-card"><b>#{i+1:02}</b> &nbsp; {balls_res}</div>', unsafe_allow_html=True)
            time.sleep(2)
        st.balloons()
    else: st.error("ERRO: Sincronize primeiro!")

# --- 6. APOSTA DE OURO & FERRAMENTAS ---
if st.session_state.sim_results and st.session_state.show_golden:
    st.markdown("---")
    
    # Lógica da Aposta de Ouro (Filtro Interno)
    golden_bet = min(st.session_state.sim_results, key=lambda x: abs(sum(x) - 195))
    golden_balls_html = "".join([f'<div class="ball" style="border: 2px solid #FFD700;">{n:02}</div>' for n in sorted(golden_bet)])
    
    st.markdown(f'<div class="gold-text">Aposta de Ouro: Que a sorte nos proteja dos números!</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="bet-card gold-card">
            <div style="width:100%; text-align:center;">{golden_balls_html}</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_copy_gold, col_del_gold = st.columns(2)
    with col_copy_gold: 
        if st.button("📋 COPIAR OURO"): st.toast("Copiado!")
    with col_del_gold: 
        if st.button("🗑️ REMOVER OURO"):
            st.session_state.show_golden = False
            st.rerun()

if st.session_state.sim_results:
    st.markdown("---")
    col_y, col_n = st.columns(2)
    with col_y:
        st.markdown('<div style="background: linear-gradient(to right, #800080, #ff00ff); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #ff00ff; font-weight: bold;">✅ Sim, confirmo</div>', unsafe_allow_html=True)
        st.button("CONFIRMAR TUDO", key="cy")
    with col_n:
        st.markdown('<div style="background: linear-gradient(to right, #2b0035, #4b0082); padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #800080; font-weight: bold;">❌ Não, não confirmo</div>', unsafe_allow_html=True)
        if st.button("CANCELAR", key="cn"):
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

st.markdown('<div class="legal-footer"><p>⚠️ PROIBIDO PARA MENORES DE 21 ANOS.</p><p>© 2026 TOTOLOTO ALGORITMIA</p></div>', unsafe_allow_html=True)
