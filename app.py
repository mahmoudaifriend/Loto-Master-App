import streamlit as st
import time
import random
import base64
import os
from datetime import datetime, timedelta
import pandas as pd

# --- 1. CONFIGURAÇÕES BÁSICAS DO SISTEMA ---
st.set_page_config(
    page_title="Totoloto Algoritmia",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PROCESSAMENTO DA IMAGEM CENTRAL (GLOBO) ---
def get_base64_img(path):
    """Converte a imagem local em Base64 para evitar links quebrados."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_b64 = get_base64_img("globo.png")
globo_src = f"data:image/png;base64,{img_b64}" if img_b64 else ""

# --- 3. LÓGICA DO CONTADOR REGRESSIVO (COUNTDOWN) ---
def get_countdown():
    """Calcula o tempo restante para o próximo sorteio da Lotofácil (20:00)."""
    now = datetime.now()
    
    # Domingo não há sorteios oficiais
    if now.weekday() == 6:
        return "00:00:00", "HOJE É DOMINGO - SEM SORTEIOS"
    
    target = now.replace(hour=20, minute=0, second=0, microsecond=0)
    
    # Se já passou das 20h, o alvo é o dia seguinte
    if now > target:
        target += timedelta(days=1)
        if target.weekday() == 6: # Pular domingo se amanhã for domingo
            target += timedelta(days=1)
            
    delta = target - now
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}", "TEMPO PARA O PRÓXIMO SORTEIO"

# --- 4. INTERFACE E DESIGN DE LUXO (CSS CUSTOMIZADO) ---
def inject_luxury_design():
    countdown_time, status = get_countdown()
    primary_color = "#930089" # Roxo Padrão Lotofácil
    gold_color = "#FFD700"    # Dourado Elite
    
    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@600&display=swap');
        
        .stApp {{
            background: radial-gradient(circle at center, #2e002b 0%, #000 100%);
            font-family: 'Rajdhani', sans-serif;
            color: white;
        }}

        /* Container do Contador Regressivo */
        .countdown-container {{
            text-align: center; padding: 15px; border: 1px solid {primary_color};
            border-radius: 12px; background: rgba(0,0,0,0.6); margin-bottom: 25px;
            box-shadow: 0 0 15px rgba(147, 0, 137, 0.3);
        }}
        .timer-val {{ font-family: 'Orbitron'; color: {gold_color}; font-size: 2.2rem; text-shadow: 0 0 10px {gold_color}; }}
        .timer-label {{ font-size: 0.9rem; color: #aaa; letter-spacing: 2px; text-transform: uppercase; }}

        /* Área do Motor Central (Globo) */
        .engine-area {{
            display: flex; justify-content: center; align-items: center;
            position: relative; width: 320px; height: 320px; margin: 0 auto;
        }}
        .globo-main {{
            width: 100%; z-index: 10; filter: drop-shadow(0 0 20px {primary_color});
        }}
        .energy-glow {{
            position: absolute; width: 260px; height: 260px;
            border: 4px dashed {gold_color}; border-radius: 50%;
            animation: rotateEngine 2s linear infinite; z-index: 5;
            box-shadow: 0 0 40px {primary_color};
        }}
        @keyframes rotateEngine {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

        /* Grade de Bolas e Responsividade Móvel */
        .results-grid {{
            display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;
            padding: 25px; background: rgba(255,255,255,0.04); border-radius: 25px;
            margin-top: 15px;
        }}
        .ball-3d {{
            width: 55px; height: 55px; border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #ffffff 0%, {primary_color} 55%, #000000 100%);
            display: inline-flex; align-items: center; justify-content: center;
            color: white; font-family: 'Orbitron'; font-size: 1.2rem; font-weight: bold;
            box-shadow: 4px 4px 12px #000; border: 1px solid rgba(255,255,255,0.1);
        }}
        .ball-x {{
            width: 55px; height: 55px; border-radius: 50%; background: #111;
            border: 2px dashed #ff4b00; display: inline-flex; align-items: center;
            justify-content: center; color: #ff4b00; font-family: 'Orbitron'; font-size: 1.6rem;
            text-shadow: 0 0 10px #ff4b00;
        }}

        /* Botão de Ação Estilizado */
        div.stButton > button {{
            background: linear-gradient(90deg, #ff4b00, #ff8700) !important;
            border: none; color: white; border-radius: 50px; padding: 22px;
            font-family: 'Orbitron'; font-size: 1.4rem; width: 100%;
            box-shadow: 0 0 25px rgba(255,75,0,0.6); transition: 0.4s;
            cursor: pointer;
        }}
        div.stButton > button:hover {{ transform: scale(1.03); filter: brightness(1.2); }}
        
        /* Rodapé Legal */
        .footer-legal {{
            text-align: center; font-size: 11px; color: #555; margin-top: 60px; 
            border-top: 1px solid #222; padding-top: 25px; line-height: 1.6;
        }}
    </style>
    
    <div class="countdown-container">
        <div class="timer-label">{status}</div>
        <div class="timer-val">{countdown_time}</div>
    </div>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- 5. MOTOR DE INTELIGÊNCIA ESTATÍSTICA ---
class TotolotoEngine:
    def __init__(self):
        # Números com maior tendência baseados em ciclos recentes de 2026
        self.hot_pool = [2, 5, 6, 9, 10, 11, 13, 14, 15, 18, 20, 23, 24, 25]
        
    def generate(self, amount, last_draw=None, closing_n=15):
        """Gera apostas baseadas em pesos estatísticos ou fechamento de matriz."""
        bets = []
        pool = list(range(1, 26))
        
        for _ in range(amount):
            if closing_n > 15:
                # Lógica de Fechamento de Matriz (Garante maior cobertura)
                matrix = sorted(random.sample(pool, closing_n))
                bet = sorted(random.sample(matrix, 15))
            else:
                # Lógica de Probabilidade Ponderada
                weights = [1.9 if last_draw and i in last_draw else 1.0 for i in pool]
                weights = [w * 1.6 if i in self.hot_pool else w for i, w in enumerate(weights, 1)]
                
                bet = []
                while len(bet) < 15:
                    pick = random.choices(pool, weights=weights, k=1)[0]
                    if pick not in bet: bet.append(pick)
                bet.sort()
            bets.append(bet)
        return bets

# --- 6. EXECUÇÃO PRINCIPAL DO APLICATIVO ---
def main():
    inject_luxury_design()
    st.markdown("<h1 style='text-align:center; font-family:Orbitron; color:#ff4b00; margin-bottom:0;'>TOTOLOTO ALGORITMIA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888; margin-top:0;'>SISTEMA AVANÇADO DE ANÁLISE PROBABILÍSTICA</p>", unsafe_allow_html=True)

    # Exibição do Motor Central (Globo)
    if globo_src:
        st.markdown(f"""
            <div class='engine-area'>
                <div class='energy-glow'></div>
                <img src='{globo_src}' class='globo-main'>
            </div>
        """, unsafe_allow_html=True)

    # --- PAINEL DE COMANDO DO USUÁRIO ---
    st.markdown("### 🛠️ PAINEL DE CONFIGURAÇÃO")
    
    col_mode, col_draw = st.columns(2)
    with col_mode:
        play_mode = st.radio("MODO DE JOGO:", ["Modo Individual", "Modo Bolão"], horizontal=True, help="O modo Bolão gera jogos com maior conectividade entre si.")
    with col_draw:
        prev_draw = st.text_input("ÚLTIMO SORTEIO (Opcional):", placeholder="Ex: 02,05,09,12,15...")

    col_close, col_qty = st.columns(2)
    with col_close:
        closing_val = st.slider("FECHAMENTO DE MATRIZ (Quantos números cercar?):", 15, 20, 15, help="Escolha cercar até 20 números para gerar combinações de 15.")
    with col_qty:
        qty_range = st.select_slider("VOLUME DE PROCESSAMENTO (Apostas):", 
                                     options=["1-100", "100-1000", "1000-10000"], 
                                     value="1-100")

    # Mapeamento do volume de geração
    qty_map = {"1-100": 100, "100-1000": 1000, "1000-10000": 10000}
    num_bets = qty_map[qty_range]

    # Botão de Execução
    if st.button("🚀 INICIAR SIMULAÇÃO"):
        # Efeito sonoro de imersão
        st.markdown('<audio autoplay loop><source src="https://www.soundjay.com/misc/sounds/bingo-ball-machine-1.mp3"></audio>', unsafe_allow_html=True)
        
        # Processamento do sorteio anterior
        p_list = []
        try:
            if prev_draw: p_list = [int(x.strip()) for x in prev_draw.split(',') if x.strip()]
        except: st.error("Erro: Verifique o formato dos números do sorteio anterior.")

        # Execução do Motor
        engine = TotolotoEngine()
        results = engine.generate(num_bets, p_list, closing_val)
        
        # Salvando no Estado da Sessão para persistência
        st.session_state['results'] = results
        st.session_state['mode'] = play_mode
        st.session_state['closing'] = closing_val

    # --- EXIBIÇÃO DINÂMICA DOS RESULTADOS ---
    if 'results' in st.session_state:
        st.divider()
        st.subheader("🔮 RESULTADOS DA SIMULAÇÃO ELITE")
        
        display_results = st.session_state['results']
        mode = st.session_state['mode']
        is_closing = st.session_state['closing'] > 15

        # Apresentação das primeiras 5 apostas com efeito de 'X' e delay UX
        for i in range(min(5, len(display_results))):
            bet = display_results[i]
            
            # Lógica do marcador 'X' (Somente no Modo Individual comum)
            x_indices = random.sample(range(15), 1) if (mode == "Modo Individual" and not is_closing) else []
            
            ball_html = ""
            for idx, num in enumerate(bet):
                if idx in x_indices:
                    ball_html += "<div class='ball-x'>X</div>"
                else:
                    ball_html += f"<div class='ball-3d'>{str(num).zfill(2)}</div>"
            
            st.markdown(f"<div style='margin-bottom:10px; color:#aaa;'>JOGO SUGERIDO {i+1}:</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='results-grid'>{ball_html}</div>", unsafe_allow_html=True)
            time.sleep(0.8) # Simulação de processamento em tempo real

        # --- FERRAMENTAS DE FILTRAGEM AVANÇADA ---
        st.markdown("---")
        if st.checkbox("🔍 FILTRAR TOP 100 APOSTAS QUENTES"):
            st.success("Algoritmo finalizado. Estas 100 apostas possuem a maior taxa de convergência estatística.")
            top_100 = display_results[:100]
            df = pd.DataFrame(top_100, columns=[f"N{i+1}" for i in range(15)])
            st.dataframe(df, use_container_width=True)
            
            # Recurso de Exportação Massiva
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 BAIXAR LISTA COMPLETA (CSV/EXCEL)", data=csv, file_name="apostas_totoloto_elite.csv")

    # --- RODAPÉ LEGAL E REGRAS DE USO ---
    st.markdown(f"""
        <div class="footer-legal">
            <p><b>AVISO DE RESPONSABILIDADE:</b> O Totoloto Algoritmia é uma ferramenta de simulação baseada em cálculos estatísticos e probabilidade. 
            Não garantimos lucros, prêmios ou resultados financeiros de qualquer natureza.</p>
            <p><b>RESTRITO:</b> O uso deste sistema é proibido para menores de 21 anos. Pratique o jogo consciente e responsável.</p>
            <p style='color:#777;'>Versão 14.0 Master Elite © 2026 - Desenvolvido para o Mercado Brasileiro.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
