import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Basketball Game", layout="wide")

st.title("🏀 Advanced Basketball Game")

html_code = """
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
    background:linear-gradient(#87CEEB,#E0F7FA);
    border:6px solid black;
    border-radius:12px;
}

</style>
</head>

<body>

<canvas id="gameCanvas" width="1300" height="720"></canvas>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// ========================================
// GAME VARIABLES
// ========================================

let score = 0;
let highScore = 0;

// ========================================
// PLAYER
// ========================================

const player = {
    x: 120,
    y: 520,
    width: 60,
    height: 100,
    speed: 7,
    velY: 0,
    jumping: false,
    holdingBall: true
};

// ========================================
// BALL
// ========================================

const ball = {
    x: 0,
    y: 0,
    radius: 16,
    dx: 0,
    dy: 0,
    gravity: 0.45,
    shooting: false,
    trail:[]
};

// ========================================
// HOOP
// ========================================

const hoop = {
    x: 980,
    y: 220,
    width: 90,
    height: 12,
    direction:1
};

// ========================================
// KEYS
// ========================================

const keys = {};

document.addEventListener("keydown",(e)=>{

    keys[e.code] = true;

    // JUMP
    if(e.code === "Space" && !player.jumping){

        player.velY = -16;
        player.jumping = true;
    }

});

document.addEventListener("keyup",(e)=>{
    keys[e.code] = false;
});

// ========================================
// SHOOTING POWER
// ========================================

let charging = false;
let shootPower = 0;

// ========================================
// DRAW PLAYER
// ========================================

function drawPlayer(){

    // Legs
    ctx.strokeStyle = "black";
    ctx.lineWidth = 5;

    ctx.beginPath();
    ctx.moveTo(player.x+15,player.y+100);
    ctx.lineTo(player.x+10,player.y+135);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(player.x+45,player.y+100);
    ctx.lineTo(player.x+50,player.y+135);
    ctx.stroke();

    // Body
    ctx.fillStyle = "#1565C0";
    ctx.fillRect(player.x,player.y,player.width,100);

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
    ctx.lineTo(player.x+80,player.y+15);
    ctx.stroke();
}

// ========================================
// DRAW BALL
// ========================================

function drawBall(){

    // Trail
    for(let i=0;i<ball.trail.length;i++){

        let t = ball.trail[i];

        ctx.beginPath();
        ctx.arc(t.x,t.y,ball.radius-5,0,Math.PI*2);
        ctx.fillStyle = "rgba(255,140,0,0.2)";
        ctx.fill();
    }

    ctx.beginPath();

    ctx.arc(ball.x,ball.y,ball.radius,0,Math.PI*2);

    let gradient = ctx.createRadialGradient(
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
    ctx.stroke();
}

// ========================================
// DRAW COURT
// ========================================

function drawCourt(){

    // Floor
    ctx.fillStyle = "#C97B30";
    ctx.fillRect(0,640,canvas.width,80);

    // Lines
    ctx.strokeStyle = "white";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.arc(300,640,120,Math.PI,0);
    ctx.stroke();

    // Hoop pole
    ctx.fillStyle = "black";
    ctx.fillRect(1120,150,12,260);

    // Backboard
    ctx.fillStyle = "white";
    ctx.fillRect(1080,180,12,120);

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

// ========================================
// UI
// ========================================

function drawUI(){

    ctx.fillStyle = "rgba(0,0,0,0.65)";
    ctx.fillRect(20,20,340,180);

    ctx.fillStyle = "white";
    ctx.font = "32px Arial";

    ctx.fillText("Score: " + score,40,70);
    ctx.fillText("High Score: " + highScore,40,120);

    ctx.font = "22px Arial";
    ctx.fillText("Move: A / D",40,170);
    ctx.fillText("Jump: SPACE",40,200);
    ctx.fillText("Hold T to Shoot",40,230);

    // Power bar
    if(charging){

        ctx.fillStyle = "lime";

        ctx.fillRect(20,250,shootPower*12,24);

        ctx.strokeStyle = "white";
        ctx.strokeRect(20,250,240,24);
    }
}

// ========================================
// PLAYER UPDATE
// ========================================

function updatePlayer(){

    if(keys["KeyA"] || keys["ArrowLeft"]){
        player.x -= player.speed;
    }

    if(keys["KeyD"] || keys["ArrowRight"]){
        player.x += player.speed;
    }

    // Gravity
    player.y += player.velY;
    player.velY += 0.8;

    // Ground collision
    if(player.y >= 520){

        player.y = 520;
        player.velY = 0;
        player.jumping = false;
    }

    // Bounds
    if(player.x < 0) player.x = 0;

    if(player.x + player.width > canvas.width){
        player.x = canvas.width - player.width;
    }

    // Holding ball
    if(player.holdingBall){

        ball.x = player.x + 75;
        ball.y = player.y + 30;
    }

    // SHOOT CHARGE
    if(keys["KeyT"] && player.holdingBall){

        charging = true;

        if(shootPower < 26){
            shootPower += 0.3;
        }
    }

    // RELEASE SHOT
    if(!keys["KeyT"] && charging && player.holdingBall){

        player.holdingBall = false;
        ball.shooting = true;

        ball.dx = shootPower * 0.8;
        ball.dy = -shootPower;

        charging = false;
        shootPower = 0;
    }
}

// ========================================
// BALL UPDATE
// ========================================

function updateBall(){

    if(ball.shooting){

        ball.x += ball.dx;
        ball.y += ball.dy;

        ball.dy += ball.gravity;

        // Trail
        ball.trail.push({
            x:ball.x,
            y:ball.y
        });

        if(ball.trail.length > 10){
            ball.trail.shift();
        }

        // Floor bounce
        if(ball.y + ball.radius > 640){

            ball.y = 640 - ball.radius;
            ball.dy *= -0.72;
        }

        // Wall bounce
        if(ball.x + ball.radius > canvas.width ||
           ball.x - ball.radius < 0){

            ball.dx *= -0.8;
        }

        // Ball friction
        ball.dx *= 0.995;

        // Score
        if(
            ball.x > hoop.x &&
            ball.x < hoop.x + hoop.width &&
            ball.y > hoop.y &&
            ball.y < hoop.y + 25
        ){

            score += 2;

            if(score > highScore){
                highScore = score;
            }
        }

        // PICKUP BALL
        let distX = ball.x - (player.x + 30);
        let distY = ball.y - (player.y + 50);

        let distance = Math.sqrt(distX*distX + distY*distY);

        if(distance < 55){

            player.holdingBall = true;

            ball.shooting = false;

            ball.dx = 0;
            ball.dy = 0;
            ball.trail = [];
        }
    }
}

// ========================================
// MOVING HOOP
// ========================================

function updateHoop(){

    hoop.x += hoop.direction * 2;

    if(hoop.x > 1050 || hoop.x < 860){
        hoop.direction *= -1;
    }
}

// ========================================
// GAME LOOP
// ========================================

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

components.html(html_code, height=740)
