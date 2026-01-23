import streamlit as st
import time
import random
import requests
from collections import Counter

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PROFISSIONAL (ZOUQ TBI3 - ESTRUTURA PRESERVADA) ---
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
    }
    
    /* GLOBO PREMIUM */
    .motor-outer { display: flex; justify-content: center; align-items: center; margin: 25px auto; width: 280px; height: 280px; border: 4px solid #ff00ff; border-radius: 50%; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(8px); box-shadow: 0 0 50px rgba(255, 0, 255, 0.3); overflow: hidden; position: relative; }
    .motor-inner { width: 100%; height: 100%; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; padding: 35px; }
    
    @keyframes chaos3d {
        0% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(15px, -15px) rotate(180deg); }
        100% { transform: translate(0, 0) rotate(360deg); }
    }
    .chaos-active .ball { animation: chaos3d 0.3s infinite linear; }
    .spin-fast { animation: shuffle 0.4s linear infinite; }
    @keyframes shuffle { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    
    /* CARDS & GRID */
    .bet-card { background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(15px); border: 1px solid rgba(255,0,255,0.2); border-radius: 15px; padding: 12px; margin-bottom: 12px; display: flex; flex-wrap: wrap; align-items: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .gold-card { border: 3px solid #FFD700 !important; box-shadow: 0 0 20px #FFD700 !important; }
    
    /* ESTILO DO GRID DE SELEÇÃO */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; max-width: 400px; margin: 0 auto; padding: 20px; background: rgba(255,255,255,0.03); border-radius: 15px; border: 1px solid #4b0082; }
    
    div.stButton > button { background: linear-gradient(45deg, #4b0082, #ff00ff) !important; color: white !important; font-weight: bold !important; border-radius: 10px; border: none; transition: 0.3s; width: 100%; }
</style>
""", unsafe_allow_html=True)

# --- 3. NOVA LOGÍSTICA: ALGORITMO DE BLOCOS ---
def attack_blocks_engine(fixed_backbone, qty=10):
    # Blocos de Afinidade (Pairs and Triplets)
    triplets = [[7, 8, 9], [16, 17, 19], [4, 5, 6], [21, 22, 23]]
    pairs = [[13, 15], [10, 12], [23, 24], [3, 5], [17, 18]]
    
    all_bets = []
    attempts = 0
    
    while len(all_bets) < qty and attempts < 5000:
        attempts += 1
        # Iniciar com o هيكل (backbone) definido pelo usuário
        current_bet = set(fixed_backbone)
        
        # 1. Injeção de Blocos (Simulando o comportamento da máquina)
        random.shuffle(triplets)
        random.shuffle(pairs)
        
        # Tentar injetar pelo menos uma tripla
        for tri in triplets:
            if len(current_bet) + 3 <= 15:
                current_bet.update(tri)
                break
        
        # Tentar injetar duplas
        for pr in pairs:
            if len(current_bet) + 2 <= 15:
                current_bet.update(pr)
        
        # 2. Preencher lacunas até 15 números (Nível de Caos)
        while len(current_bet) < 15:
            current_bet.add(random.randint(1, 25))
            
        final_list = sorted(list(current_bet))
        
        # --- FILTROS DE QUALIDADE (SÉRVIA) ---
        # Filtro de Sequência (Máximo 4)
        seq_ok = True
        count = 1
        for i in range(len(final_list)-1):
            if final_list[i+1] == final_list[i] + 1:
                count += 1
                if count > 4: seq_ok = False; break
            else: count = 1
        
        # Filtro de Paridade (7 ou 8 ímpares)
        odds = len([n for n in final_list if n % 2 != 0])
        
        if seq_ok and odds in [7, 8]:
            if final_list not in all_bets:
                all_bets.append(final_list)
                
    return all_bets

# --- 4. INTERFACE & GRID DE SELEÇÃO (THE SNIPER GRID) ---
st.markdown('<div class="main-title">💎 TOTOLOTO PRO 💎</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SISTEMA ALGORÍTMICO DE BLOCOS</div>', unsafe_allow_html=True)

# Container do Grid de Seleção
st.markdown('<p style="text-align:center; color:#ff00ff; font-weight:bold;">CONFIGURAÇÃO DO SEU "HAYKAL" (1-25):</p>', unsafe_allow_html=True)
cols = st.columns(5)
selected_nums = []

# Gerar Grid de Checkboxes para o usuário definir o esqueleto
for i in range(1, 26):
    with cols[(i-1)%5]:
        if st.checkbox(f"{i:02}", key=f"n_{i}"):
            selected_nums.append(i)

st.markdown("---")

# Visualização do Motor
motor_placeholder = st.empty()
def update_globe(speed="spin-slow", chaos=""):
    balls_html = "".join([f'<div class="ball" style="opacity:0.3; width:15px; height:15px;"></div>' for _ in range(20)])
    motor_placeholder.markdown(f'<div class="motor-outer"><div class="motor-inner {speed} {chaos}">{balls_html}</div></div>', unsafe_allow_html=True)

update_globe()

# --- 5. EXECUÇÃO ---
qty = st.sidebar.selectbox("Quantidade de Apostas:", [10, 20, 50, 100], index=0)

if st.button("INICIAR PROCESSO DE EXTRAÇÃO 🚀"):
    if not selected_nums:
        st.warning("⚠️ Selecione pelo menos um número no Grid para servir de base!")
    else:
        with st.spinner("O Algoritmo está calculando os blocos de afinidade..."):
            st.session_state.results = attack_blocks_engine(selected_nums, qty)
            
            # Animação de Sorteio Realista
            update_globe("spin-fast", "chaos-active")
            time.sleep(3)
            update_globe("spin-slow", "")
            
            # Exibição dos resultados
            for i, bet in enumerate(st.session_state.results):
                balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in bet])
                st.markdown(f'<div class="bet-card"><b>#{i+1:02}</b> &nbsp; {balls_html}</div>', unsafe_allow_html=True)
            
            st.balloons()

# --- 6. FERRAMENTAS DE EXPORTAÇÃO (PRESERVADAS) ---
if 'results' in st.session_state and st.session_state.results:
    st.markdown("---")
    
    # Aposta de Ouro (Cálculo de Soma Ideal ~195)
    golden_bet = min(st.session_state.results, key=lambda x: abs(sum(x) - 195))
    golden_html = "".join([f'<div class="ball" style="border:2px solid #FFD700;">{n:02}</div>' for n in golden_bet])
    
    st.markdown('<div style="color:#FFD700; font-weight:bold; text-align:center;">👑 RATING DE OURO SELECIONADO</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bet-card gold-card"><div style="width:100%; text-align:center;">{golden_html}</div></div>', unsafe_allow_html=True)
    
    col_dl, col_clr = st.columns(2)
    with col_dl:
        out_txt = "\n".join([" ".join([f"{n:02}" for n in b]) for b in st.session_state.results])
        st.download_button("📥 BAIXAR JOGOS (.TXT)", out_txt, file_name="sniper_blocks_results.txt")
    with col_clr:
        if st.button("🧹 LIMPAR MEMÓRIA"):
            st.session_state.clear()
            st.rerun()

st.markdown('<div style="text-align:center; margin-top:50px; opacity:0.5; font-size:0.7rem;"><p>© 2026 TOTOLOTO ALGORITMIA PRO - POWERED BY SNIPER ENGINE</p></div>', unsafe_allow_html=True)
