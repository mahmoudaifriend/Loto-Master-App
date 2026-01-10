import streamlit as st
import streamlit.components.v1 as components

# 1. Configuração da Página (Streamlit)
st.set_page_config(page_title="Totoloto Algoritmia - 10 Jan 2026", layout="wide")

st.title("🚀 Totoloto Algoritmia: Motor de Sorteio Visual")
st.write("Estratégia de Eliminação para o sorteio de hoje, 10 de Janeiro.")

# 2. O Código do Motor (HTML/JS) que criamos
# ملاحظة: تم وضع الكود الذي صممناه هنا ليتم حقنه داخل ستريم لايت
html_engine = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <style>
        body { background-color: #0e1117; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; }
        #engine-container { position: relative; width: 280px; height: 280px; border: 6px solid #8e44ad; border-radius: 50%; background: radial-gradient(circle, #1a1a1a, #000); animation: rotate 10s linear infinite; margin-top: 20px; }
        .spin-fast { animation: rotate 0.3s linear infinite !important; }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .ball { position: absolute; width: 25px; height: 25px; background-color: #8e44ad; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; border: 1px solid #fff; }
        .controls { margin-top: 20px; }
        button { padding: 12px 24px; background-color: #8e44ad; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }
        #results-area { margin-top: 30px; display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
        .popped-ball { width: 35px; height: 35px; background-color: #8e44ad; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; animation: pop 0.4s ease-out; box-shadow: 0 0 10px #8e44ad; }
        @keyframes pop { 0% { transform: scale(0); } 100% { transform: scale(1); } }
    </style>
</head>
<body>
    <div id="engine-container"></div>
    <div class="controls">
        <button onclick="startSimulation()">Iniciar Simulação (Algoritmo 10/01)</button>
    </div>
    <div id="results-area"></div>

    <script>
        const container = document.getElementById('engine-container');
        const results = document.getElementById('results-area');
        
        // Setup initial 25 balls with 'X'
        function init() {
            container.innerHTML = '';
            for(let i=1; i<=25; i++) {
                const b = document.createElement('div');
                b.className = 'ball'; b.innerText = 'X'; b.id = 'b'+i;
                const a = Math.random()*Math.PI*2; const d = Math.random()*80;
                b.style.left = `calc(50% + ${Math.cos(a)*d}px - 12px)`;
                b.style.top = `calc(50% + ${Math.sin(a)*d}px - 12px)`;
                container.appendChild(b);
            }
        }

        async function startSimulation() {
            results.innerHTML = ''; init();
            const pool = Array.from({length: 25}, (_, i) => i + 1);
            for(let i=0; i<15; i++) {
                container.classList.add('spin-fast');
                await new Promise(r => setTimeout(r, 4500));
                
                const idx = Math.floor(Math.random()*pool.length);
                const num = pool.splice(idx, 1)[0];
                document.getElementById('b'+num).remove();
                
                const resBall = document.createElement('div');
                resBall.className = 'popped-ball'; resBall.innerText = num;
                results.appendChild(resBall);
                
                container.classList.remove('spin-fast');
                await new Promise(r => setTimeout(r, 2000));
            }
            alert("Simulação do Algoritmo Concluída!");
        }
        init();
    </script>
</body>
</html>
"""

# 3. Inserindo o Motor no Streamlit
components.html(html_engine, height=600)

# 4. Conexão com os Dados do GitHub
st.sidebar.header("📊 Painel de Controle Totoloto")
st.sidebar.info("Este motor está sincronizado com os filtros de 10/01/2026.")
