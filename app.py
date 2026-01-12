import streamlit as st
import time
import random

# --- 1. CONFIGURAÇÃO E TEMA ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PROFISSIONAL (ESTILO CASINO & 3D) ---
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
        font-size: clamp(1.8rem, 5vw, 3rem);
        font-weight: 700;
        text-align: center;
        color: #ff00ff;
        text-shadow: 0 0 15px #ff00ff;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #d100d1;
        margin-bottom: 30px;
        font-weight: 300;
        letter-spacing: 2px;
    }

    /* Esferas 3D */
    .ball {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 3px;
        font-weight: 700;
        font-size: 15px;
        color: white;
        background: radial-gradient(circle at 10px 10px, #ff55ff, #4b0082);
        box-shadow: inset -3px -3px 6px rgba(0,0,0,0.7), 3px 3px 8px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* O Globo (Motor) */
    .motor-outer {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px auto;
        width: 300px;
        height: 300px;
        border: 6px solid #800080;
        border-radius: 50%;
        position: relative;
        background: rgba(43, 0, 53, 0.4);
        box-shadow: 0 0 40px rgba(255, 0, 255, 0.2), inset 0 0 20px rgba(0,0,0,0.8);
        overflow: hidden;
    }
    .motor-inner {
        width: 100%;
        height: 100%;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding: 40px;
    }
    
    .spin-fast { animation: shuffle 0.4s linear infinite; }
    .spin-slow { animation: shuffle 3s linear infinite; }

    @keyframes shuffle {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.05); }
        100% { transform: rotate(360deg) scale(1); }
    }

    /* Inputs & Botões */
    .stTextInput input {
        background-color: #000 !important;
        color: #ff00ff !important;
        border: 1px solid #ff00ff !important;
        border-radius: 5px !important;
        text-align: center;
        font-size: 20px !important;
    }
    
    .stButton button {
        background: linear-gradient(to right, #4b0082, #ff00ff) !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        transition: 0.3s !important;
    }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255,0,255,0.4); }

    .bet-container {
        background: rgba(20, 20, 20, 0.8);
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        border-left: 5px solid #ff00ff;
    }

    .legal-footer {
        font-size: 0.7rem;
        text-align: center;
        color: #666;
        margin-top: 50px;
        border-top: 1px solid #222;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DO SISTEMA SOBERANO (19 NÚMEROS + 8 FILTROS) ---
def get_matrix_19(draw_list):
    all_n = list(range(1, 26))
    missing = [n for n in all_n if n not in draw_list] # 10 que não saíram
    strong_prev = random.sample(draw_list, 9) # 9 do sorteio anterior (Lógica de peso)
    return sorted(missing + strong_prev)

def sovereign_filter_engine(matrix):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    fib = [1, 2, 3, 5, 8, 13, 21]
    
    while True:
        bet = sorted(random.sample(matrix, 15))
        # 1. Par/Ímpar (7:8 ou 8:7)
        if len([n for n in bet if n % 2 != 0]) not in [7, 8]: continue
        # 2. Primos (5-6)
        if len([n for n in bet if n in primes]) not in [5, 6]: continue
        # 3. Soma (180-210)
        if not (180 <= sum(bet) <= 210): continue
        # 4. Fibonacci (3-5)
        if len([n for n in bet if n in fib]) not in [3, 4, 5]: continue
        # 5. Gaps (Max 7)
        gaps = [bet[i+1] - bet[i] for i in range(len(bet)-1)]
        if any(g > 7 for g in gaps): continue
        
        return bet

# --- 4. ESTADO DA SESSÃO ---
if 'last_draw' not in st.session_state: st.session_state.last_draw = ""
if 'processed' not in st.session_state: st.session_state.processed = False
if 'results' not in st.session_state: st.session_state.results = []

# --- 5. CABEÇALHO ---
st.markdown('<div class="main-title">TOTOLOTO ALGORITMIA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">JOGUE COM INTELIGÊNCIA</div>', unsafe_allow_html=True)

# --- 6. ENTRADA DE DADOS ---
col_in, col_clr = st.columns([5, 1])
with col_in:
    draw_input = st.text_input("Último Sorteio:", value=st.session_state.last_draw, placeholder="01 02 03...", label_visibility="collapsed", key="input_field")
with col_clr:
    if st.button("LIMPAR 🗑️"):
        st.session_state.last_draw = ""
        st.session_state.processed = False
        st.session_state.results = []
        st.rerun()

if draw_input:
    try:
        nums = [int(x) for x in draw_input.split()]
        if len(nums) == 15:
            st.session_state.valid_nums = nums
            balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(nums)])
            st.markdown(f'<div style="text-align:center; margin-top:10px;">{balls_html}</div>', unsafe_allow_html=True)
        else: st.warning("Insira 15 números.")
    except: st.error("Erro no formato.")

# --- 7. FILTRAGEM (MOTOR PEQUENO) ---
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    f_col_left, f_col_right = st.columns([3, 1])
    with f_col_left:
        btn_filter = st.button("EXECUTAR TAREFA DE FILTRAGEM")
    with f_col_right:
        f_motor = st.empty()
    
    if btn_filter:
        if 'valid_nums' in st.session_state:
            for _ in range(15):
                f_motor.markdown('<div style="width:25px; height:25px; border:3px solid #ff00ff; border-top:3px solid transparent; border-radius:50%; animation: shuffle 0.5s linear infinite;"></div>', unsafe_allow_html=True)
                time.sleep(1)
            f_motor.empty()
            st.session_state.matrix = get_matrix_19(st.session_state.valid_nums)
            st.session_state.processed = True
            st.success("✅ Têm sido filtrado com sucesso!")
        else: st.error("Insira o sorteio primeiro.")

# --- 8. SIMULADOR (O GLOBO) ---
st.markdown("---")
motor_area = st.empty()

def update_motor(status="spin-slow"):
    balls_inside = "".join(['<div class="ball" style="opacity:0.3; width:20px; height:20px;">X</div>' for _ in range(25)])
    motor_area.markdown(f'<div class="motor-outer"><div class="motor-inner {status}">{balls_inside}</div></div>', unsafe_allow_html=True)

update_motor()

bet_qty = st.selectbox("Quantidade de Apostas:", [10, 20], index=0)

if st.button("SIMULAR AGORA 🚀"):
    if st.session_state.processed:
        st.session_state.results = []
        final_bets = []
        
        # Simulação progressiva - Bola por bola
        for i in range(bet_qty):
            # Fase rápida: Misturando
            update_motor("spin-fast")
            time.sleep(4.5)
            # Fase lenta: Ejeção
            update_motor("spin-slow")
            time.sleep(2)
            # Gerar aposta do sistema
            new_bet = sovereign_filter_engine(st.session_state.matrix)
            st.session_state.results.append(new_bet)
            st.rerun()
    else: st.error("Execute a filtragem primeiro.")

# --- 9. EXIBIÇÃO DE RESULTADOS ---
if st.session_state.results:
    st.markdown("### 📋 Apostas Geradas")
    txt_output = ""
    for idx, res in enumerate(st.session_state.results):
        res_str = " ".join([f"{n:02}" for n in res])
        txt_output += res_str + "\n"
        
        col_bet, col_cp = st.columns([5, 1])
        with col_bet:
            res_balls = "".join([f'<div class="ball">{n:02}</div>' for n in res])
            st.markdown(f'<div class="bet-container">{res_balls}</div>', unsafe_allow_html=True)
        with col_cp:
            st.write("##")
            st.button("📋", key=f"cp_{idx}")

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: st.download_button("BAIXAR TXT", txt_output, "apostas.txt")
    with c2: st.code(txt_output)
    with c3: 
        if st.button("LIMPAR TUDO"):
            st.session_state.results = []
            st.rerun()

# --- 10. FOOTER LEGAL ---
st.markdown("""
<div class="legal-footer">
    <p>⚠️ PROIBIDO PARA MENORES DE 21 ANOS.</p>
    <p>Este aplicativo é uma ferramenta estatística e educativa. Não garante lucros. Jogue com responsabilidade.</p>
    <p>TOTOLOTO ALGORITMIA © 2026</p>
</div>
""", unsafe_allow_html=True)
