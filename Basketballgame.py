import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ultimate Basketball Game", layout="wide")

st.title("🏀 Ultimate Basketball Game")

game = """
<!DOCTYPE html>
<html>
<head>
<style>
    body{
        margin:0;
        overflow:hidden;
        background:#87CEEB;
    }

    canvas{
        display:block;
        margin:auto;
        border:6px solid black;
        border-radius:12px;
        background:linear-gradient(#87CEEB,#dff6ff);
    }
</style>
</head>

<body>

<canvas id="gameCanvas" width="1200" height="700"></canvas>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// ======================================
// GAME VARIABLES
// ======================================

let score = 0;
let highScore = 0;
let combo = 0;
let timer = 60;
let gameOver = false;

// ======================================
// PLAYER
// ======================================

const player = {
    x: 120,
    y: 500,
    width: 60,
    height: 120,
    speed: 7,
    velocityY: 0,
    jumping: false
};

// ======================================
// BALL
// ======================================

const ball = {
    x: 0,
    y: 0,
    radius: 16,
    dx: 0,
    dy: 0,
    gravity: 0.45,
    shooting: false,
    trail: []
};

// ======================================
// HOOP
// ======================================

const hoop = {
    x: 950,
    y: 220,
    width: 90,
    height: 12,
    moveDirection: 1
};

// ======================================
// CONTROLS
// ======================================

const keys = {};

document.addEventListener("keydown",(e)=>{
    keys[e.code] = true;

    // Jump
    if((e.code === "KeyW" || e.code === "ArrowUp") && !player.jumping){
        player.velocityY = -15;
        player.jumping = true;
    }
});

document.addEventListener("keyup",(e)=>{
    keys[e.code] = false;

    // SHOOT
    if(e.code === "Space" && !ball.shooting && !gameOver){

        ball.shooting = true;

        ball.dx = shootPower * 0.75;
        ball.dy = -shootPower;

        shootPower = 0;
        charging = false;
    }
});

// ======================================
// SHOOT POWER
// ======================================

let shootPower = 0;
let charging = false;

// ======================================
// RESET BALL
// ======================================

function resetBall(){
    ball.shooting = false;
    ball.dx = 0;
    ball.dy = 0;
    ball.trail = [];
}

// ======================================
// DRAW PLAYER
// ======================================

function drawPlayer(){

    // Legs
    ctx.strokeStyle = "black";
    ctx.lineWidth = 5;

    ctx.beginPath();
    ctx.moveTo(player.x+15,player.y+90);
    ctx.lineTo(player.x+10,player.y+125);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(player.x+45,player.y+90);
    ctx.lineTo(player.x+50,player.y+125);
    ctx.stroke();

    // Body
    ctx.fillStyle = "#1565C0";
    ctx.fillRect(player.x,player.y,player.width,90);

    // Head
    ctx.beginPath();
    ctx.arc(player.x+30,player.y-20,22,0,Math.PI*2);
    ctx.fillStyle = "#FFD39B";
    ctx.fill();

    // Arm
    ctx.strokeStyle = "#FFD39B";
    ctx.lineWidth = 8;

    ctx.beginPath();
    ctx.moveTo(player.x+60,player.y+25);
    ctx.lineTo(player.x+80,player.y+10);
    ctx.stroke();
}

// ======================================
// DRAW BALL
// ======================================

function drawBall(){

    // Trail
    for(let i=0;i<ball.trail.length;i++){

        const t = ball.trail[i];

        ctx.beginPath();
        ctx.arc(t.x,t.y,ball.radius-5,0,Math.PI*2);
        ctx.fillStyle = "rgba(255,140,0,0.2)";
        ctx.fill();
    }

    ctx.beginPath();
    ctx.arc(ball.x,ball.y,ball.radius,0,Math.PI*2);

    const gradient = ctx.createRadialGradient(
        ball.x-5,
        ball.y-5,
        5,
        ball.x,
        ball.y,
        20
    );

    gradient.addColorStop(0,"#FFD54F");
    gradient.addColorStop(1,"#F57C00");

    ctx.fillStyle = gradient;
    ctx.fill();

    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
    ctx.stroke();
}

// ======================================
// DRAW COURT
// ======================================

function drawCourt(){

    // Floor
    ctx.fillStyle = "#D2691E";
    ctx.fillRect(0,620,canvas.width,80);

    // Court lines
    ctx.strokeStyle = "white";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.arc(300,620,120,Math.PI,0);
    ctx.stroke();

    // Hoop pole
    ctx.fillStyle = "black";
    ctx.fillRect(1080,140,10,260);

    // Backboard
    ctx.fillStyle = "white";
    ctx.fillRect(1040,170,12,120);

    // Rim
    ctx.fillStyle = "red";
    ctx.fillRect(hoop.x,hoop.y,hoop.width,hoop.height);

    // Net
    ctx.strokeStyle = "white";

    for(let i=0;i<8;i++){

        ctx.beginPath();
        ctx.moveTo(hoop.x + i*11, hoop.y+12);
        ctx.lineTo(hoop.x + 10 + i*8, hoop.y+45);
        ctx.stroke();
    }
}

// ======================================
// SCOREBOARD
// ======================================

function drawUI(){

    ctx.fillStyle = "rgba(0,0,0,0.7)";
    ctx.fillRect(20,20,320,180);

    ctx.fillStyle = "white";
    ctx.font = "30px Arial";

    ctx.fillText("Score: " + score,40,60);
    ctx.fillText("High Score: " + highScore,40,100);
    ctx.fillText("Combo: x" + combo,40,140);
    ctx.fillText("Time: " + timer,40,180);

    // Power bar
    if(charging){

        ctx.fillStyle = "lime";
        ctx.fillRect(20,220,shootPower*12,25);

        ctx.strokeStyle = "white";
        ctx.strokeRect(20,220,240,25);
    }

    // Controls
    ctx.fillStyle = "black";
    ctx.font = "22px Arial";
    ctx.fillText(
        "Move: A/D  Jump: W/↑  Hold SPACE to shoot",
        320,
        40
    );

    if(gameOver){

        ctx.fillStyle = "rgba(0,0,0,0.8)";
        ctx.fillRect(0,0,canvas.width,canvas.height);

        ctx.fillStyle = "white";
        ctx.font = "70px Arial";
        ctx.fillText("GAME OVER",390,280);

        ctx.font = "40px Arial";
        ctx.fillText("Final Score: " + score,450,360);

        ctx.font = "28px Arial";
        ctx.fillText("Refresh page to restart",440,430);
    }
}

// ======================================
// UPDATE PLAYER
// ======================================

function updatePlayer(){

    if(keys["KeyA"] || keys["ArrowLeft"]){
        player.x -= player.speed;
    }

    if(keys["KeyD"] || keys["ArrowRight"]){
        player.x += player.speed;
    }

    // Gravity
    player.y += player.velocityY;
    player.velocityY += 0.8;

    // Ground collision
    if(player.y >= 500){
        player.y = 500;
        player.velocityY = 0;
        player.jumping = false;
    }

    // Boundaries
    if(player.x < 0) player.x = 0;

    if(player.x + player.width > canvas.width){
        player.x = canvas.width - player.width;
    }

    // Hold ball
    if(!ball.shooting){

        ball.x = player.x + 80;
        ball.y = player.y + 25;
    }

    // Charging
    if(keys["Space"]){

        charging = true;

        if(shootPower < 24){
            shootPower += 0.25;
        }
    }
}

// ======================================
// UPDATE BALL
// ======================================

function updateBall(){

    if(ball.shooting){

        ball.x += ball.dx;
        ball.y += ball.dy;

        ball.dy += ball.gravity;

        // Trail
        ball.trail.push({x:ball.x,y:ball.y});

        if(ball.trail.length > 12){
            ball.trail.shift();
        }

        // Floor bounce
        if(ball.y + ball.radius > 620){

            ball.y = 620 - ball.radius;
            ball.dy *= -0.72;
        }

        // Wall bounce
        if(ball.x + ball.radius > canvas.width ||
           ball.x - ball.radius < 0){

            ball.dx *= -0.82;
        }

        // SCORE
        if(
            ball.x > hoop.x &&
            ball.x < hoop.x + hoop.width &&
            ball.y > hoop.y &&
            ball.y < hoop.y + 25
        ){

            combo += 1;

            let points = 2 * combo;

            score += points;

            if(score > highScore){
                highScore = score;
            }

            resetBall();
        }

        // Missed shot reset
        if(ball.y > canvas.height + 150 ||
           ball.x > canvas.width + 150){

            combo = 0;
            resetBall();
        }
    }
}

// ======================================
// MOVING HOOP
// ======================================

function updateHoop(){

    hoop.x += 2 * hoop.moveDirection;

    if(hoop.x > 1020 || hoop.x < 800){
        hoop.moveDirection *= -1;
    }
}

// ======================================
// TIMER
// ======================================

setInterval(()=>{

    if(!gameOver){

        timer--;

        if(timer <= 0){
            gameOver = true;
        }
    }

},1000);

// ======================================
// GAME LOOP
// ======================================

function gameLoop(){

    ctx.clearRect(0,0,canvas.width,canvas.height);

    drawCourt();

    updatePlayer();
    updateBall();
    updateHoop();

    drawPlayer();
    drawBall();

    drawUI();

    requestAnimationFrame(gameLoop);
}

gameLoop();

</script>

</body>
</html>
"""

components.html(game, height=720)
