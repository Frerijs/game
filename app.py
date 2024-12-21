import streamlit as st
import streamlit.components.v1 as components

# Iestatīt lapas virsrakstu un izskatu
st.set_page_config(page_title="🦖 Dino Runner", layout="centered")

st.title("🦖 Dino Runner ar Streamlit")

st.write("""
Spēlē Dino Runner spēli tieši šeit! Nospied Space taustiņu vai Augšējo bultiņu, lai vadītu T-Rex un izvairītos no šķēršļiem.
""")

# HTML un JavaScript Dino Runner kods
dino_game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dino Runner</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #f0f0f0;
        }
        canvas {
            display: block;
            margin: 0 auto;
            background-color: #ffffff;
            border: 2px solid #000000;
        }
        #score {
            position: absolute;
            top: 10px;
            left: 10px;
            font-size: 24px;
            color: #333333;
            font-family: Arial, sans-serif;
        }
        #gameOver {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border: 2px solid #555555;
            text-align: center;
            display: none;
            font-family: Arial, sans-serif;
        }
        #restartButton {
            padding: 10px 20px;
            font-size: 18px;
            margin-top: 10px;
            cursor: pointer;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
        }
        #restartButton:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div id="score">Score: 0</div>
    <canvas id="gameCanvas" width="800" height="400"></canvas>
    <div id="gameOver">
        <h1>Game Over!</h1>
        <p>Your Score: <span id="finalScore">0</span></p>
        <button id="restartButton">Restart Game</button>
    </div>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreDisplay = document.getElementById('score');
        const gameOverDisplay = document.getElementById('gameOver');
        const finalScoreDisplay = document.getElementById('finalScore');
        const restartButton = document.getElementById('restartButton');

        // Spēles iestatījumi
        const gravity = 0.6;
        const jumpStrength = -12;
        let gameSpeed = 5;
        let score = 0;
        let gameOver = false;

        // Dinas objektu
        const dino = {
            x: 50,
            y: 300,
            width: 40,
            height: 60,
            dy: 0,
            jumping: false,
            color: 'green'
        };

        // Šķēršļu masīvs
        const obstacles = [];

        // Šķēršļu iestatījumi
        const obstacleFrequency = 1500; // milisekundes
        const obstacleWidth = 20;
        const obstacleHeight = 40;
        const obstacleColor = 'red';

        // Laika kontrole
        let lastObstacleTime = Date.now();

        // Spēles sākšana
        function startGame() {
            document.addEventListener('keydown', handleKeyDown);
            requestAnimationFrame(gameLoop);
        }

        // Vadība
        function handleKeyDown(e) {
            if ((e.code === 'Space' || e.code === 'ArrowUp') && !dino.jumping) {
                dino.dy = jumpStrength;
                dino.jumping = true;
            }
        }

        // Šķēršļu ģenerēšana
        function spawnObstacle() {
            const obstacle = {
                x: canvas.width,
                y: 300,
                width: obstacleWidth,
                height: obstacleHeight,
                color: obstacleColor
            };
            obstacles.push(obstacle);
        }

        // Saskarsme pārbaude
        function checkCollision(dino, obstacle) {
            return (
                dino.x < obstacle.x + obstacle.width &&
                dino.x + dino.width > obstacle.x &&
                dino.y < obstacle.y + obstacle.height &&
                dino.y + dino.height > obstacle.y
            );
        }

        // Spēles cikls
        function gameLoop() {
            if (gameOver) {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                gameOverDisplay.style.display = 'block';
                finalScoreDisplay.textContent = score;
                return;
            }

            // Fona atjaunošana
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Dinas kustība
            dino.dy += gravity;
            dino.y += dino.dy;

            if (dino.y + dino.height >= 300) {
                dino.y = 300 - dino.height;
                dino.dy = 0;
                dino.jumping = false;
            }

            // Dinas zīmēšana
            ctx.fillStyle = dino.color;
            ctx.fillRect(dino.x, dino.y, dino.width, dino.height);

            // Šķēršļu kustība un zīmēšana
            for (let i = 0; i < obstacles.length; i++) {
                const obstacle = obstacles[i];
                obstacle.x -= gameSpeed;
                ctx.fillStyle = obstacle.color;
                ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);

                // Saskarsme
                if (checkCollision(dino, obstacle)) {
                    gameOver = true;
                }

                // Punktu palielināšana, kad šķērslis iziet no ekrāna
                if (obstacle.x + obstacle.width < 0) {
                    obstacles.splice(i, 1);
                    i--;
                    score++;
                    scoreDisplay.textContent = `Score: ${score}`;
                }
            }

            // Šķēršļu ģenerēšana
            const currentTime = Date.now();
            if (currentTime - lastObstacleTime > obstacleFrequency) {
                spawnObstacle();
                lastObstacleTime = currentTime;
            }

            // Spēles ātruma palielināšana pakāpeniski
            if (score % 5 === 0 && score !== 0) {
                gameSpeed += 0.5;
            }

            requestAnimationFrame(gameLoop);
        }

        // Restartēšana
        restartButton.addEventListener('click', () => {
            // Resetē spēles stāvokli
            obstacles.length = 0;
            gameSpeed = 5;
            score = 0;
            gameOver = false;
            scoreDisplay.textContent = `Score: ${score}`;
            gameOverDisplay.style.display = 'none';
            dino.y = 300 - dino.height;
            dino.dy = 0;
            dino.jumping = false;
            requestAnimationFrame(gameLoop);
        });

        startGame();
    </script>
</body>
</html>
"""

# Iebūvē Dino Runner spēli ar HTML un JavaScript
components.html(dino_game_html, height=420)
