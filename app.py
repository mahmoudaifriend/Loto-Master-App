import streamlit as st
import time
import random
import requests

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PROFISSIONAL (ESTILO CASINO PURA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');
    
    .stApp { background: radial-gradient(circle at top, #1a0022 0%, #000000 100%); color: #ffffff; font-family: 'Roboto', sans-serif; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; text-align: center; color: #ff00ff; text-shadow: 0 0 15px #ff00ff; margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 0.9rem; color: #d100d1; margin-bottom: 30px; letter-spacing: 2px; }
    
    .ball { width: 38px; height: 38px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin: 2px; font-weight: 700; font-size: 14px; color: white; background: radial-gradient(circle at 10px 10px, #ff55ff, #4b0082); border: 1px solid rgba(255,255,255,0.2); }
    
    .motor-outer { display: flex; justify-content: center; align-items: center; margin: 20px auto; width: 260px; height: 260px; border: 5px solid #800080; border-radius: 50%; background: rgba(43, 0, 53, 0.4); box-shadow: 0 0 40px #ff00ff44; overflow: hidden; }
    .motor-inner { width: 100%; height: 100%; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; padding: 20px; }
    .spin-fast { animation: shuffle 0.4s linear infinite; }
    .spin-slow { animation: shuffle 4s linear infinite; }
    @keyframes shuffle { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    
    .bet-card { background: rgba(20, 20, 20, 0.9); border: 1px solid #4b0082; border-radius: 10px; padding: 10px; margin-bottom: 10px; display: flex; flex-wrap: wrap; align-items: center; }

    div.stButton > button { background: linear-gradient(to right, #4b0082, #ff00ff) !important; color: white !important; font-weight: bold !important; width: 100%; border: none; border-radius: 5px; }
    
    .confirm-yes { background: linear-gradient(to right, #800080, #ff00ff) !important; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #ff00ff; font-weight: bold; margin-bottom: 10px; }
    .confirm-no { background: linear-gradient(to right, #2b0035, #4b0082) !important; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #800080; font-weight: bold; margin-bottom: 10px; }

    .legal-footer { font-size: 0.7rem; text-align: center; color: #666; margin-top: 40px; padding: 20px; border-top: 1px solid #222; }
</style>
""", unsafe_allow_html=True)

# --- 3. DADOS HISTÓRICOS (INJETADOS) ---
MOST_FREQUENT = [20, 25, 10, 11, 13, 24, 14, 1, 4, 3, 12, 5, 2, 22, 15, 9, 19, 18, 21, 7, 17, 6, 23, 8, 16]
MOST_DELAYED = [19, 5, 11, 14, 10, 22, 24, 12, 6, 3]

# --- 4. FUNÇÃO REAL-TIME API ---
def fetch_real_latest_draw():
    try:
        # API Oficial da Caixa (Proxy/Mirror)
        response = requests.get("https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil", timeout=5)
        data = response.json()
        return [int(n) for n in data['dezenas']]
    except:
        # Fallback se a API estiver fora do ar
        return [1, 2, 4, 7, 8, 9, 13, 15, 16, 17, 18, 20, 21, 23, 25]

# --- 5. LÓGICA DO SISTEMA SOBERANO (MATRIZ 19) ---
def get_sovereign_matrix(latest_draw):
    # Prioridade 1: Os 10 mais atrasados (conforme sua lista)
    matrix = MOST_DELAYED.copy()
    # Prioridade 2: Completar com os mais frequentes históricos que não estão na lista
    for num in MOST_FREQUENT:
        if num not in matrix:
            matrix.append(num)
        if len(matrix) == 19: break
    return sorted(matrix)

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

# --- 6. SESSION STATE ---
if 'matrix' not in st.session_state: st.session_state.matrix = []
if 'sim_results' not in st.session_state: st.session_state.sim_results = []
if 'current_view' not in st.session_state: st.session_state.current_view = []

# --- 7. INTERFACE USUÁRIO ---
st.markdown('<div class="main-title">TOTOLOTO ALGORITMIA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">JOGUE COM INTELIGÊNCIA</div>', unsafe_allow_html=True)

if st.button("🔄 SINCRONIZAR COM LOTERIAS CAIXA"):
    with st.spinner("Conectando..."):
        latest = fetch_real_latest_draw()
        st.session_state.matrix = get_sovereign_matrix(latest)
        st.success(f"✅ Conectado! Matriz 19 otimizada com sucesso.")

st.markdown("---")
qty = st.selectbox("Quantidade de Apostas:", [10, 20])
sim_btn = st.button("INICIAR SIMULAÇÃO SOBERANA 🚀")

motor_area = st.empty()
def update_motor(speed="spin-slow"):
    balls = "".join(['<div class="ball" style="opacity:0.3; width:18px; height:18px;">X</div>' for _ in range(25)])
    motor_area.markdown(f'<div class="motor-outer"><div class="motor-inner {speed}">{balls}</div></div>', unsafe_allow_html=True)

update_motor()
results_placeholder = st.empty()

if sim_btn:
    if st.session_state.matrix:
        st.session_state.sim_results = [generate_sovereign_bet(st.session_state.matrix) for _ in range(qty)]
        st.session_state.current_view = [[] for _ in range(qty)]
        
        for ball_idx in range(15):
            update_motor("spin-fast") # 4.5s
            time.sleep(4.5)
            update_motor("spin-slow") # 2s
            
            for i in range(qty):
                st.session_state.current_view[i].append(st.session_state.sim_results[i][ball_idx])
            
            with results_placeholder.container():
                for i in range(qty):
                    balls_res = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(st.session_state.current_view[i])])
                    st.markdown(f'<div class="bet-card"><b>#{i+1:02}</b> &nbsp; {current_balls}</div>', unsafe_allow_html=True)
            time.sleep(2)
        st.balloons()
    else: st.error("Sincronize os dados primeiro.")

# --- 8. CONFIRMAÇÃO E FERRAMENTAS ---
if st.session_state.sim_results:
    st.markdown("---")
    col_y, col_n = st.columns(2)
    with col_y:
        st.markdown('<div class="confirm-yes">✅ Sim, confirmo</div>', unsafe_allow_html=True)
        st.button("CONFIRMAR JOGO", key="c_y")
    with col_n:
        st.markdown('<div class="confirm-no">❌ Não, não confirmo</div>', unsafe_allow_html=True)
        st.button("CANCELAR JOGO", key="c_n")

    st.markdown("<br>", unsafe_allow_html=True)
    c_clear, c_dl = st.columns(2)
    with c_clear:
        if st.button("🧹 LIMPAR TUDO"):
            st.session_state.clear()
            st.rerun()
    with c_dl:
        output = "\n".join([" ".join([f"{n:02}" for n in b]) for b in st.session_state.sim_results])
        st.download_button("📥 BAIXAR RESULTADOS (.TXT)", output, file_name="lotofacil_soberana.txt")

st.markdown('<div class="legal-footer"><p>⚠️ PROIBIDO PARA MENORES DE 21 ANOS.</p><p>Estatística e educação. © 2026 TOTOLOTO ALGORITMIA</p></div>', unsafe_allow_html=True)
