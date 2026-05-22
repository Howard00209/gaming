import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Basketball Hold-to-Shoot", layout="wide")

st.title("🏀 Hold-to-Shoot Basketball (PC + Mobile)")

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

/* MOBILE BUTTON */
#controls {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
}

button {
    font-size: 18px;
    padding: 16px;
    border-radius: 12px;
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
// GAME STATE
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
// INPUT
// =====================

let keys = {};

// PC KEYBOARD
document.addEventListener("keydown",(e)=>{

    keys[e.code] = true;

    // HOLD T TO CHARGE
    if(e.code === "KeyT" && player.holding){
        charging = true;
    }
});

document.addEventListener("keyup",(e)=>{

    keys[e.code] = false;

    // RELEASE T TO SHOOT
    if(e.code === "KeyT" && charging){
        shoot();
        charging = false;
        power = 0;
    }
});

// =====================
// MOBILE HOLD BUTTON
// =====================

const shootBtn = document.getElementById("shootBtn");

shootBtn.addEventListener("touchstart",()=>{
    if(player.holding){
        charging = true;
    }
});

shootBtn.addEventListener("touchend",()=>{
    if(charging){
        shoot();
        charging = false;
        power = 0;
    }
});

// =====================
// SHOOT (POWER BASED)
// =====================

function shoot(){
    if(!player.holding) return;

    player.holding = false;
    ball.moving = true;

    let strength = Math.min(power / 20, 1);

    ball.dx = 6 + strength * 6;
    ball.dy = -10 - strength * 8;
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
// BALL UPDATE
// =====================

function updateBall(){

    if(charging){
        power++;
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

    // power bar
    ctx.fillStyle = "black";
    ctx.fillRect(20, 80, 100, 10);

    ctx.fillStyle = "lime";
    ctx.fillRect(20, 80, power, 10);
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
