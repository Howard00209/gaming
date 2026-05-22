import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Basketball Game", layout="wide")

st.title("🏀 3D Basketball Game (Mobile + Desktop)")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<style>
body {
    margin: 0;
    overflow: hidden;
    background: #0f172a;
    font-family: Arial;
}

#ui {
    position: absolute;
    top: 10px;
    left: 10px;
    color: white;
    font-size: 20px;
    background: rgba(0,0,0,0.5);
    padding: 10px;
    border-radius: 10px;
}

button {
    font-size: 20px;
    padding: 15px;
    margin: 5px;
    border-radius: 10px;
}

#controls {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
}

</style>
</head>

<body>

<div id="ui">
Score: <span id="score">0</span>
</div>

<div id="controls">
<button onclick="moveLeft()">⬅️</button>
<button onclick="jump()">⬆️</button>
<button onclick="moveRight()">➡️</button>
<button onclick="shoot()">🏀 Shoot</button>
</div>

<script>

// ==========================
// BASIC SETUP
// ==========================

let scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);

let camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
camera.position.set(0, 5, 12);

let renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// ==========================
// LIGHT
// ==========================

let light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5,10,5);
scene.add(light);

// ==========================
// COURT
// ==========================

let floorGeo = new THREE.PlaneGeometry(30, 20);
let floorMat = new THREE.MeshStandardMaterial({color:0xd2691e});
let floor = new THREE.Mesh(floorGeo, floorMat);
floor.rotation.x = -Math.PI/2;
scene.add(floor);

// ==========================
// PLAYER
// ==========================

let playerGeo = new THREE.BoxGeometry(1,2,1);
let playerMat = new THREE.MeshStandardMaterial({color:0x2563eb});
let player = new THREE.Mesh(playerGeo, playerMat);
player.position.set(-10,1,0);
scene.add(player);

// ==========================
// BALL
// ==========================

let ballGeo = new THREE.SphereGeometry(0.3,16,16);
let ballMat = new THREE.MeshStandardMaterial({color:0xffa500});
let ball = new THREE.Mesh(ballGeo, ballMat);
scene.add(ball);

let ballVel = {x:0,y:0,z:0};
let holdingBall = true;

// ==========================
// HOOP (FIXED TO WALL)
// ==========================

let backboardGeo = new THREE.BoxGeometry(0.2,3,2);
let backboardMat = new THREE.MeshStandardMaterial({color:0xffffff});
let backboard = new THREE.Mesh(backboardGeo, backboardMat);
backboard.position.set(12,3,0);
scene.add(backboard);

// rim
let rimGeo = new THREE.TorusGeometry(0.7,0.05,16,100);
let rimMat = new THREE.MeshStandardMaterial({color:0xff0000});
let rim = new THREE.Mesh(rimGeo, rimMat);
rim.position.set(11,2.5,0);
rim.rotation.x = Math.PI/2;
scene.add(rim);

// hoop center
let hoopX = 11;
let hoopY = 2.5;
let hoopZ = 0;

// ==========================
// GAME VARIABLES
// ==========================

let score = 0;

// ==========================
// CONTROLS
// ==========================

let keys = {};

document.addEventListener("keydown",(e)=>{
    keys[e.code] = true;

    if(e.code === "Space"){
        jump();
    }
});

document.addEventListener("keyup",(e)=>{
    keys[e.code] = false;
});

// ==========================
// MOBILE BUTTONS
// ==========================

function moveLeft(){ player.position.x -= 0.7; }
function moveRight(){ player.position.x += 0.7; }

function jump(){
    if(player.position.y <= 1){
        player.position.y = 3;
    }
}

function shoot(){
    if(!holdingBall) return;

    holdingBall = false;

    ball.position.set(player.position.x, 2, player.position.z);

    ballVel.x = 0.2;
    ballVel.y = 0.35;
    ballVel.z = 0;
}

// ==========================
// UPDATE BALL
// ==========================

function updateBall(){

    if(holdingBall){
        ball.position.set(player.position.x, 2, player.position.z);
        return;
    }

    ball.position.x += ballVel.x;
    ball.position.y += ballVel.y;
    ball.position.z += ballVel.z;

    ballVel.y -= 0.015; // gravity

    // ground
    if(ball.position.y < 0.3){
        ball.position.y = 0.3;
        ballVel.y *= -0.6;
    }

    // backboard collision
    if(ball.position.x > 10.8 &&
       ball.position.y < 5 &&
       ball.position.y > 1 &&
       Math.abs(ball.position.z) < 1.2){

        ballVel.x *= -0.8;
    }

    // SCORE CHECK (must go DOWN into hoop)
    let dx = ball.position.x - hoopX;
    let dy = ball.position.y - hoopY;
    let dz = ball.position.z - hoopZ;

    let dist = Math.sqrt(dx*dx + dy*dy + dz*dz);

    if(dist < 0.8 && ballVel.y < 0){

        score++;
        document.getElementById("score").innerText = score;

        resetBall();
    }

    // reset if missed
    if(ball.position.y < -5 || ball.position.x > 20){
        resetBall();
    }
}

function resetBall(){
    holdingBall = true;
    ballVel = {x:0,y:0,z:0};
}

// ==========================
// UPDATE PLAYER (keyboard)
// ==========================

function updatePlayer(){

    if(keys["ArrowLeft"] || keys["KeyA"]){
        player.position.x -= 0.2;
    }

    if(keys["ArrowRight"] || keys["KeyD"]){
        player.position.x += 0.2;
    }
}

// ==========================
// LOOP
// ==========================

function animate(){
    requestAnimationFrame(animate);

    updatePlayer();
    updateBall();

    renderer.render(scene, camera);
}

animate();

window.addEventListener("resize",()=>{
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

</script>

</body>
</html>
"""

components.html(html_code, height=800)
