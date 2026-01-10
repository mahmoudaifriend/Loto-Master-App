<!DOCTYPE html>
<html lang="pt-br" dir="ltr">
<head>
    <meta charset="UTF-8">
    <title>Simulador Lotofácil - Mahmoud</title>
    <style>
        /* Basic body styles for centering and dark theme */
        body { background-color: #1a1a1a; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; overflow-x: hidden; }
        
        /* The circular engine container style */
        #engine-container { position: relative; width: 300px; height: 300px; border: 8px solid #444; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, #333, #000); box-shadow: 0 0 30px rgba(0,0,0,0.5); transition: transform 0.5s ease; }
        
        /* Spinning animations states */
        .spin-slow { animation: rotate 10s linear infinite; }
        .spin-fast { animation: rotate 0.3s linear infinite; }
        
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

        /* Styles for the balls inside the engine */
        .ball { position: absolute; width: 30px; height: 30px; background-color: #8e44ad; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; border: 2px solid #5e3370; color: white; box-shadow: inset -2px -2px 5px rgba(0,0,0,0.5); }

        /* Control panel area */
        .controls { margin-top: 30px; text-align: center; z-index: 10; }
        input { padding: 10px; border-radius: 5px; border: none; width: 60px; text-align: center; font-size: 18px; }
        button { padding: 10px 25px; border-radius: 5px; border: none; background-color: #8e44ad; color: white; cursor: pointer; font-size: 18px; font-weight: bold; transition: 0.3s; }
        button:hover { background-color: #9b59b6; transform: scale(1.05); }
        button:disabled { background-color: #555; cursor: not-allowed; }

        /* Area where drawn balls appear */
        #results-area { margin-top: 40px; display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; max-width: 600px; min-height: 50px; }
        
        /* Style and animation for the popped-out balls */
        .popped-ball { width: 40px; height: 40px; background-color: #8e44ad; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; animation: pop-up 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }

        @keyframes pop-up { 0% { transform: scale(0); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    </style>
</head>
<body>

    <h1>Motor de Sorteio Lotofácil 🎰</h1>

    <div id="engine-container" class="spin-slow">
        </div>

    <div class="controls">
        <label>Quantidade de bolas a sortear (1-25): </label>
        <input type="number" id="rounds" value="15" min="1" max="25">
        <br><br>
        <button id="simulateBtn" onclick="startSimulation()">Iniciar Simulação</button>
    </div>

    <div id="results-area" id="results"></div>

    <script>
        const engine = document.getElementById('engine-container');
        const resultsArea = document.getElementById('results-area');
        const simulateBtn = document.getElementById('simulateBtn');
        const ballsCount = 25;

        // Function to create the initial 25 balls inside the engine with 'X'
        function createInitialBalls() {
            engine.innerHTML = '';
            for (let i = 1; i <= ballsCount; i++) {
                const ball = document.createElement('div');
                ball.className = 'ball';
                ball.innerText = 'X';
                ball.id = 'ball-' + i;
                
                // Random distribution of balls inside the circle boundary
                const angle = Math.random() * Math.PI * 2;
                const dist = Math.random() * 100; // Keep within radius
                ball.style.left = `calc(50% + ${Math.cos(angle) * dist}px - 15px)`;
                ball.style.top = `calc(50% + ${Math.sin(angle) * dist}px - 15px)`;
                
                engine.appendChild(ball);
            }
        }

        // Main async function to handle the simulation flow
        async function startSimulation() {
            const rounds = parseInt(document.getElementById('rounds').value);
            // Validation alert in Portuguese
            if (rounds < 1 || rounds > 25) return alert("Por favor, escolha um número entre 1 e 25.");

            simulateBtn.disabled = true;
            resultsArea.innerHTML = '';
            createInitialBalls();

            // Create an array of available numbers [1...25]
            const availableBalls = Array.from({length: 25}, (_, i) => i + 1);

            for (let i = 0; i < rounds; i++) {
                // 1. Speed up the engine (High RPM state)
                engine.className = 'spin-fast';
                
                // Wait for 4.5 seconds while spinning fast
                await new Promise(r => setTimeout(r, 4500));

                // 2. Remove a ball randomly from the engine visually and logically
                const randomIndex = Math.floor(Math.random() * availableBalls.length);
                // Get the actual number and remove from array
                const ballNum = availableBalls.splice(randomIndex, 1)[0]; 
                // Remove the visual 'X' ball from inside the engine
                const ballElement = document.getElementById('ball-' + ballNum);
                if (ballElement) ballElement.remove();

                // 3. Pop up the ball in the results area with the actual number
                const poppedBall = document.createElement('div');
                poppedBall.className = 'popped-ball';
                poppedBall.innerText = ballNum; 
                resultsArea.appendChild(poppedBall);

                // 4. Slow down the engine for 2 seconds (Idle state)
                engine.className = 'spin-slow';
                await new Promise(r => setTimeout(r, 2000));
            }

            simulateBtn.disabled = false;
            // Final alert in Portuguese
            alert("Simulação concluída!");
        }

        // Initial setup on page load
        createInitialBalls();
    </script>
</body>
</html>
