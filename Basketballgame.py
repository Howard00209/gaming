import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Realistic Basketball", layout="wide")

st.title("🏀 Basketball Game (Fixed Shooting + Real Hoop)")

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
    background: linear-gradient(#87CEEB, #cfefff);
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
    margin: 4px;
    border-radius: 10px;
    border: none;
    background: #222;
    color: white;
}
</style>
</head>

<body>

<div id="ui">
Score: <span id="score">0</span><br>
Power: <span id="power">0</span>
</div>

<div id="controls">
<button id="shootBtn">🏀 HOLD SHOOT</button>
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
// REALISTIC HOOP
// =====================

const hoop = {
    x: 980,
    y: 220,
    r: 35
};

const backboard = {
    x: 1040,
    y: 150,
    w: 15,
    h: 150
};

const pole = {
    x: 1055,
    y: 120,
    w: 10,
    h: 380
};

// =====================
// INPUT
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

    if(e.code === "KeyT"){
        if(charging){
            shoot();
        }
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
// SHOOT (FIXED CORE BUG)
// =====================

function shoot(){

    if(!player.holding) return;

    player.holding = false;
    ball.moving = true;

    ball.x = player.x + 20;
    ball.y = player.y;

    let strength = Math.min(power / 25, 1);

    ball.dx = 7 + strength * 7;
    ball.dy = -11 - strength * 10;
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
// BALL PHYSICS (FIXED STABILITY)
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

    // SCORE (inside rim zone)
    let dx = ball.x - hoop.x;
    let dy = ball.y - hoop.y;

    let dist = Math.sqrt(dx*dx + dy*dy);

    if(dist < hoop.r && ball.dy > 0){
        score++;
        document.getElementById("score").innerText = score;
        resetBall();
    }

    if(ball.x < 0 || ball.x > canvas.width){
        resetBall();
    }
}

// =====================
// DRAW REALISTIC HOOP
// =====================

function draw(){

    // background
    ctx.fillStyle = "#87CEEB";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle = "#c27c3e";
    ctx.fillRect(0,500,canvas.width,100);

    // pole
    ctx.fillStyle = "#555";
    ctx.fillRect(pole.x, pole.y, pole.w, pole.h);

    // backboard
    ctx.fillStyle = "#fff";
    ctx.fillRect(backboard.x, backboard.y, backboard.w, backboard.h);

    // rim (realistic circle)
    ctx.beginPath();
    ctx.arc(hoop.x, hoop.y, hoop.r, 0, Math.PI*2);
    ctx.strokeStyle = "orange";
    ctx.lineWidth = 6;
    ctx.stroke();

    // net (cone style)
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;

    for(let i=0;i<6;i++){
        ctx.beginPath();
        ctx.moveTo(hoop.x - 25 + i*10, hoop.y + 5);
        ctx.lineTo(hoop.x, hoop.y + 70);
        ctx.stroke();
    }

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
