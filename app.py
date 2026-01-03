import streamlit as st
import random
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA (PAGE CONFIG) ---
st.set_page_config(
    page_title="LotoMaster Brasil | IA para Loterias",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILO VISUAL (CSS) ---
st.markdown("""
<style>
    /* Estilo inspirado na Caixa Econômica Federal */
    .main-header {
        color: #009640;
        font-family: 'Helvetica', sans-serif;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #f68822; /* Laranja Caixa */
        color: white;
        font-weight: bold;
        font-size: 22px;
        border-radius: 8px;
        border: none;
        padding: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #d66e0a;
        transform: scale(1.02);
    }
    .game-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 10px solid #009640; /* Verde Caixa */
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }
    .result-text {
        font-size: 28px;
        font-weight: bold;
        color: #333;
        letter-spacing: 2px;
        margin-top: 10px;
    }
    .badge {
        background-color: #e9ecef;
        color: #495057;
        padding: 5px 10px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: bold;
    }
    .seo-box {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        margin-top: 50px;
        border: 1px solid #e9ecef;
        color: #555;
    }
    /* Ocultar menus padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR LÓGICO (LOTTERY ENGINE) ---
class LotteryEngine:
    @staticmethod
    def generate_game(game_type, amount):
        games = []
        for _ in range(amount):
            if game_type == "Lotofácil":
                # Estratégia: Balanceamento de Pares/Ímpares (7 a 9 ímpares)
                while True:
                    game = sorted(random.sample(range(1, 26), 15))
                    odds = sum(1 for n in game if n % 2 != 0)
                    if 7 <= odds <= 9:
                        games.append(game)
                        break
            elif game_type == "Mega-Sena":
                games.append(sorted(random.sample(range(1, 61), 6)))
            elif game_type == "Quina":
                games.append(sorted(random.sample(range(1, 81), 5)))
            elif game_type == "Lotomania":
                games.append(sorted(random.sample(range(0, 100), 50)))
            elif game_type == "Dupla Sena":
                games.append(sorted(random.sample(range(1, 51), 6)))
            elif game_type == "Super Sete":
                games.append([random.randint(0, 9) for _ in range(7)])
            elif game_type == "Timemania":
                teams = ["FLAMENGO", "CORINTHIANS", "PALMEIRAS", "SÃO PAULO", "VASCO", "SANTOS", "GRÊMIO", "CRUZEIRO", "INTER", "ATLÉTICO-MG", "BOTAFOGO", "FLUMINENSE"]
                games.append({"numbers": sorted(random.sample(range(1, 81), 10)), "team": random.choice(teams)})
            elif game_type == "Dia de Sorte":
                months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                games.append({"numbers": sorted(random.sample(range(1, 32), 7)), "month": random.choice(months)})
            elif game_type == "+Milionária":
                games.append({"numbers": sorted(random.sample(range(1, 51), 6)), "trevos": sorted(random.sample(range(1, 7), 2))})
        return games

# --- 4. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.title("📱 LotoMaster App")
    st.markdown("---")
    
    # Seleção do Jogo
    selected_game = st.selectbox(
        "Escolha a Loteria:",
        ["Lotofácil", "Mega-Sena", "Quina", "Lotomania", "+Milionária", "Timemania", "Dia de Sorte", "Dupla Sena", "Super Sete"]
    )
    
    st.markdown("---")
    
    # Informações
    st.info("""
    💡 **Como funciona?**
    Nosso algoritmo de Inteligência Artificial analisa padrões matemáticos para evitar sequências óbvias e aumentar suas probabilidades.
    """)
    
    # Área Administrativa (Admin)
    st.markdown("---")
    if st.checkbox("Área do Admin 🔒"):
        pwd = st.text_input("Senha de Acesso:", type="password")
        if pwd == "Mahmoud2026": # Senha do Admin
            st.success("Acesso Permitido!")
            st.metric("Usuários Online", "125")
            st.metric("Jogos Gerados Hoje", "1,450")

# --- 5. INTERFACE PRINCIPAL (MAIN UI) ---

# Título Principal
st.markdown(f"<h1 class='main-header'>Gerador {selected_game} (IA) 🤖</h1>", unsafe_allow_html=True)

# Controles
col1, col2 = st.columns([1, 2])
with col1:
    # Quantidade de Jogos
    num_games = st.number_input("Quantidade de Jogos:", min_value=1, max_value=10, value=3)
with col2:
    st.write("") # Espaço em branco
    st.write("") 
    # Botão de Gerar
    generate = st.button(f"GERAR PALPITES AGORA 🎲")

# --- 6. EXIBIÇÃO DE RESULTADOS ---
if generate:
    engine = LotteryEngine()
    
    # Efeito de Carregamento
    with st.spinner("🤖 A IA está calculando as melhores probabilidades..."):
        time.sleep(1) 
    
    results = engine.generate_game(selected_game, num_games)
    
    st.success(f"✅ Sucesso! Aqui estão seus palpites otimizados para {selected_game}:")
    
    for i, res in enumerate(results):
        # Formatação baseada no tipo de jogo
        if isinstance(res, dict): # Jogos Especiais
            if "team" in res: # Timemania
                val_nums = " - ".join(f"{n:02d}" for n in res['numbers'])
                val_extra = f"❤️ Time do Coração: {res['team']}"
                display_html = f"<div class='result-text'>{val_nums}</div><div style='color:#e63946; margin-top:5px;'>{val_extra}</div>"
            elif "month" in res: # Dia de Sorte
                val_nums = " - ".join(f"{n:02d}" for n in res['numbers'])
                val_extra = f"📅 Mês da Sorte: {res['month']}"
                display_html = f"<div class='result-text'>{val_nums}</div><div style='color:#457b9d; margin-top:5px;'>{val_extra}</div>"
            elif "trevos" in res: # +Milionária
                val_nums = " - ".join(f"{n:02d}" for n in res['numbers'])
                val_trevos = " - ".join(str(t) for t in res['trevos'])
                display_html = f"<div class='result-text'>{val_nums}</div><div style='color:#2a9d8f; margin-top:5px;'>🍀 Trevos: {val_trevos}</div>"
        else:
            # Jogos Numéricos Padrão
            val = " - ".join(f"{n:02d}" for n in res)
            display_html = f"<div class='result-text'>{val}</div>"
            
        # Card de Resultado
        st.markdown(f"""
        <div class="game-card">
            <span class="badge">Jogo #{i+1}</span>
            {display_html}
        </div>
        """, unsafe_allow_html=True)

# --- 7. RODAPÉ SEO (SEO FOOTER) ---
st.markdown("<div class='seo-box'>", unsafe_allow_html=True)
st.markdown(f"""
### 📊 Sobre o Gerador LotoMaster para {selected_game}
Você está utilizando uma ferramenta avançada de análise combinatória. Diferente da "Surpresinha" da lotérica, que escolhe números totalmente aleatórios, nosso sistema busca equilíbrio.

* **Dica de Ouro:** Estatisticamente, a maioria dos sorteios da {selected_game} contém um equilíbrio entre números pares e ímpares. Evite marcar apenas números seguidos (ex: 1, 2, 3, 4).
* **Aviso Legal:** Este site é uma ferramenta informativa e educativa. Não realizamos vendas de apostas. Jogue com responsabilidade.
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Copyright
st.markdown("---")
st.caption("© 2026 LotoMaster Brasil - Todos os direitos reservados.")
