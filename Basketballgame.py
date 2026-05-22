import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Basketball Game", layout="wide")

st.title("🏀 Basketball Shooter Game")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        overflow: hidden;
        background: #87CEEB;
    }

    canvas {
        background: #f4a460;
        display: block;
        margin: auto;
        border: 5px solid black;
        border-radius: 10px;
    }
</style>
</head>

<body>

<canvas id="gameCanvas" width="1000" height="550"></canvas>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// =========================
// PLAYER
// =========================
const player = {
    x: 100,
    y: 380,
    width: 50,
    height: 90,
    speed: 6
};

// =========================
// BALL
// =========================
const ball = {
    x: player.x + 25,
    y: player.y,
    radius: 15,
    dx: 0,
    dy: 0,
    gravity: 0.4,
    shooting: false
};

// =========================
// HOOP
// =========================
const hoop = {
    x: 820,
    y: 200,
    width: 80,
    height: 10
};

let score = 0;

// =========================
// CONTROLS
// =========================
const keys = {};

document.addEventListener("keydown", (e) => {
    keys[e.code] = true;
});

document.addEventListener("keyup", (e) => {
    keys[e.code] = false;

    // SHOOT
    if (e.code === "Space" && !ball.shooting) {
        ball.shooting = true;

        // Power based on player direction
        ball.dx = 10;
        ball.dy = -12;
    }
});

// =========================
// DRAW FUNCTIONS
// =========================
function drawPlayer() {
    // Body
    ctx.fillStyle = "blue";
    ctx.fillRect(player.x, player.y, player.width, player.height);

    // Head
    ctx.beginPath();
    ctx.arc(player.x + 25, player.y - 20, 20, 0, Math.PI * 2);
    ctx.fillStyle = "#f5cfa0";
    ctx.fill();

    // Legs
    ctx.strokeStyle = "black";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.moveTo(player.x + 15, player.y + 90);
    ctx.lineTo(player.x + 10, player.y + 120);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(player.x + 35, player.y + 90);
    ctx.lineTo(player.x + 40, player.y + 120);
    ctx.stroke();
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = "orange";
    ctx.fill();

    ctx.strokeStyle = "black";
    ctx.stroke();
}

function drawCourt() {
    // Floor
    ctx.fillStyle = "#d2691e";
    ctx.fillRect(0, 470, canvas.width, 80);

    // Hoop pole
    ctx.fillStyle = "black";
    ctx.fillRect(900, 120, 10, 250);

    // Rim
    ctx.fillStyle = "red";
    ctx.fillRect(hoop.x, hoop.y, hoop.width, hoop.height);

    // Backboard
    ctx.fillStyle = "white";
    ctx.fillRect(890, 140, 10, 100);

    // Score
    ctx.fillStyle = "black";
    ctx.font = "32px Arial";
    ctx.fillText("Score: " + score, 30, 50);

    // Instructions
    ctx.font = "22px Arial";
    ctx.fillText("Move: A/D or Arrow Keys | Hold Space to Shoot", 30, 90);
}

// =========================
// MOVEMENT
// =========================
let shootPower = 0;
let charging = false;

function updatePlayer() {

    if (keys["ArrowLeft"] || keys["KeyA"]) {
        player.x -= player.speed;
    }

    if (keys["ArrowRight"] || keys["KeyD"]) {
        player.x += player.speed;
    }

    // Keep in bounds
    if (player.x < 0) player.x = 0;
    if (player.x + player.width > canvas.width)
        player.x = canvas.width - player.width;

    // Hold ball if not shooting
    if (!ball.shooting) {
        ball.x = player.x + 55;
        ball.y = player.y + 20;
    }

    // Charge shot
    if (keys["Space"]) {
        charging = true;

        if (shootPower < 20) {
            shootPower += 0.3;
        }
    }
}

// =========================
// SHOOTING
// =========================
document.addEventListener("keyup", (e) => {

    if (e.code === "Space" && !ball.shooting) {

        ball.shooting = true;

        ball.dx = shootPower;
        ball.dy = -shootPower;

        shootPower = 0;
        charging = false;
    }
});

function updateBall() {

    if (ball.shooting) {

        ball.x += ball.dx;
        ball.y += ball.dy;

        ball.dy += ball.gravity;

        // Bounce floor
        if (ball.y + ball.radius > 470) {
            ball.y = 470 - ball.radius;
            ball.dy *= -0.7;
        }

        // Wall bounce
        if (ball.x + ball.radius > canvas.width ||
            ball.x - ball.radius < 0) {
            ball.dx *= -0.8;
        }

        // Score
        if (
            ball.x > hoop.x &&
            ball.x < hoop.x + hoop.width &&
            ball.y > hoop.y &&
            ball.y < hoop.y + 20
        ) {

            score += 1;

            resetBall();
        }

        // Reset if ball falls away
        if (ball.y > canvas.height + 100) {
            resetBall();
        }
    }
}

function resetBall() {
    ball.shooting = false;
    ball.dx = 0;
    ball.dy = 0;
}

// =========================
// GAME LOOP
// =========================
function gameLoop() {

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawCourt();
    drawPlayer();
    drawBall();

    updatePlayer();
    updateBall();

    // Power bar
    if (charging) {
        ctx.fillStyle = "green";
        ctx.fillRect(30, 110, shootPower * 10, 20);

        ctx.strokeStyle = "black";
        ctx.strokeRect(30, 110, 200, 20);
    }

    requestAnimationFrame(gameLoop);
}

gameLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=600)
