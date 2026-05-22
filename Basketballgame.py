import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Basketball Game", layout="wide")

st.title("🏀 Mini Basketball Game")

game_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        overflow: hidden;
        background: linear-gradient(to bottom, #87ceeb, #ffffff);
    }

    canvas {
        display: block;
        margin: auto;
        background: #f4a460;
        border: 6px solid black;
        border-radius: 10px;
    }

    h1 {
        text-align: center;
        font-family: Arial;
    }
</style>
</head>

<body>

<canvas id="gameCanvas" width="900" height="500"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let score = 0;

// Ball
let ball = {
    x: 120,
    y: 250,
    radius: 20,
    dx: 0,
    dy: 0,
    gravity: 0.4
};

// Hoop
const hoop = {
    x: 720,
    y: 180,
    width: 80,
    height: 10
};

// Mouse control
let dragging = false;
let startX, startY;

canvas.addEventListener("mousedown", (e) => {
    dragging = true;
    startX = e.offsetX;
    startY = e.offsetY;
});

canvas.addEventListener("mouseup", (e) => {
    if (dragging) {
        let endX = e.offsetX;
        let endY = e.offsetY;

        ball.dx = (startX - endX) / 6;
        ball.dy = (startY - endY) / 6;

        dragging = false;
    }
});

function drawCourt() {
    // Ground
    ctx.fillStyle = "#d2691e";
    ctx.fillRect(0, 400, canvas.width, 100);

    // Hoop pole
    ctx.fillStyle = "black";
    ctx.fillRect(780, 100, 10, 200);

    // Rim
    ctx.fillStyle = "red";
    ctx.fillRect(hoop.x, hoop.y, hoop.width, hoop.height);

    // Net
    ctx.beginPath();
    ctx.moveTo(hoop.x, hoop.y + 10);
    ctx.lineTo(hoop.x + 15, hoop.y + 40);
    ctx.lineTo(hoop.x + 65, hoop.y + 40);
    ctx.lineTo(hoop.x + 80, hoop.y + 10);
    ctx.strokeStyle = "white";
    ctx.stroke();

    // Score
    ctx.fillStyle = "black";
    ctx.font = "30px Arial";
    ctx.fillText("Score: " + score, 30, 50);
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = "orange";
    ctx.fill();
    ctx.strokeStyle = "black";
    ctx.stroke();
}

function updateBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;

    ball.dy += ball.gravity;

    // Floor bounce
    if (ball.y + ball.radius > 400) {
        ball.y = 400 - ball.radius;
        ball.dy *= -0.7;
    }

    // Wall bounce
    if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) {
        ball.dx *= -0.8;
    }

    // Score detection
    if (
        ball.x > hoop.x &&
        ball.x < hoop.x + hoop.width &&
        ball.y > hoop.y &&
        ball.y < hoop.y + 20
    ) {
        score += 1;

        // Reset ball
        ball.x = 120;
        ball.y = 250;
        ball.dx = 0;
        ball.dy = 0;
    }
}

function gameLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawCourt();
    drawBall();
    updateBall();

    requestAnimationFrame(gameLoop);
}

gameLoop();
</script>

</body>
</html>
"""

components.html(game_html, height=550)
