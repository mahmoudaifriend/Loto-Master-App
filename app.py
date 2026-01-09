# -*- coding: utf-8 -*-
import streamlit as st
import random
import math
import time
import requests

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="TOTOLOTO ALGORITMIA",
    layout="centered"
)

# --------------------------------------------------
# GLOBAL STYLE (LOTOfácil)
# --------------------------------------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #2b0a3d, #120018);
    color: #f5d76e;
}
h1, h2, h3 {
    color: #f5d76e;
}
.engine {
    width:300px;
    height:300px;
    margin:auto;
    animation: spin 12s linear infinite;
    filter: drop-shadow(0 0 25px #a855f7);
}
@keyframes spin {
    from {transform: rotate(0deg);}
    to {transform: rotate(360deg);}
}
.ball {
    fill: #7c3aed;
}
.simulating .engine {
    animation: spin 2s linear infinite;
}
.result-ball {
    display:inline-block;
    width:42px;
    height:42px;
    border-radius:50%;
    background:#f5d76e;
    color:#1a0022;
    text-align:center;
    line-height:42px;
    margin:4px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# API LAST DRAW
# --------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_last_draw():
    try:
        r = requests.get(
            "https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest",
            timeout=10
        )
        return [int(n) for n in r.json()["dezenas"]]
    except:
        return []

LAST_DRAW = fetch_last_draw()

# --------------------------------------------------
# ENGINE VISUAL
# --------------------------------------------------
def render_engine():
    balls = []
    r = 120
    cx = cy = 150
    for i in range(25):
        ang = 2 * math.pi * i / 25
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        balls.append(
            f"<circle cx='{x}' cy='{y}' r='14' class='ball' />"
            f"<text x='{x}' y='{y+5}' text-anchor='middle' font-size='10' fill='black'>{i+1}</text>"
        )
    svg = "<svg class='engine' viewBox='0 0 300 300'>" + "".join(balls) + "</svg>"
    st.markdown(svg, unsafe_allow_html=True)

# --------------------------------------------------
# HOT/COLD (SILENT)
# --------------------------------------------------
def generate_bet(size=15, allow_x=True):
    nums = list(range(1,26))
    weights = []
    for n in nums:
        w = 1.0
        if n in LAST_DRAW:
            w += random.uniform(0.4,0.7)
        weights.append(w)
    bet = sorted(random.choices(nums, weights=weights, k=size))
    bet = list(dict.fromkeys(bet))
    while len(bet)<size:
        bet.append(random.choice(nums))
        bet = list(dict.fromkeys(bet))
    bet.sort()
    if allow_x:
        bet[random.randint(0,size-1)] = "X"
    return bet

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("TOTOLOTO ALGORITMIA")
st.caption("Motor inteligente para Lotofácil")

render_engine()

modo = st.radio("Modo", ["Individual", "Bolão"])
range_choice = st.radio("Quantidade de apostas", ["1–100", "100–1000", "1000–10000"])

if range_choice == "1–100":
    qty = 100
elif range_choice == "100–1000":
    qty = 500
else:
    qty = 2000

simulate = st.button("🔮 Simular agora")

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------
if simulate:
    st.markdown("<div class='simulating'>", unsafe_allow_html=True)
    bets = [generate_bet(15, modo=="Individual") for _ in range(qty)]

    st.subheader("Apostas (revelação)")
    for i, b in enumerate(bets[:5]):
        row = st.empty()
        shown = ""
        for n in b:
            time.sleep(0.3)
            shown += f"<span class='result-ball'>{n}</span>"
            row.markdown(shown, unsafe_allow_html=True)

    st.subheader("Resumo")
    st.write(f"{qty} apostas geradas com sucesso.")

    text = "\n".join(
        " ".join(str(n).zfill(2) for n in b if n!="X")
        for b in bets
    )

    st.text_area("Copiar para Caixa", text, height=200)
