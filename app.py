import streamlit as st
import time
import random
import requests
from collections import Counter

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="TOTOLOTO ALGORITMIA PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS AVANÇADO (RESPONSIVO E REALISTA) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');
    
    /* Background Azul Claro Profissional */
    .stApp { 
        background: linear-gradient(180deg, #e0f2f1 0%, #b3e5fc 100%); 
        color: #01579b; 
        font-family: 'Roboto', sans-serif; 
    }
    
    .main-title { font-family: 'Orbitron', sans-serif; font-size: 2.5rem; text-align: center; color: #0277bd; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 0.8rem; color: #01579b; margin-bottom: 20px; letter-spacing: 1px; font-weight: bold; }
    
    /* BOLAS 3D REALISTAS */
    .ball { 
        width: 35px; height: 35px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; margin: 2px; 
        font-weight: 800; font-size: 13px; color: white; 
        background: radial-gradient(circle at 35% 35%, #4fc3f7, #0288d1 45%, #01579b 90%);
        box-shadow: inset -3px -3px 8px rgba(0,0,0,0.5), 0 3px 6px rgba(0,0,0,0.3);
        transition: all 0.5s ease;
    }

    /* GLOBO REALISTA COM GRAVIDADE */
    .motor-outer { 
        display: flex; justify-content: center; align-items: center; margin: 20px auto; 
        width: 250px; height: 250px; border: 6px solid #0288d1; border-radius: 50%; 
        background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(5px); 
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); overflow: hidden; position: relative; 
    }
    .motor-inner { 
        width: 100%; height: 100%; display: flex; flex-wrap: wrap; 
        justify-content: center; align-items: flex-end; padding: 20px; 
    }
    
    /* Animação de Acúmulo no Fundo (Gravity) */
    .ball-idle { transform: translateY(80px); opacity: 0.8; }
    
    /* Animação de Caos (Spin Fast) */
    @keyframes chaos {
        0% { transform: translate(0,0) rotate(0deg); }
        25% { transform: translate(20px, -50px) rotate(90deg); }
        50% { transform: translate(-20px, -100px) rotate(180deg); }
        75% { transform: translate(30px, -40px) rotate(270deg); }
        100% { transform: translate(0,0) rotate(360deg); }
    }
    .spin-active .ball { animation: chaos 0.3s infinite linear; }
    
    /* Animação de Desaceleração (Spin Slow) */
    @keyframes slow-chaos {
        0% { transform: translate(0,0); }
        100% { transform: translate(5px, 10px); }
    }
    .spin-slow .ball { animation: slow-chaos 1.5s infinite alternate ease-in-out; }

    /* GRID RESPONSIVO */
    .grid-container { 
        display: grid; grid-template-columns: repeat(auto-fit, minmax(45px, 1fr)); 
        gap: 5px; background: white; padding: 15px; border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
    }

    .bet-card { 
        background: white; border-radius: 12px; padding: 10px; margin-bottom: 8px; 
        display: flex; flex-wrap: wrap; align-items: center; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #0288d1;
    }
    .strong-bet { border-left: 5px solid #ff9800; background: #fff8e1; }

    /* Estilo do Botão Valendo */
    div.stButton > button { 
        background: #0288d1 !important; color: white !important; 
        width: 100%; font-size: 1.5rem !important; font-weight: bold !important; 
        border-radius: 50px; padding: 15px; border: none; box-shadow: 0 4px 15px rgba(2, 136, 209, 0.4);
    }
    
    /* Fireworks Effect Placeholder */
    .fireworks { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 999; }
</style>
""", unsafe_allow_html=True)

# --- 3. ALGORITMO DE BLOCOS (LÓGICA DA MÁQUINA) ---
def attack_blocks_engine(fixed_backbone, qty=10):
    triplets = [[7, 8, 9], [16, 17, 19], [4, 5, 6], [21, 22, 23]]
    pairs = [[13, 15], [10, 12], [23, 24], [3, 5]]
    all_bets = []
    while len(all_bets) < qty:
        current_bet = set(fixed_backbone)
        random.shuffle(triplets); random.shuffle(pairs)
        for tri in triplets:
            if len(current_bet) + 3 <= 15: current_bet.update(tri); break
        for pr in pairs:
            if len(current_bet) + 2 <= 15: current_bet.update(pr)
        while len(current_bet) < 15: current_bet.add(random.randint(1, 25))
        final_list = sorted(list(current_bet))
        
        # Filtro de Sequência Máxima 4
        seq_ok = True
        for i in range(len(final_list)-4):
            if final_list[i+4] == final_list[i] + 4: seq_ok = False; break
        
        if seq_ok and len([n for n in final_list if n % 2 != 0]) in [7, 8]:
            if final_list not in all_bets: all_bets.append(final_list)
    return all_bets

# --- 4. INTERFACE ---
st.markdown('<div class="main-title">💎 TOTOLOTO ALGORITMIA 💎</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">محاكي السحب العشوائي بنظام الكتل الهجومية</div>', unsafe_allow_html=True)

# Grid de Seleção (Responsive)
st.markdown('<p style="font-weight:bold; color:#01579b;">اختر هيكلك الأساسي (HAYKAL):</p>', unsafe_allow_html=True)
cols = st.columns(5)
selected_nums = []
for i in range(1, 26):
    with cols[(i-1)%5]:
        if st.checkbox(f"{i:02}", key=f"n_{i}"): selected_nums.append(i)

# Quantidade de Apostas (Visível abaixo do grid)
qty = st.selectbox("عدد الرهانات المطلوب توليدها:", [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

st.markdown("---")
motor_placeholder = st.empty()
valendo_text = st.empty()

def render_globe(state="idle"):
    chaos_class = "spin-active" if state == "fast" else ("spin-slow" if state == "slow" else "ball-idle")
    balls_html = "".join([f'<div class="ball {chaos_class}">{random.randint(1,25)}</div>' for _ in range(20)])
    motor_placeholder.markdown(f'<div class="motor-outer"><div class="motor-inner">{balls_html}</div></div>', unsafe_allow_html=True)

render_globe("idle")

# --- 5. LOGICA DE SORTEIO (VALENDO) ---
if st.button("VALENDO 🚀"):
    if not selected_nums:
        st.error("⚠️ الرجاء اختيار أرقام الهيكل أولاً!")
    else:
        results = attack_blocks_engine(selected_nums, qty)
        st.session_state.results = results
        current_display = [[] for _ in range(qty)]
        
        list_placeholder = st.empty()
        
        # 15 Cycles Loop
        for ball_turn in range(15):
            valendo_text.markdown(f'<h2 style="text-align:center; color:#0288d1;">VALENDO... (Bola {ball_turn+1}/15)</h2>', unsafe_allow_html=True)
            
            # Fast Rotation (4.5s)
            render_globe("fast")
            time.sleep(4.5)
            
            # Slow Rotation & Ball Drop (4.5s)
            render_globe("slow")
            time.sleep(4.5)
            
            # Update each bet with its next number
            for i in range(qty):
                current_display[i].append(results[i][ball_turn])
            
            # Display Progress
            with list_placeholder.container():
                # Top 5 Strong Bets
                st.markdown("### 🔥 أقوى 5 رهانات (المسار الذهبي):")
                for i in range(5):
                    balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(current_display[i])])
                    st.markdown(f'<div class="bet-card strong-bet"><b>⭐ {i+1:02}</b> &nbsp; {balls_html}</div>', unsafe_allow_html=True)
                
                st.markdown(f"### 📋 بقية الرهانات ({qty-5}):")
                for i in range(5, qty):
                    balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in sorted(current_display[i])])
                    st.markdown(f'<div class="bet-card"><b>#{i+1:02}</b> &nbsp; {balls_html}</div>', unsafe_allow_html=True)

        valendo_text.empty()
        render_globe("idle")
        
        # Fireworks Celebration (Using balloons as standard, custom CSS firework can be added)
        st.snow() # Fireworks alternative in Streamlit
        st.success("✅ تم اكتمال محاكاة السحب بنجاح!")

# --- 6. EXPORT ---
if 'results' in st.session_state:
    out_txt = "\n".join([" ".join([f"{n:02}" for n in b]) for b in st.session_state.results])
    st.download_button("📥 تحميل كافة الرهانات (TXT)", out_txt, file_name="lotofacil_sniper.txt")

st.markdown('<div style="text-align:center; margin-top:30px; opacity:0.6;">© 2026 TOTOLOTO PRO - BRASIL</div>', unsafe_allow_html=True)
