import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="🏀 Keyboard Basketball",
    page_icon="🏀",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.markdown("""
# 🏀 Keyboard Basketball Game

### Controls
- ⬅ LEFT ARROW = Move Left
- ➡ RIGHT ARROW = Move Right
- SPACEBAR = Shoot Ball

Try to score in the basket!
""")

# =========================================================
# HTML + CSS + JAVASCRIPT GAME
# =========================================================

game_code = """
<!DOCTYPE html>
<html>
<head>

<style>

body {
    margin: 0;
    overflow: hidden;
    background: #07111f;
    font-family: Arial;
}

#game {
    position: relative;
    width: 100%;
    height: 650px;
    background: linear-gradient(to bottom, #0f172a, #111827);
    overflow: hidden;
    border-radius: 20px;
    border: 5px solid white;
}

/* COURT */
#court {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 180px;
    background: #c26a00;
    border-top: 8px solid white;
}

/* PLAYER */
#player {
    position: absolute;
    bottom: 140px;
    left: 120px;
    font-size: 70px;
    transition: left 0.05s linear;
}

/* BALL */
#ball {
    position: absolute;
    bottom: 185px;
    left: 145px;
    font-size: 40px;
}

/* HOOP */
#hoop {
    position: absolute;
    right: 120px;
    top: 160px;
    font-size: 100px;
}

/* SCOREBOARD */
#scoreboard {
    position: absolute;
    top: 20px;
    left: 20px;
    color: white;
    font-size: 35px;
    font-weight: bold;
}

/* POWER BAR */
#powerContainer {
    position: absolute;
    bottom: 30px;
    left: 30px;
    width: 250px;
    height: 30px;
    border: 3px solid white;
    background: #222;
}

#powerBar {
    width: 50%;
    height: 100%;
    background: lime;
}

.instructions {
    position: absolute;
    top: 20px;
    right: 20px;
    color: white;
    font-size: 22px;
    text-align: right;
}

</style>
</head>

<body>

<div id="game">

    <div id="scoreboard">
        Score: <span id="score">0</span>
    </div>

    <div class="instructions">
        ⬅ ➡ Move<br>
        SPACE = Shoot
    </div>

    <div id="hoop">🧺</div>

    <div id="player">⛹️</div>

    <div id="ball">🏀</div>

    <div id="court"></div>

    <div id="powerContainer">
        <div id="powerBar"></div>
    </div>

</div>

<script>

let player = document.getElementById("player");
let ball = document.getElementById("ball");
let scoreText = document.getElementById("score");
let powerBar = document.getElementById("powerBar");

let playerX = 120;

let score = 0;

let shooting = false;

let power = 50;
let powerDirection = 1;

/* =========================================
   POWER BAR ANIMATION
========================================= */

setInterval(() => {

    power += powerDirection * 2;

    if(power >= 100){
        powerDirection = -1;
    }

    if(power <= 10){
        powerDirection = 1;
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

/* =========================================
   KEYBOARD CONTROLS
========================================= */

document.addEventListener("keydown", function(event){

    // LEFT
    if(event.key === "ArrowLeft"){

        playerX -= 25;

        if(playerX < 0){
            playerX = 0;
        }

        player.style.left = playerX + "px";

        if(!shooting){
            ball.style.left = (playerX + 25) + "px";
        }
    }

    // RIGHT
    if(event.key === "ArrowRight"){

        playerX += 25;

        if(playerX > window.innerWidth - 300){
            playerX = window.innerWidth - 300;
        }

        player.style.left = playerX + "px";

        if(!shooting){
            ball.style.left = (playerX + 25) + "px";
        }
    }

    // SHOOT
    if(event.code === "Space" && !shooting){

        shootBall();
    }

});

/* =========================================
   SHOOT FUNCTION
========================================= */

function shootBall(){

    shooting = true;

    let ballX = playerX + 25;
    let ballY = 185;

    let velocityX = 10 + (power / 10);
    let velocityY = 18 + (power / 6);

    let gravity = 0.6;

    let hoopX = window.innerWidth - 240;
    let hoopY = 170;

    let interval = setInterval(() => {

        ballX += velocityX;
        ballY += velocityY;

        velocityY -= gravity;

        ball.style.left = ballX + "px";
        ball.style.bottom = ballY + "px";

        // SCORE DETECTION
        if(
            ballX > hoopX &&
            ballX < hoopX + 90 &&
            ballY > hoopY &&
            ballY < hoopY + 60
        ){

            score++;

            scoreText.innerText = score;

            clearInterval(interval);

            resetBall();
        }

        // MISS
        if(ballY < 0 || ballX > window.innerWidth){

            clearInterval(interval);

            resetBall();
        }

    }, 20);
}

/* =========================================
   RESET BALL
========================================= */

function resetBall(){

    shooting = false;

    ball.style.bottom = "185px";
    ball.style.left = (playerX + 25) + "px";
}

</script>

</body>
</html>
"""

# =========================================================
# DISPLAY GAME
# =========================================================

components.html(game_code, height=700, scrolling=False)
