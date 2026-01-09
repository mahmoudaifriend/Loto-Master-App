import streamlit as st
import time
import random
import base64
import os
from datetime import datetime

# --- 1. CONFIGURAÇÃO MASTER ---
st.set_page_config(page_title="Totoloto Algoritmia", layout="wide", initial_sidebar_state="collapsed")

def get_img_64(path):
    if os.path.exists(path):
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    return None

img_src = f"data:image/png;base64,{get_img_64('globo.png')}" if get_img_64('globo.png') else ""

# --- 2. DESIGN & MOBILE RESPONSIVE CSS ---
def inject_design():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@600&display=swap');
        .stApp {{ background: linear-gradient(180deg, #2d002a 0%, #000 100%); color: white; font-family: 'Rajdhani'; }}
        .header {{ font-family: 'Orbitron'; color: #ff4b00; text-align: center; font-size: 2.5rem; text-shadow: 0 0 20px #ff4b00; margin-bottom: 20px; }}
        
        /* GLOBO ANIMATION */
        .globo-box {{ display: flex; justify-content: center; align-items: center; position: relative; width: 280px; height: 280px; margin: 0 auto; }}
        .globo-img {{ width: 100%; z-index: 10; filter: drop-shadow(0 0 15px #930089); }}
        .neon-ring {{ position: absolute; width: 200px; height: 200px; border: 4px dotted #930089; border-radius: 50%; animation: spin 1.2s linear infinite; z-index: 5; box-shadow: 0 0 20px #930089; }}
        @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

        /* RESULTS WRAPPING (MOBILE FIX) */
        .bet-container {{ background: rgba(255,255,255,0.05); border-left: 5px solid #930089; padding: 15px; border-radius: 12px; margin-bottom: 10px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
        .ball {{ width: 45px; height: 45px; border-radius: 50%; background: radial-gradient(circle at 35% 35%, #fff, #930089, #000); display: inline-flex; align-items: center; justify-content: center; font-family: 'Orbitron'; font-weight: bold; font-size: 1.1rem; box-shadow: 3px 3px 10px #000; }}
        .ball-x {{ width: 45px; height: 45px; border-radius: 50%; background: #111; border: 2px dashed #ff4b00; display: inline-flex; align-items: center; justify-content: center; color: #ff4b00; font-family: 'Orbitron'; font-weight: bold; }}

        /* BUTTONS */
        div.stButton > button {{ background: linear-gradient(90deg, #ff4b00, #ff8700) !important; color: white; border-radius: 50px; font-family: 'Orbitron'; width: 100%; padding: 15px; border: none; box-shadow: 0 0 15px rgba(255,75,0,0.4); }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ALGORITMO DE INTELIGÊNCIA ---
class LotofacilEngine:
    def __init__(self, last_draw):
        self.last_draw = last_draw
        # Statistical Tendency Jan 2026 (Numbers with high frequency in last 30 days)
        self.hot_numbers = [2, 5, 6, 10, 13, 15, 18, 20, 23, 24, 25]
        self.pool = list(range(1, 26))

    def generate_elite_bets(self, quantity, closing_range, mode, luck):
        results = []
        for _ in range(quantity):
            # 1. Base Logic (Historic + Hot Numbers)
            base_pool = list(set(self.hot_numbers + self.last_draw))
            
            # 2. Closing (Fechamento) Logic
            if closing_range > 15:
                matrix = sorted(random.sample(self.pool, closing_range))
                bet = sorted(random.sample(matrix, 15))
            else:
                # Weighted Randomization
                weights = [2.0 if i in base_pool else 0.8 for i in self.pool]
                if luck > 50: weights = [w + random.uniform(0, luck/100) for w in weights]
                bet = []
                while len(bet) < 15:
                    n = random.choices(self.pool, weights=weights, k=1)[0]
                    if n not in bet: bet.append(n)
                bet.sort()
            
            results.append(bet)
        return results

# --- 4. APP INTERFACE ---
def main():
    inject_design()
    st.markdown(f"<p style='text-align:right; font-family:monospace;'>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>", unsafe_allow_html=True)
    st.markdown("<h1 class='header'>TOTOLOTO ALGORITMIA</h1>", unsafe_allow_html=True)

    # VISUAL GLOBO
    st.markdown(f"<div class='globo-box'><div class='neon-ring'></div><img src='{img_src}' class='globo-img'></div>", unsafe_allow_html=True)

    # INPUT PANEL
    with st.expander("🛠️ PAINEL DE CONFIGURAÇÃO ELITE", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            last_res = st.text_input("ÚLTIMO SORTEIO (15 números):", placeholder="01,02,05...")
            qnt = st.number_input("QUANTIDADE DE APOSTAS (até 1000):", 1, 1000, 100)
            mode = st.selectbox("TIPO DE JOGO:", ["Aposta Individual", "Bolão em Grupo"])
        with col2:
            closing = st.slider("MATRIZ DE FECHAMENTO (15-20 números):", 15, 20, 15)
            luck = st.slider("SORTE LÓGICA (ALGORITMO):", 0, 100, 75)

    # VALIDATION & RUN
    valid = False
    try:
        p_list = [int(x.strip()) for x in last_res.split(',') if x.strip()]
        if len(p_list) == 15: valid = True
    except: pass

    if st.button("🚀 GERAR JOGOS VENCEDORES", disabled=not valid):
        st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/misc/sounds/bingo-ball-machine-1.mp3"></audio>', unsafe_allow_html=True)
        
        engine = LotofacilEngine(p_list)
        bets = engine.generate_elite_bets(qnt, closing, mode, luck)
        
        # Display Best Samples (Visual feedback for first 5, list for rest)
        st.subheader(f"🔥 TOP {min(qnt, 100)} JOGOS GERADOS")
        
        hidden_pos = [random.randint(2, 12) for _ in range(qnt)]
        
        # To handle performance, we simulate 4.5s draw for the first 5 bets only, 
        # then show the rest instantly or in batches.
        display_limit = 5
        rows = [st.empty() for _ in range(display_limit)]
        memory = [[] for _ in range(display_limit)]

        for b_idx in range(15):
            time.sleep(4.5) # The Physical 4.5s pulse
            for j_idx in range(display_limit):
                if b_idx == hidden_pos[j_idx]:
                    ball_html = "<div class='ball-x'>X</div>"
                else:
                    val = bets[j_idx][b_idx]
                    ball_html = f"<div class='ball'>{(str(val).zfill(2))}</div>"
                
                memory[j_idx].append(ball_html)
                rows[j_idx].markdown(f"<div class='bet-container'><b>JOGO {j_idx+1}</b> {''.join(memory[j_idx])}</div>", unsafe_allow_html=True)
        
        # Show the rest of the 100 or 1000 bets in a structured table or text for the client
        if qnt > display_limit:
            st.info(f"O sistema processou mais {qnt-display_limit} jogos elite. Veja abaixo:")
            remaining_bets = [", ".join([str(n).zfill(2) for n in b]) for b in bets[display_limit:]]
            st.text_area("LISTA COMPLETA PARA COPIAR:", "\n".join(remaining_bets), height=300)

    if not valid and last_res:
        st.warning("⚠️ Insira exatamente 15 números separados por vírgula.")

if __name__ == "__main__":
    main()
