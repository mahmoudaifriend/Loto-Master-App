import streamlit as st
import time
import random
from collections import Counter

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TOTOLOTO SNIPER", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS PROFISSIONAL (SNIPER STYLE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');
    
    .stApp { background: radial-gradient(circle at top, #050005 0%, #000000 100%); color: #ffffff; font-family: 'Roboto', sans-serif; }
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 3rem; text-align: center; color: #fff; text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 0.9rem; color: #00ff00; margin-bottom: 30px; letter-spacing: 2px; font-weight: bold; text-shadow: 0 0 5px #00ff00; }
    
    .ball { 
        width: 38px; height: 38px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin: 3px; 
        font-weight: 800; font-size: 14px; color: white; 
        background: radial-gradient(circle at 35% 35%, #b3ffb3, #00ff00 45%, #004d00 90%);
        box-shadow: inset -4px -4px 10px rgba(0,0,0,0.8), inset 3px 3px 6px rgba(255,255,255,0.4), 0 5px 15px rgba(0,0,0,0.5);
    }
    
    .motor-outer { display: flex; justify-content: center; align-items: center; margin: 25px auto; width: 280px; height: 280px; border: 4px solid #00ff00; border-radius: 50%; background: rgba(0, 255, 0, 0.05); backdrop-filter: blur(8px); box-shadow: 0 0 50px rgba(0, 255, 0, 0.2); overflow: hidden; position: relative; }
    .motor-inner { width: 100%; height: 100%; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; padding: 35px; }
    
    .bet-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0,255,0,0.2); border-radius: 15px; padding: 12px; margin-bottom: 12px; display: flex; flex-wrap: wrap; align-items: center; }
    .range-tag { background: #004d00; color: #00ff00; padding: 2px 8px; border-radius: 5px; font-size: 0.7rem; margin-right: 10px; border: 1px solid #00ff00; }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DO SISTEMA SNIPER ---
def generate_sniper_bets(last_draw_list):
    all_bets = []
    # Define RANGES based on the system
    ranges = [
        (1, 25, 5), # 5 bets (1-25)
        (2, 25, 2), # 2 bets (2-25)
        (1, 24, 2), # 2 bets (1-24)
        (3, 25, 1)  # 1 bet (3-25)
    ]
    
    for start, end, count in ranges:
        for _ in range(count):
            pool = list(range(start, end + 1))
            last_in_pool = [n for n in last_draw_list if n in pool]
            missing_in_pool = [n for n in pool if n not in last_draw_list]
            
            # 9 from last draw + 6 from missing (Adaptive)
            n_last = min(len(last_in_pool), 9)
            n_miss = 15 - n_last
            
            selected_last = random.sample(last_in_pool, n_last)
            selected_miss = random.sample(missing_in_pool, n_miss)
            
            bet = sorted(selected_last + selected_miss)
            all_bets.append({"bet": bet, "range": f"{start:02}-{end:02}"})
            
    return all_bets

# --- 4. INTERFACE ---
st.markdown('<div class="main-title">🎯 SNIPER LOTOFÁCIL 🎯</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">SYSTEM V2: 9+6 MATRIX ALGORITHM</div>', unsafe_allow_html=True)

# INPUT OBRIGATÓRIO DO ÚLTIMO SORTEIO
with st.sidebar:
    st.header("⚙️ CONFIG")
    last_draw_input = st.text_input("ENTER LAST DRAW (15 numbers separated by space):", placeholder="Ex: 01 04 05 06...")

if last_draw_input:
    try:
        last_draw_nums = sorted([int(n) for n in last_draw_input.split() if n.strip()])
        if len(last_draw_nums) != 15:
            st.warning("⚠️ Please enter EXACTLY 15 numbers.")
            st.stop()
        st.session_state.last_draw = last_draw_nums
        st.success(f"✅ Last Draw Loaded: {last_draw_nums}")
    except:
        st.error("❌ Invalid Format. Use spaces between numbers.")
        st.stop()
else:
    st.info("💡 Enter the LAST DRAW results in the sidebar to unlock the system.")
    st.stop()

# --- 5. EXECUÇÃO ---
if st.button("GENERATE 10 SNIPER BETS 🚀"):
    st.session_state.bets = generate_sniper_bets(st.session_state.last_draw)

if 'bets' in st.session_state:
    st.markdown("---")
    for i, item in enumerate(st.session_state.bets):
        bet = item['bet']
        r_text = item['range']
        balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in bet])
        st.markdown(f'''
            <div class="bet-card">
                <span class="range-tag">RANGE {r_text}</span>
                <b>#{i+1:02}</b> &nbsp; {balls_html}
            </div>
        ''', unsafe_allow_html=True)

    # TOOLS
    st.markdown("---")
    col_clr, col_dl = st.columns(2)
    with col_clr:
        if st.button("🧹 CLEAR SYSTEM"):
            st.session_state.clear()
            st.rerun()
    with col_dl:
        out_txt = "\n".join([" ".join([f"{n:02}" for n in b['bet']]) for b in st.session_state.bets])
        st.download_button("📥 DOWNLOAD SNIPER_RESULTS (.TXT)", out_txt, file_name="lotofacil_sniper.txt")

st.markdown('<div style="text-align:center; opacity:0.5; font-size:0.8rem; margin-top:50px;"><p>© 2026 SNIPER PRO - NO MEMORY, ONLY MATH.</p></div>', unsafe_allow_html=True)
