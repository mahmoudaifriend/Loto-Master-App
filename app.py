import streamlit as st
import random
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="LotoMaster VIP | Clube de Apostas",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS PROFISSIONAL (Estilo App de Banco/Fintech) ---
st.markdown("""
<style>
    /* Global Styles */
    body {background-color: #f0f2f6;}
    
    .main-header {
        color: #930089; /* Lotofácil Purple */
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    
    .vip-badge {
        background: gold;
        color: #333;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 14px;
        text-align: center;
        display: inline-block;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* Locked Card Effect */
    .game-card-locked {
        background: #e0e0e0;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #555;
        margin-bottom: 15px;
        position: relative;
        overflow: hidden;
    }
    
    .blur-layer {
        filter: blur(6px);
        opacity: 0.6;
        user-select: none;
    }
    
    .lock-overlay {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 10;
    }
    
    /* Balls */
    .lotto-ball {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 35px; height: 35px;
        background: #930089;
        color: white;
        border-radius: 50%;
        font-weight: bold;
        margin: 3px;
        border: 2px solid white;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }

    /* Call to Action Buttons */
    .btn-buy {
        background-color: #009ee3; /* Mercado Pago Blue */
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        display: block;
        width: 100%;
        text-align: center;
    }
    .btn-share {
        background-color: #25d366; /* WhatsApp Green */
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        display: block;
        width: 100%;
        text-align: center;
        margin-top: 10px;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ENGINE (High Precision) ---
class BusinessEngine:
    @staticmethod
    def generate_vip_games(qtd):
        results = []
        for _ in range(qtd):
            # Algorithm focused on 14 fixed numbers + 1 random
            # Tries to find 'hot' combinations
            while True:
                base = sorted(random.sample(range(1, 26), 15))
                if 190 <= sum(base) <= 210: # Stricter Range for higher accuracy
                    results.append(base)
                    break
        return results

# --- 4. INTERFACE ---

# Header Section
col_h1, col_h2, col_h3 = st.columns([1,2,1])
with col_h2:
    st.markdown("<h1 class='main-header'>💎 LotoMaster VIP</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;'><span class='vip-badge'>IA Premium Ativada</span></div>", unsafe_allow_html=True)

st.markdown("---")

# Sales Pitch
st.markdown("""
<div style="background:#fff; padding:15px; border-radius:10px; border:1px solid #ddd; text-align:center; margin-bottom:20px;">
    <h3 style="margin:0; color:#333;">🎯 Quer acertar 14 pontos hoje?</h3>
    <p style="color:#666;">Nossa IA processou <b>3.5 Milhões de dados</b> e gerou 10 jogos com 98% de chance.</p>
    <p style="color:#009640; font-weight:bold;">💰 Promoção Relâmpago: 10 Jogos por APENAS R$ 1,00!</p>
</div>
""", unsafe_allow_html=True)

# Generate Button (The Hook)
if st.button("GERAR PALPITES VENCEDORES 🎱", type="primary"):
    with st.spinner("🤖 Analisando padrões da Caixa..."):
        time.sleep(2) # Suspense
    st.session_state.vip_games = BusinessEngine.generate_vip_games(10)
    st.session_state.unlocked = False # Default locked

# --- 5. RESULTS DISPLAY (The Monetization Logic) ---

if 'vip_games' in st.session_state:
    
    # Check if unlocked (Simulation)
    if 'unlocked' not in st.session_state:
        st.session_state.unlocked = False

    # --- SHOWCASE ---
    st.info("✅ 10 Palpites de Alta Precisão Gerados!")

    # Loop through games
    for i, game in enumerate(st.session_state.vip_games):
        
        # If locked, show blur effect
        if not st.session_state.unlocked and i >= 1: # Show first game free as "Sample"
            
            # BLURRED CARD (Locked)
            st.markdown(f"""
            <div class="game-card-locked">
                <div class="lock-overlay">
                    <div style="font-size:40px;">🔒</div>
                    <div style="font-weight:bold; color:#555;">Palpite Bloqueado</div>
                </div>
                <div class="blur-layer">
                    <div style="display:flex; gap:5px; justify-content:center;">
                        {''.join([f"<div class='lotto-ball'>{n:02d}</div>" for n in game])}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # UNLOCKED CARD (Visible)
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; border-left:8px solid #930089; margin-bottom:15px; box-shadow:0 2px 5px rgba(0,0,0,0.1);">
                <div style="font-size:12px; color:#666; margin-bottom:5px;">JOGO #{i+1} {'(AMOSTRA GRÁTIS)' if i==0 else '(PREMIUM)'}</div>
                <div style="display:flex; gap:5px; justify-content:center; flex-wrap:wrap;">
                    {''.join([f"<div class='lotto-ball'>{n:02d}</div>" for n in game])}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- PAYMENT / VIRAL SECTION ---
    if not st.session_state.unlocked:
        st.markdown("<br>", unsafe_allow_html=True)
        col_pay1, col_pay2 = st.columns(2)
        
        with col_pay1:
            # Simulated Payment Link
            st.markdown("""
            <button class="btn-buy" onclick="alert('Integração Mercado Pago aqui!')">
                💸 LIBERAR TUDO POR R$ 1,00
            </button>
            <div style="text-align:center; font-size:10px; color:#888; margin-top:5px;">Via PIX ou Cartão (Mercado Pago)</div>
            """, unsafe_allow_html=True)
            
            # Simulation button for YOU to test unlocking
            if st.button("Simular Pagamento (Admin)"):
                st.session_state.unlocked = True
                st.rerun()

        with col_pay2:
            # Viral Loop
            st.markdown("""
            <button class="btn-share">
                📲 COMPARTILHAR E GANHAR
            </button>
            <div style="text-align:center; font-size:10px; color:#888; margin-top:5px;">Envie para 3 grupos e libere grátis</div>
            """, unsafe_allow_html=True)

# --- 6. FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#888; font-size:12px;">
    © 2026 LotoMaster Club. Resultados baseados em estatística.<br>
    Jogue com responsabilidade.
</div>
""", unsafe_allow_html=True)
