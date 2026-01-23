import streamlit as st
import time
import random
import pandas as pd
import io

# --- 1. APP CONFIGURATION ---
st.set_page_config(page_title="TOTOLOTO 15K PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. THE MECHANICAL PURPLE NEON UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');
    
    .stApp { background: #050005; color: #ffffff; font-family: 'Roboto', sans-serif; }
    
    /* MECHANICAL TUBES */
    .tube-rack { display: flex; justify-content: center; gap: 8px; margin-bottom: 30px; }
    .tube { 
        width: 25px; height: 120px; border: 2px solid #bf00ff; 
        border-radius: 0 0 20px 20px; background: linear-gradient(to bottom, rgba(191,0,255,0.05), rgba(191,0,255,0.2)); 
    }
    
    /* THE GLOBO - ADVANCED VISUALS */
    .globo-container { position: relative; width: 420px; height: 420px; margin: 0 auto; }
    .globo-sphere { 
        width: 100%; height: 100%; border: 8px solid #bf00ff; border-radius: 50%; 
        background: radial-gradient(circle at center, rgba(191,0,255,0.1) 0%, #000 100%);
        box-shadow: 0 0 60px rgba(191,0,255,0.5), inset 0 0 80px #000;
        display: flex; justify-content: center; align-items: center; position: relative; overflow: hidden;
    }
    
    .rotate-slow { animation: mechanicalRotate 10s linear infinite; }
    .rotate-fast { animation: mechanicalRotate 0.4s linear infinite; }
    @keyframes mechanicalRotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

    .ball { 
        width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; 
        font-weight: 900; font-size: 12px; color: white; position: absolute;
        background: radial-gradient(circle at 35% 35%, #f5ccff, #bf00ff 45%, #2b0035 100%);
        box-shadow: inset -4px -4px 10px rgba(0,0,0,0.8);
    }

    .status-panel { 
        text-align: center; font-family: 'Orbitron'; color: #bf00ff; 
        font-size: 1.5rem; margin: 20px; text-shadow: 0 0 15px #bf00ff; 
    }

    .result-tray { 
        display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; 
        margin-top: 40px; padding: 20px; background: rgba(255,255,255,0.02); border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. THE UGLY LOGIC ENGINE (ZERO-BASED) ---
def generate_ugly_bet():
    primes = {2, 3, 5, 7, 11, 13, 17, 19, 23}
    while True:
        bet = sorted(random.sample(range(1, 26), 15))
        odds = len([n for n in bet if n % 2 != 0])
        s_val = sum(bet)
        p_count = len([n for n in bet if n in primes])
        
        # Max Sequence Filter
        max_seq, curr_seq = 1, 1
        for i in range(len(bet)-1):
            if bet[i+1] == bet[i] + 1: curr_seq += 1
            else:
                max_seq = max(max_seq, curr_seq)
                curr_seq = 1
        max_seq = max(max_seq, curr_seq)

        if odds in [7, 8, 9] and 180 <= s_val <= 210 and p_count in [5, 6] and max_seq <= 4:
            return bet

# --- 4. MAIN INTERFACE ---
st.markdown('<h1 style="text-align:center; font-family:Orbitron; color:white; text-shadow: 0 0 30px #bf00ff;">TOTOLOTO 15K PRO</h1>', unsafe_allow_html=True)

tab_sim, tab_bulk = st.tabs(["MECHANICAL SIMULATION", "BULK GENERATION (15,000)"])

with tab_bulk:
    st.markdown("### SOVEREIGN BATCH GENERATOR")
    if st.button("GENERATE 15,000 UGLY BETS 🚀"):
        with st.spinner("Processing 15,000 algorithmic combinations..."):
            batch = [generate_ugly_bet() for _ in range(15000)]
            df = pd.DataFrame(batch)
            output = io.StringIO()
            for b in batch:
                output.write(" ".join([f"{n:02}" for n in b]) + "\n")
            
            st.success("15,000 Bets Generated Successfully!")
            st.download_button("📥 DOWNLOAD 15,000 BETS (.TXT)", output.getvalue(), file_name="totoloto_15k_sovereign.txt")

with tab_sim:
    # Top Tubes
    tube_cols = st.columns(15)
    for i in range(15): tube_cols[i].markdown('<div class="tube"></div>', unsafe_allow_html=True)

    status_area = st.empty()
    globo_area = st.empty()
    tray_area = st.empty()

    def refresh_sim(speed_class, in_globo_count, ejected_list, msg):
        # We simulate balls as dots inside the globe for performance
        balls_html = ""
        for _ in range(in_globo_count):
            t, l = random.randint(15, 85), random.randint(15, 85)
            balls_html += f'<div class="ball" style="top:{t}%; left:{left}%;"></div>'
            
        globo_area.markdown(f'''
            <div class="globo-container">
                <div class="globo-sphere {speed_class}">{balls_html}</div>
            </div>
        ''', unsafe_allow_html=True)
        
        tray_html = "".join([f'<div class="ball" style="position:static; margin:5px;">{n:02}</div>' for n in sorted(ejected_list)])
        tray_area.markdown(f'<div class="result-tray">{tray_html}</div>', unsafe_allow_html=True)
        status_area.markdown(f'<div class="status-panel">{msg}</div>', unsafe_allow_html=True)

    if st.button("START MECHANICAL EXTRACTION 🎬"):
        target = generate_ugly_bet()
        ejected = []
        
        # PROTOCOL 1: Settle at bottom
        refresh_sim("rotate-slow", 25, ejected, "BALLS SETTLING IN THE CHAMBER...")
        time.sleep(2)
        
        # PROTOCOL 2: 15-Ball Extraction Cycle
        for i in range(15):
            # FAST MIXING (4.5s)
            refresh_sim("rotate-fast", 25 - i, ejected, f"INTENSE SHUFFLE - ROUND {i+1}")
            time.sleep(4.5)
            
            # SLOW EJECTION (4.5s)
            ejected.append(target[i])
            refresh_sim("rotate-slow", 25 - (i+1), ejected, f"SLOWING DOWN... EJECTING BALL #{i+1}")
            time.sleep(4.5)
            
        status_area.markdown('<div class="status-panel" style="color:#00ff00;">EXTRACTION COMPLETE</div>', unsafe_allow_html=True)
        st.balloons()

st.markdown('<div style="text-align:center; margin-top:60px; opacity:0.2; font-size:0.8rem;">© 2026 SOVEREIGN LOGIC - NO ARABIC STRINGS IN CODE</div>', unsafe_allow_html=True)
