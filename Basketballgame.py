import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Basketball Fixed", layout="wide")

st.title("🏀 Basketball Game (Fixed Ball + Net Added)")

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

#ui {
    position: absolute;
    top: 10px;
    left: 10px;
    background: rgba(0,0,0,0.5);
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
// STATE
// =====================

let score = 0;
let power = 0;
let charging = false;

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
    gravity: 0.45,
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
// INPUT (PC + MOBILE)
// =====================

let keys = {};

// PC
document.addEventListener("keydown",(e)=>{

    keys[e.code] = true;

    if(e.code === "KeyT"){
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
    charging = true;
});

btn.addEventListener("touchend",()=>{
    shoot();
    charging = false;
    power = 0;
});

// =====================
// SHOOT (FIXED)
// =====================

function shoot(){

    if(!player.holding) return;

    player.holding = false;
    ball.moving = true;

    // ensure starting from player
    ball.x = player.x + 20;
    ball.y = player.y;

    let strength = Math.min(power / 25, 1);

    ball.dx = 7 + strength * 7;
    ball.dy = -10 - strength * 10;
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
// PLAYER
// =====================

function updatePlayer(){

    if(keys["KeyA"] || keys["ArrowLeft"]) player.x -= player.speed;
    if(keys["KeyD"] || keys["ArrowRight"]) player.x += player.speed;

    player.x = Math.max(0, Math.min(canvas.width - player.w, player.x));

    if(player.holding){
        ball.x = player.x + 20;
        ball.y = player.y;
    } else {
        pickup();
    }
}

// =====================
// BALL PHYSICS (FIXED)
// =====================

function updateBall(){

    if(charging){
        power += 1.2;
        if(power > 100) power = 100;
    }

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

    // SCORE (must go down)
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

    // out of bounds
    if(ball.x < 0 || ball.x > canvas.width){
        resetBall();
    }
}

// =====================
// DRAW
// =====================

function draw(){

    // background
    ctx.fillStyle = "#87CEEB";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    // ground
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

    // 🧵 NET (NEW)
    ctx.strokeStyle = "white";
    ctx.beginPath();
    ctx.moveTo(hoop.x, hoop.y + 10);
    ctx.lineTo(hoop.x + 10, hoop.y + 60);
    ctx.lineTo(hoop.x + 20, hoop.y + 70);
    ctx.lineTo(hoop.x + 30, hoop.y + 80);
    ctx.lineTo(hoop.x + 40, hoop.y + 70);
    ctx.lineTo(hoop.x + 50, hoop.y + 60);
    ctx.lineTo(hoop.x + 60, hoop.y + 70);
    ctx.lineTo(hoop.x + 70, hoop.y + 60);
    ctx.lineTo(hoop.x + 80, hoop.y + 10);
    ctx.stroke();

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
