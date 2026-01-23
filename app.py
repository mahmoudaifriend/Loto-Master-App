import streamlit as st
import time
import random
import itertools

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="TOTOLOTO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. PREMIUM PURPLE NEON CSS (LOTOFÁCIL VIBE) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;700&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #2b0035 0%, #000000 100%); 
        color: #ffffff; 
        font-family: 'Roboto', sans-serif; 
    }
    
    .main-title { 
        font-family: 'Orbitron', sans-serif; 
        font-size: 3.5rem; 
        text-align: center; 
        color: #fff; 
        text-shadow: 0 0 10px #bf00ff, 0 0 20px #bf00ff, 0 0 40px #bf00ff; 
        margin-bottom: 5px; 
    }

    /* THE GLOBO - FIXED ROTATION & VISIBILITY */
    .motor-outer { 
        display: flex; justify-content: center; align-items: center; 
        margin: 30px auto; width: 300px; height: 300px; 
        border: 5px solid #bf00ff; border-radius: 50%; 
        background: rgba(191, 0, 255, 0.05); 
        box-shadow: 0 0 30px rgba(191, 0, 255, 0.4), inset 0 0 50px #000; 
        position: relative; overflow: hidden;
    }

    .motor-inner { 
        width: 100%; height: 100%; 
        display: flex; flex-wrap: wrap; 
        justify-content: center; align-items: center; 
        padding: 20px;
        animation: rotateGlobe 4s linear infinite;
    }

    @keyframes rotateGlobe {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .ball { 
        width: 32px; height: 32px; border-radius: 50%; 
        display: inline-flex; align-items: center; justify-content: center; 
        margin: 4px; font-weight: bold; font-size: 13px; color: white; 
        background: radial-gradient(circle at 30% 30%, #e680ff, #bf00ff 50%, #4b0082 100%);
        box-shadow: 0 4px 10px rgba(0,0,0,0.5), inset -2px -2px 5px rgba(0,0,0,0.5);
    }

    /* SELECTION GRID */
    .grid-container { 
        display: grid; grid-template-columns: repeat(5, 1fr); 
        gap: 8px; max-width: 450px; margin: 20px auto; 
    }

    /* BET CARDS */
    .bet-card { 
        background: rgba(255, 255, 255, 0.05); 
        border: 1px solid rgba(191, 0, 255, 0.3); 
        border-radius: 12px; padding: 15px; margin-bottom: 10px; 
        display: flex; flex-wrap: wrap; justify-content: center;
        transition: 0.3s;
    }
    .bet-card:hover { border-color: #bf00ff; box-shadow: 0 0 15px rgba(191, 0, 255, 0.2); }

    /* BUTTONS */
    div.stButton > button { 
        background: linear-gradient(45deg, #4b0082, #bf00ff) !important; 
        color: white !important; border: none !important; 
        padding: 12px 24px !important; font-weight: bold !important; 
        border-radius: 8px !important; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SOVEREIGN LOGIC (12 TO 10) ---
def generate_sovereign_bets(fixed_12, qty=10):
    all_nums = set(range(1, 26))
    pool = list(all_nums - set(fixed_12))
    
    # Generate all 286 combinations of the remaining 3 numbers
    combos = list(itertools.combinations(pool, 3))
    valid_candidates = []
    
    for c in combos:
        bet = sorted(list(fixed_12) + list(c))
        # Filter 1: Parity (7 or 8 Odds)
        odds = len([n for n in bet if n % 2 != 0])
        # Filter 2: Sum Range (180 - 210)
        s_val = sum(bet)
        # Filter 3: Primes (5 or 6)
        primes = len([n for n in bet if n in [2, 3, 5, 7, 11, 13, 17, 19, 23]])
        
        if odds in [7, 8] and 180 <= s_val <= 210 and primes in [5, 6]:
            valid_candidates.append(bet)
    
    if len(valid_candidates) < qty:
        # If filters are too tight, relax them slightly to meet qty
        return [sorted(list(fixed_12) + list(random.sample(pool, 3))) for _ in range(qty)]
    
    return random.sample(valid_candidates, qty)

# --- 4. APP INTERFACE ---
st.markdown('<div class="main-title">💎 TOTOLOTO PRO 💎</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; opacity:0.6;">SOVEREIGN ALGORITHMIC SYSTEM</p>', unsafe_allow_html=True)

# Globe Visualization
motor_placeholder = st.empty()
def render_globe(active=False):
    anim_class = "chaos-active" if active else ""
    balls_html = "".join([f'<div class="ball">{random.randint(1,25):02}</div>' for _ in range(12)])
    motor_placeholder.markdown(f'''
        <div class="motor-outer">
            <div class="motor-inner">{balls_html}</div>
        </div>
    ''', unsafe_allow_html=True)

render_globe()

# User Selection Grid
st.markdown('<p style="text-align:center; color:#bf00ff;">SELECT YOUR 12 CONFIRMED NUMBERS:</p>', unsafe_allow_html=True)
cols = st.columns(5)
selected = []
for i in range(1, 26):
    with cols[(i-1)%5]:
        if st.checkbox(f"{i:02}", key=f"num_{i}"):
            selected.append(i)

st.markdown("---")
col_opt, col_btn = st.columns([1, 2])
with col_opt:
    bet_qty = st.selectbox("Quantity:", [10, 20])
with col_btn:
    run_btn = st.button("START EXTRACTION 🚀")

if run_btn:
    if len(selected) != 12:
        st.error(f"Error: Please select exactly 12 numbers. You have selected {len(selected)}.")
    else:
        # Simulation phase
        render_globe(active=True)
        time.sleep(3)
        
        results = generate_sovereign_bets(selected, bet_qty)
        st.session_state.final_results = results
        
        # Display results
        for i, bet in enumerate(results):
            balls_html = "".join([f'<div class="ball">{n:02}</div>' for n in bet])
            st.markdown(f'<div class="bet-card"><b>#{i+1:02}</b> &nbsp; {balls_html}</div>', unsafe_allow_html=True)
        st.balloons()

# Reset and Download
if 'final_results' in st.session_state:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧹 CLEAR SYSTEM"):
            st.session_state.clear()
            st.rerun()
    with c2:
        out_text = "\n".join([" ".join([f"{n:02}" for n in b]) for b in st.session_state.final_results])
        st.download_button("📥 DOWNLOAD RESULTS", out_text, file_name="totoloto_results.txt")

st.markdown('<div style="text-align:center; margin-top:50px; opacity:0.3; font-size:0.8rem;">© 2026 TOTOLOTO PRO SYSTEM</div>', unsafe_allow_html=True)
