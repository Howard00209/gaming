import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Side View Basketball", layout="wide")

st.title("🏀 Basketball Game (Side View Hoop + Fixed Shoot)")

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
    background: linear-gradient(#87CEEB, #dff3ff);
    display: block;
}

#ui {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(0,0,0,0.6);
    color: white;
    padding: 10px;
    border-radius: 10px;
}

#controls {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
}

button {
    font-size: 18px;
    padding: 14px;
    border-radius: 10px;
    background: #222;
    color: white;
    border: none;
}
</style>
</head>

<body>

<div id="ui">
Score: <span id="score">0</span><br>
Power: <span id="power">0</span>
</div>

<div id="controls">
<button id="shootBtn">🏀 HOLD TO SHOOT</button>
</div>

<canvas id="game" width="1200" height="600"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// =====================
// STATE (FIXED)
// =====================

let score = 0;
let power = 0;
let charging = false;

const player = {
    x: 120,
    y: 450,
    w: 40,
    h: 80,
    speed: 6,
    holding: true
};

const ball = {
    x: 0,
    y: 0,
    r: 12,
    dx: 0,
    dy: 0,
    gravity: 0.45,
    moving: false
};

// =====================
// SIDE VIEW HOOP (IMPORTANT FIX)
// =====================

const hoop = {
    x: 980,
    y: 230,
    w: 55,   // horizontal rim width
    h: 10    // thickness
};

const backboard = {
    x: 1045,
    y: 150,
    w: 12,
    h: 150
};

// =====================
// INPUT SYSTEM (FIXED SHOOT)
// =====================

let keys = {};

// PC
document.addEventListener("keydown",(e)=>{

    keys[e.code] = true;

    if(e.code === "KeyT" && player.holding){
        charging = true;
    }
});

document.addEventListener("keyup",(e)=>{

    keys[e.code] = false;

    if(e.code === "KeyT" && charging){
        shoot();
        charging = false;
        power = 0;
    }
});

// MOBILE
const btn = document.getElementById("shootBtn");

btn.addEventListener("touchstart",()=>{
    if(player.holding) charging = true;
});

btn.addEventListener("touchend",()=>{
    if(charging){
        shoot();
    }
    charging = false;
    power = 0;
});

// =====================
// SHOOT (STABLE)
// =====================

function shoot(){

    if(!player.holding) return;

    player.holding = false;
    ball.moving = true;

    ball.x = player.x + 20;
    ball.y = player.y;

    let strength = Math.min(power / 25, 1);

    ball.dx = 7 + strength * 6;
    ball.dy = -10 - strength * 9;
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
// PLAYER
// =====================

function updatePlayer(){

    if(keys["KeyA"] || keys["ArrowLeft"]) player.x -= player.speed;
    if(keys["KeyD"] || keys["ArrowRight"]) player.x += player.speed;

    player.x = Math.max(0, Math.min(canvas.width - player.w, player.x));

    if(player.holding){
        ball.x = player.x + 20;
        ball.y = player.y;
    }
}

// =====================
// BALL PHYSICS
// =====================

function updateBall(){

    if(charging){
        power += 1.5;
        if(power > 100) power = 100;
    }

    if(!ball.moving) return;

    ball.x += ball.dx;
    ball.y += ball.dy;

    ball.dy += ball.gravity;

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

    // =====================
    // SIDE VIEW SCORE ZONE FIX
    // =====================

    let insideRimX = ball.x > hoop.x && ball.x < hoop.x + hoop.w;
    let nearRimY = ball.y > hoop.y && ball.y < hoop.y + 20;

    if(insideRimX && nearRimY && ball.dy > 0){
        score++;
        document.getElementById("score").innerText = score;
        resetBall();
    }
}

// =====================
// DRAW (SIDE VIEW HOOP FIXED)
// =====================

function draw(){

    ctx.fillStyle = "#87CEEB";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle = "#c27c3e";
    ctx.fillRect(0,500,canvas.width,100);

    // player
    ctx.fillStyle = "#2563eb";
    ctx.fillRect(player.x, player.y, player.w, player.h);

    ctx.beginPath();
    ctx.arc(player.x+20, player.y-10, 15, 0, Math.PI*2);
    ctx.fillStyle = "#ffdbac";
    ctx.fill();

    // ball
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2);
    ctx.fillStyle = "#ff8800";
    ctx.fill();

    // backboard
    ctx.fillStyle = "#fff";
    ctx.fillRect(backboard.x, backboard.y, backboard.w, backboard.h);

    // =====================
    // 🔴 SIDE VIEW RIM (REALISTIC)
    // =====================

    ctx.strokeStyle = "red";
    ctx.lineWidth = 5;

    ctx.beginPath();
    ctx.moveTo(hoop.x, hoop.y);
    ctx.lineTo(hoop.x + hoop.w, hoop.y);
    ctx.stroke();

    // rim thickness (front edge)
    ctx.beginPath();
    ctx.moveTo(hoop.x, hoop.y + hoop.h);
    ctx.lineTo(hoop.x + hoop.w, hoop.y + hoop.h);
    ctx.stroke();

    // net (hanging down)
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 1.5;

    for(let i=0;i<6;i++){
        let x = hoop.x + i * 9;
        ctx.beginPath();
        ctx.moveTo(x, hoop.y);
        ctx.lineTo(hoop.x + hoop.w/2, hoop.y + 60);
        ctx.stroke();
    }

    // power bar
    ctx.fillStyle = "black";
    ctx.fillRect(20,80,100,10);

    ctx.fillStyle = "lime";
    ctx.fillRect(20,80,power,10);
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
