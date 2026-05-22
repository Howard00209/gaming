import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Ultimate Basketball Game", layout="wide")

st.title("🏀 Ultimate Basketball Game")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>

body{
    margin:0;
    overflow:hidden;
    background:#0f172a;
    font-family:Arial;
}

canvas{
    display:block;
    margin:auto;
    margin-top:10px;
    border-radius:18px;
    border:5px solid #1e293b;
    box-shadow:0 0 30px rgba(0,0,0,0.5);
    background:linear-gradient(#60a5fa,#dbeafe);
}

</style>
</head>

<body>

<canvas id="gameCanvas" width="1400" height="760"></canvas>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// ========================================
// GAME VARIABLES
// ========================================

let score = 0;
let highScore = 0;

let particles = [];

// ========================================
// PLAYER
// ========================================

const player = {
    x: 120,
    y: 560,
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
    gravity: 0.42,
    shooting: false,
    trail:[]
};

// ========================================
// HOOP
// ========================================

const hoop = {
    x: 1180,
    y: 250,
    width: 95,
    height: 12
};

// ========================================
// KEYS
// ========================================

const keys = {};

document.addEventListener("keydown",(e)=>{

    keys[e.code] = true;

    // JUMP
    if(e.code === "Space" && !player.jumping){

        player.velY = -17;
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
// PARTICLES
// ========================================

function createParticles(x,y){

    for(let i=0;i<40;i++){

        particles.push({

            x:x,
            y:y,

            dx:(Math.random()-0.5)*8,
            dy:(Math.random()-0.5)*8,

            size:Math.random()*8 + 2,

            life:100
        });
    }
}

function updateParticles(){

    for(let i=particles.length-1;i>=0;i--){

        let p = particles[i];

        p.x += p.dx;
        p.y += p.dy;

        p.life--;

        if(p.life <= 0){
            particles.splice(i,1);
        }
    }
}

function drawParticles(){

    for(let p of particles){

        ctx.beginPath();

        ctx.arc(p.x,p.y,p.size,0,Math.PI*2);

        ctx.fillStyle = "gold";

        ctx.fill();
    }
}

// ========================================
// DRAW PLAYER
// ========================================

function drawPlayer(){

    // Shadow
    ctx.fillStyle = "rgba(0,0,0,0.2)";
    ctx.beginPath();
    ctx.ellipse(player.x+30,675,35,10,0,0,Math.PI*2);
    ctx.fill();

    // Legs
    ctx.strokeStyle = "#111";
    ctx.lineWidth = 6;

    ctx.beginPath();
    ctx.moveTo(player.x+15,player.y+100);
    ctx.lineTo(player.x+10,player.y+140);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(player.x+45,player.y+100);
    ctx.lineTo(player.x+50,player.y+140);
    ctx.stroke();

    // Jersey
    ctx.fillStyle = "#2563eb";
    ctx.fillRect(player.x,player.y,player.width,100);

    // Jersey Number
    ctx.fillStyle = "white";
    ctx.font = "30px Arial";
    ctx.fillText("23",player.x+13,player.y+60);

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
    ctx.lineTo(player.x+82,player.y+15);
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

    // Ball
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

    gradient.addColorStop(0,"#fde68a");
    gradient.addColorStop(1,"#ea580c");

    ctx.fillStyle = gradient;
    ctx.fill();

    ctx.strokeStyle = "#111";
    ctx.lineWidth = 2;
    ctx.stroke();
}

// ========================================
// DRAW COURT
// ========================================

function drawCourt(){

    // Floor
    ctx.fillStyle = "#c2410c";
    ctx.fillRect(0,680,canvas.width,80);

    // Wood details
    ctx.strokeStyle = "rgba(255,255,255,0.15)";
    ctx.lineWidth = 2;

    for(let i=0;i<canvas.width;i+=80){

        ctx.beginPath();
        ctx.moveTo(i,680);
        ctx.lineTo(i,760);
        ctx.stroke();
    }

    // Three point arc
    ctx.strokeStyle = "white";
    ctx.lineWidth = 4;

    ctx.beginPath();
    ctx.arc(350,680,160,Math.PI,0);
    ctx.stroke();

    // Hoop stand fixed to wall
    ctx.fillStyle = "#111";

    ctx.fillRect(1320,100,18,350);

    // Backboard
    ctx.fillStyle = "white";
    ctx.fillRect(1260,180,16,130);

    // Rim
    ctx.fillStyle = "red";
    ctx.fillRect(hoop.x,hoop.y,hoop.width,hoop.height);

    // Net
    ctx.strokeStyle = "white";

    for(let i=0;i<8;i++){

        ctx.beginPath();

        ctx.moveTo(hoop.x + i*12, hoop.y+12);
        ctx.lineTo(hoop.x + 10 + i*9, hoop.y+50);

        ctx.stroke();
    }
}

// ========================================
// UI
// ========================================

function drawUI(){

    // Glass panel
    ctx.fillStyle = "rgba(15,23,42,0.75)";
    ctx.fillRect(25,25,360,220);

    // Outline
    ctx.strokeStyle = "rgba(255,255,255,0.2)";
    ctx.strokeRect(25,25,360,220);

    // Title
    ctx.fillStyle = "#f8fafc";
    ctx.font = "bold 34px Arial";
    ctx.fillText("SCOREBOARD",50,70);

    // Score
    ctx.fillStyle = "#22c55e";
    ctx.font = "bold 50px Arial";
    ctx.fillText(score,60,140);

    // High score
    ctx.fillStyle = "#facc15";
    ctx.font = "28px Arial";
    ctx.fillText("High Score: " + highScore,60,190);

    // Controls
    ctx.fillStyle = "white";
    ctx.font = "20px Arial";

    ctx.fillText("A / D → Move",1020,50);
    ctx.fillText("SPACE → Jump",1020,80);
    ctx.fillText("Hold T → Shoot",1020,110);

    // Power bar
    if(charging){

        ctx.fillStyle = "#22c55e";

        ctx.fillRect(50,215,shootPower*10,22);

        ctx.strokeStyle = "white";
        ctx.strokeRect(50,215,260,22);
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
    if(player.y >= 560){

        player.y = 560;
        player.velY = 0;
        player.jumping = false;
    }

    // Bounds
    if(player.x < 0) player.x = 0;

    if(player.x + player.width > canvas.width){
        player.x = canvas.width - player.width;
    }

    // Hold ball
    if(player.holdingBall){

        ball.x = player.x + 75;
        ball.y = player.y + 25;
    }

    // Charge shot
    if(keys["KeyT"] && player.holdingBall){

        charging = true;

        if(shootPower < 30){
            shootPower += 0.4;
        }
    }

    // Release shot
    if(!keys["KeyT"] && charging && player.holdingBall){

        player.holdingBall = false;

        ball.shooting = true;

        // HIGHER ARC
        ball.dx = shootPower * 0.65;
        ball.dy = -shootPower * 1.4;

        charging = false;
        shootPower = 0;
    }
}

// ========================================
// BALL UPDATE
// ========================================

let alreadyScored = false;

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

        if(ball.trail.length > 12){
            ball.trail.shift();
        }

        // Floor bounce
        if(ball.y + ball.radius > 680){

            ball.y = 680 - ball.radius;
            ball.dy *= -0.72;
        }

        // Wall bounce
        if(ball.x + ball.radius > canvas.width ||
           ball.x - ball.radius < 0){

            ball.dx *= -0.8;
        }

        // Friction
        ball.dx *= 0.995;

        // SCORE DETECTION
        if(
            ball.x > hoop.x &&
            ball.x < hoop.x + hoop.width &&
            ball.y > hoop.y &&
            ball.y < hoop.y + 30 &&
            !alreadyScored
        ){

            alreadyScored = true;

            score += 2;

            if(score > highScore){
                highScore = score;
            }

            // SCORE ANIMATION
            createParticles(ball.x,ball.y);
        }

        // Reset score flag
        if(ball.y > hoop.y + 120){
            alreadyScored = false;
        }

        // Pickup ball
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
// GAME LOOP
// ========================================

function gameLoop(){

    ctx.clearRect(0,0,canvas.width,canvas.height);

    drawCourt();

    updatePlayer();
    updateBall();

    updateParticles();

    drawPlayer();
    drawBall();

    drawParticles();

    drawUI();

    requestAnimationFrame(gameLoop);
}

gameLoop();

</script>

</body>
</html>
"""

components.html(html_code, height=780)
