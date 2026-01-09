# -*- coding: utf-8 -*-
# =====================================================
# TOTOLOTO ALGORITMIA
# Lotofacil Simulation & Analysis Engine (PRO+)
# Plataforma: Streamlit
# =====================================================

import streamlit as st
import random
import math
import requests
from collections import Counter

# -----------------------------------------------------
# CONFIGURAÇÃO GERAL
# -----------------------------------------------------
st.set_page_config(
    page_title="TOTOLOTO ALGORITMIA",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------
# API – Último sorteio oficial Lotofácil (Caixa)
# -----------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_last_draw():
    try:
        res = requests.get(
            "https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest",
            timeout=10
        )
        data = res.json()
        return [int(n) for n in data["dezenas"]]
    except Exception:
        return []

LAST_DRAW = fetch_last_draw()

# -----------------------------------------------------
# HOT / COLD ENGINE (sem كشف)
# -----------------------------------------------------
def hot_cold_weights(last_draw):
    weights = {}
    for n in range(1, 26):
        base = 1.0
        if n in last_draw:
            base += random.uniform(0.3, 0.6)
        base += random.uniform(0.0, 0.4)
        weights[n] = base
    return weights

# -----------------------------------------------------
# GERADOR DE APOSTAS
# -----------------------------------------------------
def generate_bet(weights, size=15, allow_x=True):
    nums = list(weights.keys())
    selected = random.choices(nums, weights=[weights[n] for n in nums], k=size)
    bet = sorted(set(selected))

    while len(bet) < size:
        bet.append(random.choice(nums))
        bet = sorted(set(bet))

    if allow_x:
        x_pos = random.randint(0, len(bet) - 1)
        bet[x_pos] = "X"

    return bet

def generate_bets(qty, bet_size, allow_x=True):
    weights = hot_cold_weights(LAST_DRAW)
    return [generate_bet(weights, bet_size, allow_x) for _ in range(qty)]

# -----------------------------------------------------
# CONTADOR DE ACERTOS
# -----------------------------------------------------
def count_hits(bet, draw):
    return len([n for n in bet if n != "X" and n in draw])

# -----------------------------------------------------
# SOCIAL PROOF
# -----------------------------------------------------
def render_social_proof(bets, draw):
    stats = Counter()
    for b in bets:
        hits = count_hits(b, draw)
        if hits >= 11:
            stats[hits] += 1

    if not stats:
        return

    st.markdown("### Comparação com o último sorteio")

    if stats.get(14, 0) > 0:
        st.markdown(
            f"<div style='padding:12px;border-radius:12px;"
            f"background:linear-gradient(90deg,#f5c542,#ffdd88);"
            f"color:black;font-weight:700;'>"
            f"🔥 {stats[14]} apostas fariam 14 pontos"
            f"</div>",
            unsafe_allow_html=True
        )

    if stats.get(13, 0) > 0:
        st.markdown(
            f"<div style='margin-top:8px;padding:10px;border-radius:10px;"
            f"background:linear-gradient(90deg,#7c3aed,#a78bfa);"
            f"color:white;font-weight:600;'>"
            f"⭐ {stats[13]} apostas fariam 13 pontos"
            f"</div>",
            unsafe_allow_html=True
        )

    for k in [12, 11]:
        if stats.get(k, 0) > 0:
            st.write(f"{stats[k]} apostas fariam {k} pontos")

# -----------------------------------------------------
# MOTOR CIRCULAR (25 BOLAS)
# -----------------------------------------------------
def render_circular_engine():
    balls = []
    radius = 120
    cx, cy = 150, 150

    for i in range(25):
        angle = (2 * math.pi / 25) * i
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        balls.append(
            f"<circle cx='{x}' cy='{y}' r='14' fill='hsl({i*14},70%,55%)' />"
            f"<text x='{x}' y='{y+5}' text-anchor='middle' "
            f"font-size='10' fill='black'>{i+1}</text>"
        )

    svg = (
        "<svg width='300' height='300' viewBox='0 0 300 300'>"
        "<g>"
        + "".join(balls) +
        "</g></svg>"
    )

    st.markdown(svg, unsafe_allow_html=True)

# -----------------------------------------------------
# INTERFACE
# -----------------------------------------------------
st.title("TOTOLOTO ALGORITMIA")
st.caption("Simulação inteligente para Lotofácil")

render_circular_engine()

modo = st.selectbox(
    "Modo de jogo",
    ["Individual", "Bolão (Fechamento)"]
)

bet_size = st.slider(
    "Quantidade de números por aposta",
    min_value=15,
    max_value=20,
    value=15
)

qty_range = st.radio(
    "Quantidade de apostas",
    ["1–100", "100–1000", "1000–10000"]
)

if qty_range == "1–100":
    qty = st.slider("Apostas", 1, 100, 20)
elif qty_range == "100–1000":
    qty = st.slider("Apostas", 100, 1000, 200)
else:
    qty = st.slider("Apostas", 1000, 10000, 2000)

simulate = st.button("Simular")

# -----------------------------------------------------
# RESULTADOS
# -----------------------------------------------------
if simulate:
    allow_x = modo == "Individual"
    bets = generate_bets(qty, bet_size, allow_x)

    st.markdown("### Resultados (amostra)")
    for b in bets[:10]:
        st.write(" ".join(str(n).zfill(2) if n != "X" else "X" for n in b))

    # Copiar para Caixa
    formatted = "\n".join(
        " ".join(str(n).zfill(2) for n in b if n != "X")
        for b in bets
    )

    st.text_area(
        "Copiar apostas para Caixa",
        value=formatted,
        height=200
    )

    if LAST_DRAW:
        render_social_proof(bets, LAST_DRAW)
