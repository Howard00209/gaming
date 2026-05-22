import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🏀 Basketball Game",
    page_icon="🏀",
    layout="wide"
)

st.markdown("# 🏀 Basketball Shooter")
st.markdown("""
### Controls
- ⬅ Move Left
- ➡ Move Right
- SPACEBAR = Shoot
""")

game = """
<!DOCTYPE html>
<html>
<head>

<style>

body{
    margin:0;
    overflow:hidden;
    background:#0b1220;
}

/* GAME AREA */

#game{
    position:relative;
    width:100%;
    height:600px;
    overflow:hidden;
    background:linear-gradient(#102040,#07111f);
    border-radius:20px;
    border:5px solid white;
}

/* COURT */

#court{
    position:absolute;
    bottom:0;
    width:100%;
    height:140px;
    background:#c26a00;
    border-top:5px solid white;
}

/* PLAYER */

#player{
    position:absolute;
    bottom:100px;
    left:100px;
    font-size:55px;
    transition:left 0.03s linear;
}

/* BALL */

#ball{
    position:absolute;
    bottom:135px;
    left:125px;
    font-size:28px;
}

/* HOOP */

#hoop{
    position:absolute;
    right:120px;
    top:140px;
    font-size:70px;
}

/* SCORE */

#scoreboard{
    position:absolute;
    top:20px;
    left:20px;
    color:white;
    font-size:30px;
    font-weight:bold;
    z-index:100;
}

/* POWER BAR */

#powerBox{
    position:absolute;
    left:20px;
    bottom:20px;
    width:220px;
    height:25px;
    border:3px solid white;
    background:#222;
}

#power{
    width:50%;
    height:100%;
    background:lime;
}

/* TEXT */

#instructions{
    position:absolute;
    right:20px;
    top:20px;
    color:white;
    font-size:20px;
}

</style>

</head>

<body>

<div id="game">

    <div id="scoreboard">
        Score: <span id="score">0</span>
    </div>

    <div id="instructions">
        ⬅ ➡ Move<br>
        SPACE Shoot
    </div>

    <div id="hoop">🧺</div>

    <div id="player">⛹️</div>

    <div id="ball">🏀</div>

    <div id="court"></div>

    <div id="powerBox">
        <div id="power"></div>
    </div>

</div>

<script>

const player = document.getElementById("player");
const ball = document.getElementById("ball");
const scoreText = document.getElementById("score");
const powerBar = document.getElementById("power");

let playerX = 100;
let score = 0;
let shooting = false;

let power = 50;
let direction = 1;

/* ======================================
   POWER BAR
====================================== */

setInterval(() => {

    power += direction * 2;

    if(power >= 100){
        direction = -1;
    }

    if(power <= 10){
        direction = 1;
    }

    powerBar.style.width = power + "%";

    if(power > 70){
        powerBar.style.background = "red";
    }
    else if(power > 40){
        powerBar.style.background = "orange";
    }
    else{
        powerBar.style.background = "lime";
    }

}, 30);

/* ======================================
   MOVE PLAYER
====================================== */

document.addEventListener("keydown", (e) => {

    if(e.key === "ArrowLeft"){

        playerX -= 20;

        if(playerX < 0){
            playerX = 0;
        }

        player.style.left = playerX + "px";

        if(!shooting){
            ball.style.left = (playerX + 22) + "px";
        }
    }

    if(e.key === "ArrowRight"){

        playerX += 20;

        if(playerX > window.innerWidth - 300){
            playerX = window.innerWidth - 300;
        }

        player.style.left = playerX + "px";

        if(!shooting){
            ball.style.left = (playerX + 22) + "px";
        }
    }

    if(e.code === "Space" && !shooting){
        shoot();
    }

});

/* ======================================
   SHOOT FUNCTION
====================================== */

function shoot(){

    shooting = true;

    let x = playerX + 22;
    let y = 135;

    let velocityX = 7 + (power / 18);
    let velocityY = 14 + (power / 10);

    const gravity = 0.45;

    const hoopX = window.innerWidth - 220;
    const hoopY = 240;

    const interval = setInterval(() => {

        x += velocityX;
        y += velocityY;

        velocityY -= gravity;

        ball.style.left = x + "px";
        ball.style.bottom = y + "px";

        /* SCORE */

        if(
            x > hoopX &&
            x < hoopX + 70 &&
            y > hoopY &&
            y < hoopY + 60
        ){

            score++;

            scoreText.innerText = score;

            clearInterval(interval);

            resetBall();
        }

        /* MISS */

        if(
            y < -50 ||
            x > window.innerWidth + 100
        ){

            clearInterval(interval);

            resetBall();
        }

    }, 20);
}

/* ======================================
   RESET BALL
====================================== */

function resetBall(){

    shooting = false;

    ball.style.left = (playerX + 22) + "px";
    ball.style.bottom = "135px";
}

</script>

</body>
</html>
"""

components.html(game, height=620, scrolling=False)
