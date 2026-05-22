import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cross Platform Basketball", layout="wide")

st.title("🏀 Cross-Platform 2D Basketball (PC + Mobile)")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {
    margin: 0;
    overflow: hidden;
    font-family: Arial;
}

canvas {
    background: #87CEEB;
    display: block;
}

/* UI */
#ui {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(0,0,0,0.5);
    color: white;
    padding: 10px;
    border-radius: 10px;
}

/* MOBILE CONTROLS */
#controls {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 10px;
}

button {
    font-size: 18px;
    padding: 14px;
    border-radius: 12px;
    border: none;
    background: #222;
    color: white;
}
</style>
</head>

<body>

<div id="ui">Score: <span id="score">0</span></div>

<div id="controls">
<button onclick="press('left')">⬅️</button>
<button onclick="press('right')">➡️</button>
<button onclick="press('shoot')">🏀 SHOOT</button>
</div>

<canvas id="game" width="1200" height="600"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// =====================
// GAME STATE
// =====================

let score = 0;

const player = {
    x: 100,
    y: 450,
    w: 40,
    h: 80,
    speed: 7,
    holding: true
};

const ball = {
    x: 0,
    y: 0,
    r: 12,
    dx: 0,
    dy: 0,
    gravity: 0.5,
    moving: false
};

const hoop = {
    x: 1000,
    y: 200,
    w: 80,
    h: 10
};

const backboard = {
    x: 1080,
    y: 150,
    w: 15,
    h: 140
};

// =====================
// INPUT SYSTEM (UNIFIED)
// =====================

let keys = {};

// keyboard (PC)
document.addEventListener("keydown",(e)=>{
    keys[e.code] = true;

    if(e.code === "Space"){
        shoot();
    }
});

document.addEventListener("keyup",(e)=>{
    keys[e.code] = false;
});

// mobile buttons
function press(action){

    if(action === "left") player.x -= player.speed;
    if(action === "right") player.x += player.speed;
    if(action === "shoot") shoot();
}

// =====================
// SHOOT
// =====================

function shoot(){
    if(!player.holding) return;

    player.holding = false;
    ball.moving = true;

    ball.dx = 10;
    ball.dy = -13;
}

// =====================
// PICKUP
// =====================

function pickup(){

    let dx = ball.x - player.x;
    let dy = ball.y - player.y;

    let dist = Math.sqrt(dx*dx + dy*dy);

    if(dist < 60){
        player.holding = true;
        ball.moving = false;
    }
}

// =====================
// RESET
// =====================

function resetBall(){
    player.holding = true;
    ball.moving = false;
    ball.dx = 0;
    ball.dy = 0;
}

// =====================
// UPDATE PLAYER
// =====================

function updatePlayer(){

    // PC MOVEMENT
    if(keys["KeyA"] || keys["ArrowLeft"]) player.x -= player.speed;
    if(keys["KeyD"] || keys["ArrowRight"]) player.x += player.speed;

    player.x = Math.max(0, Math.min(canvas.width - player.w, player.x));

    // BALL FOLLOW HAND
    if(player.holding){
        ball.x = player.x + 20;
        ball.y = player.y;
    } else {
        pickup();
    }
}

// =====================
// UPDATE BALL
// =====================

function updateBall(){

    if(!ball.moving) return;

    ball.x += ball.dx;
    ball.y += ball.dy;

    ball.dy += ball.gravity;

    // floor
    if(ball.y > canvas.height - 20){
        resetBall();
    }

    // backboard bounce
    if(
        ball.x > backboard.x &&
        ball.x < backboard.x + backboard.w &&
        ball.y > backboard.y &&
        ball.y < backboard.y + backboard.h
    ){
        ball.dx *= -0.8;
    }

    // SCORE
    if(
        ball.x > hoop.x &&
        ball.x < hoop.x + hoop.w &&
        ball.y > hoop.y &&
        ball.dy > 0
    ){
        score++;
        document.getElementById("score").innerText = score;
        resetBall();
    }

    // OUT OF BOUNDS
    if(ball.x < 0 || ball.x > canvas.width){
        resetBall();
    }
}

// =====================
// DRAW
// =====================

function draw(){

    ctx.fillStyle = "#87CEEB";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle = "#c27c3e";
    ctx.fillRect(0,500,canvas.width,100);

    // player
    ctx.fillStyle = "#2563eb";
    ctx.fillRect(player.x, player.y, player.w, player.h);

    // head
    ctx.beginPath();
    ctx.arc(player.x+20, player.y-10, 15, 0, Math.PI*2);
    ctx.fillStyle = "#ffdbac";
    ctx.fill();

    // ball
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2);
    ctx.fillStyle = "#ff8800";
    ctx.fill();

    // hoop
    ctx.fillStyle = "white";
    ctx.fillRect(backboard.x, backboard.y, backboard.w, backboard.h);

    ctx.fillStyle = "red";
    ctx.fillRect(hoop.x, hoop.y, hoop.w, hoop.h);
}

// =====================
// LOOP
// =====================

function loop(){
    updatePlayer();
    updateBall();
    draw();

    requestAnimationFrame(loop);
}

loop();

</script>

</body>
</html>
"""

components.html(html_code, height=650)
