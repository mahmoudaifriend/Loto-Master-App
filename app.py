import streamlit as st
import time
import random
import itertools
import pandas as pd
from io import BytesIO

# --- CONFIGURATION ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA", layout="wide", initial_sidebar_state="collapsed")

# --- CUSTOM CSS (Casinos Style & 3D Spheres) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;500&display=swap');

    /* Global Background */
    .stApp {
        background: radial-gradient(circle at top, #2b0035 0%, #100012 100%);
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }

    /* Titles */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #ff00ff, #800080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #d100d1;
        margin-bottom: 20px;
        font-style: italic;
    }

    /* 3D Sphere Style */
    .ball {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 5px;
        font-weight: bold;
        font-size: 18px;
        color: white;
        background: radial-gradient(circle at 15px 15px, #ff44ff, #4b0082);
        box-shadow: inset -5px -5px 10px rgba(0,0,0,0.5), 5px 5px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .ball-white {
        background: radial-gradient(circle at 15px 15px, #ffffff, #888888);
        color: #4b0082;
    }

    /* Input & Containers */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.05);
        color: #ff00ff;
        border: 2px solid #800080;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
    }

    /* Simulation Motor UI */
    .motor-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 300px;
        margin: 30px 0;
    }
    .motor-circle {
        width: 250px;
        height: 250px;
        border: 10px dashed #ff00ff;
        border-radius: 50%;
        display: flex;
        flex-wrap: wrap;
        padding: 20px;
        justify-content: center;
        align-items: center;
        animation: spin 10s linear infinite;
    }
    .motor-circle.fast { animation: spin 0.5s linear infinite; }
    .motor-circle.slow { animation: spin 3s linear infinite; }

    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #800080 0%, #ff00ff 100%);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0px 4px 15px rgba(255, 0, 255, 0.3);
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 20px rgba(255, 0, 255, 0.5);
    }

    /* Bet Cards */
    .bet-card {
        background: rgba(43, 0, 53, 0.8);
        border: 1px solid #ff00ff;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
    }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #777;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- ALGORITHM ENGINE ---
def sovereign_filter(matrix_19):
    # Sovereign Filters Constants
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    FIBONACCI = [1, 2, 3, 5, 8, 13, 21]
    
    bets = []
    # Generation logic limited for performance in UI
    while len(bets) < 200:
        combo = sorted(random.sample(matrix_19, 15))
        
        # Gates: 
        # 1. Odd/Even (7:8 or 8:7)
        odds = [n for n in combo if n % 2 != 0]
        if len(odds) not in [7, 8]: continue
        
        # 2. Primes (5 or 6)
        primes_count = len([n for n in combo if n in PRIMES])
        if primes_count not in [5, 6]: continue
        
        # 3. Sum (180 - 210)
        if not (180 <= sum(combo) <= 210): continue
        
        # 4. Fibonacci (3 - 5)
        fib_count = len([n for n in combo if n in FIBONACCI])
        if fib_count not in [3, 4, 5]: continue

        if combo not in bets:
            bets.append(combo)
            
    return bets

# --- UI HEADER ---
st.markdown('<h1 class="main-title">TOTOLOTO ALGORITMIA</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Jogue com inteligência</p>', unsafe_allow_html=True)

# Logo placeholder (Casino style emoji/text)
st.markdown("<div style='text-align: center; font-size: 50px;'>🎰 💎 🎰</div>", unsafe_allow_html=True)

# --- INPUT SECTION ---
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        last_draw_input = st.text_input("Último Sorteio (Insira 15 números separados por espaço):", key="draw_in", placeholder="Ex: 01 02 04 07...")
    with col2:
        st.write("##")
        if st.button("Limpar 🗑️"):
            st.session_state.draw_in = ""
            st.rerun()

    if last_draw_input:
        try:
            nums = [int(x) for x in last_draw_input.split()]
            if len(nums) == 15:
                ball_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(nums)])
                st.markdown(f'<div style="text-align: center; margin-top: 10px;">{ball_html}</div>', unsafe_allow_html=True)
                st.session_state.valid_draw = nums
            else:
                st.warning("Por favor, insira exatamente 15 números.")
        except:
            st.error("Formato inválido.")

st.markdown("---")

# --- FILTERING SECTION ---
st.markdown("<h3 style='text-align: center;'>TELA DE FILTRAGEM (19 NÚMEROS)</h3>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns([1, 2, 1])

with col_b:
    if st.button("EXECUTAR FILTRAGEM SOVIÉTICA"):
        if 'valid_draw' in st.session_state:
            with st.spinner("Motor de filtragem em movimento..."):
                # Simulation of 15s Motor
                motor_placeholder = st.empty()
                for i in range(15):
                    motor_placeholder.markdown(f'<div class="motor-container"><div class="motor-circle fast"><div style="color:#ff00ff; font-weight:bold; transform:rotate(-{i*24}deg)">ALGO</div></div></div>', unsafe_allow_html=True)
                    time.sleep(1)
                
                # Logic to build Matrix 19
                all_nums = list(range(1, 26))
                out_nums = [n for n in all_nums if n not in st.session_state.valid_draw] # 10 missing
                # Take 9 strongest from last draw (simulated logic)
                strong_last = random.sample(st.session_state.valid_draw, 9)
                st.session_state.matrix_19 = sorted(out_nums + strong_last)
                
                st.session_state.processed_bets = sovereign_filter(st.session_state.matrix_19)
                st.success("✅ Têm sido filtrado com sucesso!")
        else:
            st.error("Insira o último sorteio primeiro.")

st.markdown("---")

# --- SIMULATION SECTION ---
st.markdown("<h3 style='text-align: center;'>MOTOR DE SIMULAÇÃO</h3>", unsafe_allow_html=True)

# Visual Motor (Idle)
motor_ui = st.empty()
motor_ui.markdown('<div class="motor-container"><div class="motor-circle"><div class="ball ball-white">X</div>' * 5 + '</div></div>', unsafe_allow_html=True)

# Bet Selector
num_bets = st.selectbox("Quantidade de Apostas para Simular:", [10, 20, 30, 40, 50, 100, 200])

if st.button("INICIAR SIMULAÇÃO 🚀"):
    if 'processed_bets' in st.session_state:
        results_area = st.empty()
        final_bets = random.sample(st.session_state.processed_bets, min(num_bets, len(st.session_state.processed_bets)))
        
        # Animation Logic
        for idx, bet in enumerate(final_bets):
            # Fast Spin
            motor_ui.markdown('<div class="motor-container"><div class="motor-circle fast"></div></div>', unsafe_allow_html=True)
            time.sleep(4.5)
            # Slow Spin + Pop Out
            motor_ui.markdown('<div class="motor-container"><div class="motor-circle slow"></div></div>', unsafe_allow_html=True)
            time.sleep(2)
            
            # Show bet
            st.session_state[f'res_{idx}'] = bet
            
        st.balloons()
    else:
        st.error("Execute a filtragem antes da simulação.")

# --- DISPLAY RESULTS ---
if 'processed_bets' in st.session_state:
    st.markdown("### 📋 Resultados Gerados")
    all_text = ""
    
    for i in range(num_bets):
        if f'res_{i}' in st.session_state:
            bet = st.session_state[f'res_{i}']
            bet_str = " ".join([f"{n:02}" for n in bet])
            all_text += bet_str + "\n"
            
            with st.container():
                c1, c2 = st.columns([5, 1])
                with c1:
                    balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in bet])
                    st.markdown(f'<div class="bet-card">{balls_html}</div>', unsafe_allow_html=True)
                with c2:
                    st.write("##")
                    st.button("Copiar", key=f"btn_{i}", on_click=lambda s=bet_str: st.write(f"Copiado: {s}"))

    st.markdown("---")
    # Bulk Actions
    down_col1, down_col2, down_col3 = st.columns(3)
    with down_col1:
        st.download_button("Baixar TXT 📥", all_text, file_name="apostas_algormitia.txt")
    with down_col2:
        if st.button("Copiar Todos 📋"):
            st.code(all_text)
    with down_col3:
        if st.button("Reiniciar Painel 🔄"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        <p>⚠️ AVISO: USO PROIBIDO PARA MENORES DE 21 ANOS.</p>
        <p>Este aplicativo é uma ferramenta estatística e educacional. Não garante ganhos ou lucros.</p>
        <p>JOGUE COM RESPONSABILIDADE. © 2026 TOTOLOTO ALGORITMIA</p>
    </div>
""", unsafe_allow_html=True)
