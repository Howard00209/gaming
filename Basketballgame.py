import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Basketball Game", layout="wide")

st.title("🏀 3D Basketball Game (Fixed + Improved)")

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
    font-family: Arial;
}

/* UI */
#ui {
    position: absolute;
    top: 10px;
    left: 10px;
    color: white;
    background: rgba(0,0,0,0.5);
    padding: 10px;
    border-radius: 10px;
    font-size: 18px;
}

/* mobile controls */
#controls {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
}

button {
    font-size: 20px;
    padding: 12px;
    margin: 4px;
    border-radius: 10px;
}
</style>
</head>

<body>

<div id="ui">Score: <span id="score">0</span></div>

<div id="controls">
<button onclick="left()">⬅️</button>
<button onclick="jump()">⬆️</button>
<button onclick="right()">➡️</button>
<button onclick="shoot()">🏀 Shoot</button>
</div>

<script>

// ======================
// SCENE
// ======================

let scene = new THREE.Scene();

// SKY BACKGROUND (FIXED)
scene.background = new THREE.Color(0x87ceeb);

// CAMERA (FIXED ANGLE)
let camera = new THREE.PerspectiveCamera(
    70,
    window.innerWidth/window.innerHeight,
    0.1,
    1000
);

camera.position.set(0, 6, 16);
camera.lookAt(0, 3, 0);

// RENDERER
let renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// LIGHT
let light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5,10,5);
scene.add(light);

// ======================
// COURT
// ======================

let floor = new THREE.Mesh(
    new THREE.PlaneGeometry(40, 25),
    new THREE.MeshStandardMaterial({color:0xd2691e})
);
floor.rotation.x = -Math.PI/2;
scene.add(floor);

// ======================
// PLAYER (FIXED HEAD)
// ======================

let body = new THREE.Mesh(
    new THREE.BoxGeometry(1,2,1),
    new THREE.MeshStandardMaterial({color:0x2563eb})
);
body.position.set(-10,1,0);
scene.add(body);

// HEAD (FIXED MISSING PART)
let head = new THREE.Mesh(
    new THREE.SphereGeometry(0.4,16,16),
    new THREE.MeshStandardMaterial({color:0xffd39b})
);
scene.add(head);

// ======================
// BALL
// ======================

let ball = new THREE.Mesh(
    new THREE.SphereGeometry(0.3,16,16),
    new THREE.MeshStandardMaterial({color:0xff8800})
);
scene.add(ball);

let ballVel = {x:0,y:0,z:0};
let holding = true;

// ======================
// HOOP (HIGHER + FIXED WALL)
// ======================

let backboard = new THREE.Mesh(
    new THREE.BoxGeometry(0.3,4,2),
    new THREE.MeshStandardMaterial({color:0xffffff})
);

backboard.position.set(15,6,0);
scene.add(backboard);

// rim (higher now)
let rim = new THREE.Mesh(
    new THREE.TorusGeometry(0.8,0.05,16,100),
    new THREE.MeshStandardMaterial({color:0xff0000})
);

rim.position.set(14,5,0);
rim.rotation.x = Math.PI/2;
scene.add(rim);

// ======================
// GAME DATA
// ======================

let score = 0;

// ======================
// CONTROLS
// ======================

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

// MOBILE
function left(){ body.position.x -= 0.6; }
function right(){ body.position.x += 0.6; }

function jump(){
    if(body.position.y <= 1){
        body.position.y = 3;
    }
}

function shoot(){

    if(!holding) return;

    holding = false;

    ball.position.set(body.position.x,2,body.position.z);

    ballVel.x = 0.25;
    ballVel.y = 0.35;
    ballVel.z = 0;
}

// ======================
// UPDATE
// ======================

function updatePlayer(){

    if(keys["ArrowLeft"] || keys["KeyA"]){
        body.position.x -= 0.2;
    }

    if(keys["ArrowRight"] || keys["KeyD"]){
        body.position.x += 0.2;
    }

    // sync head position (FIXED BUG)
    head.position.set(
        body.position.x,
        body.position.y + 1.4,
        body.position.z
    );
}

function updateBall(){

    if(holding){
        ball.position.set(body.position.x,2,0);
        return;
    }

    ball.position.x += ballVel.x;
    ball.position.y += ballVel.y;
    ball.position.z += ballVel.z;

    ballVel.y -= 0.015;

    // floor
    if(ball.position.y < 0.3){
        ball.position.y = 0.3;
        ballVel.y *= -0.5;
    }

    // backboard collision
    if(
        ball.position.x > 14.5 &&
        ball.position.y < 7 &&
        ball.position.y > 3 &&
        Math.abs(ball.position.z) < 1
    ){
        ballVel.x *= -0.8;
    }

    // SCORE ONLY FROM ABOVE
    let dx = ball.position.x - 14;
    let dy = ball.position.y - 5;
    let dz = ball.position.z;

    let dist = Math.sqrt(dx*dx + dy*dy + dz*dz);

    if(dist < 0.7 && ballVel.y < 0){

        score++;
        document.getElementById("score").innerText = score;

        resetBall();
    }

    if(ball.position.y < -5){
        resetBall();
    }
}

function resetBall(){
    holding = true;
    ballVel = {x:0,y:0,z:0};
}

// ======================
// LOOP
// ======================

function animate(){
    requestAnimationFrame(animate);

    updatePlayer();
    updateBall();

    renderer.render(scene,camera);
}

animate();

// resize fix
window.addEventListener("resize",()=>{
    camera.aspect = window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
});

</script>

</body>
</html>
"""

components.html(html_code, height=800)
