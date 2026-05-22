import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Basketball Stable Hoop", layout="wide")

st.title("🏀 Basketball Game (No Sticking + Single Hoop Fix)")

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
</style>
</head>

<body>

<canvas id="game" width="1200" height="600"></canvas>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// =====================
// STATE
// =====================

let score = 0;

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
    gravity: 0.35,
    moving: false
};

// =====================
// SINGLE HOOP (CLEAN)
// =====================

const hoop = {
    x: 980,
    y: 250,
    w: 60,
    h: 12
};

const backboard = {
    x: 1045,
    y: 150,
    w: 12,
    h: 160
};

// =====================
// INPUT (keyboard only for simplicity)
// =====================

let keys = {};

document.addEventListener("keydown",(e)=>keys[e.code]=true);
document.addEventListener("keyup",(e)=>keys[e.code]=false);

// click to shoot (simple test control)
document.addEventListener("mousedown", shoot);

// =====================
// SHOOT
// =====================

function shoot(){

    if(!player.holding) return;

    player.holding = false;
    ball.moving = true;

    ball.x = player.x + 20;
    ball.y = player.y;

    ball.dx = 6;
    ball.dy = -9;
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

    if(keys["ArrowLeft"]) player.x -= player.speed;
    if(keys["ArrowRight"]) player.x += player.speed;

    player.x = Math.max(0, Math.min(canvas.width - player.w, player.x));

    if(player.holding){
        ball.x = player.x + 20;
        ball.y = player.y;
    }
}

// =====================
// BALL PHYSICS (NO STICKING FIX)
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

    // =====================
    // BACKBOARD BOUNCE
    // =====================

    if(
        ball.x + ball.r > backboard.x &&
        ball.x - ball.r < backboard.x + backboard.w &&
        ball.y + ball.r > backboard.y &&
        ball.y - ball.r < backboard.y + backboard.h
    ){
        ball.dx *= -0.8;
    }

    // =====================
    // RIM COLLISION (ANTI-STICK FIX)
    // =====================

    let rimLeft = hoop.x;
    let rimRight = hoop.x + hoop.w;
    let rimTop = hoop.y;
    let rimBottom = hoop.y + hoop.h;

    let hitRim =
        ball.x > rimLeft - ball.r &&
        ball.x < rimRight + ball.r &&
        ball.y > rimTop - ball.r &&
        ball.y < rimBottom + ball.r;

    if(hitRim){

        // push ball OUT so it doesn't stick
        if(ball.x < (rimLeft + rimRight)/2){
            ball.x -= 2;
        } else {
            ball.x += 2;
        }

        // bounce only if moving into rim
        if(ball.dy > 0){
            ball.dy *= -0.5;
        }
        ball.dx *= 0.6;
    }

    // =====================
    // SCORING (ONLY FROM ABOVE)
    // =====================

    let inside = ball.x > rimLeft && ball.x < rimRight;
    let falling = ball.dy > 0;

    if(
        inside &&
        ball.y > rimTop &&
        ball.y < rimBottom + 10 &&
        falling
    ){
        score++;
        resetBall();
    }
}

// =====================
// DRAW (SINGLE HOOP ONLY)
// =====================

function draw(){

    ctx.fillStyle = "#87CEEB";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle = "#c27c3e";
    ctx.fillRect(0,500,canvas.width,100);

    // player
    ctx.fillStyle = "#2563eb";
    ctx.fillRect(player.x, player.y, player.w, player.h);

    // ball
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2);
    ctx.fillStyle = "#ff8800";
    ctx.fill();

    // backboard
    ctx.fillStyle = "#fff";
    ctx.fillRect(backboard.x, backboard.y, backboard.w, backboard.h);

    // =====================
    // SINGLE RIM ONLY (NO DOUBLE LINE)
    // =====================

    ctx.strokeStyle = "red";
    ctx.lineWidth = 5;

    ctx.beginPath();
    ctx.moveTo(hoop.x, hoop.y);
    ctx.lineTo(hoop.x + hoop.w, hoop.y);
    ctx.stroke();

    // net (visual only)
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 1;

    for(let i=0;i<6;i++){
        let x = hoop.x + i*10;
        ctx.beginPath();
        ctx.moveTo(x, hoop.y);
        ctx.lineTo(hoop.x + hoop.w/2, hoop.y + 60);
        ctx.stroke();
    }
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
