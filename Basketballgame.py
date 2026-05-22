import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Basketball Game", layout="wide")

st.title("🏀 3D Basketball Game (Pickup + Background)")

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

#ui {
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 10px;
    background: rgba(0,0,0,0.5);
    color: white;
    border-radius: 10px;
}
</style>
</head>

<body>

<div id="ui">Score: <span id="score">0</span></div>

<script>

// =========================
// SCENE + BACKGROUND
// =========================

const scene = new THREE.Scene();

/* 🌄 SKY BACKGROUND */
const loader = new THREE.TextureLoader();
scene.background = loader.load(
    "https://threejs.org/examples/textures/skybox/sky.png"
);

// CAMERA
const camera = new THREE.PerspectiveCamera(70, window.innerWidth/window.innerHeight, 0.1, 1000);
camera.position.set(0, 6, 18);

// RENDERER
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// LIGHT
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5,10,5);
scene.add(light);

// =========================
// COURT
// =========================

const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(50, 30),
    new THREE.MeshStandardMaterial({color:0xd2691e})
);
floor.rotation.x = -Math.PI/2;
scene.add(floor);

// =========================
// PLAYER
// =========================

const body = new THREE.Mesh(
    new THREE.BoxGeometry(1,2,1),
    new THREE.MeshStandardMaterial({color:0x2563eb})
);
body.position.set(-10,1,0);
scene.add(body);

// HEAD
const head = new THREE.Mesh(
    new THREE.SphereGeometry(0.4,16,16),
    new THREE.MeshStandardMaterial({color:0xffd39b})
);
scene.add(head);

// =========================
// BALL
// =========================

const ball = new THREE.Mesh(
    new THREE.SphereGeometry(0.3,16,16),
    new THREE.MeshStandardMaterial({color:0xff8800})
);
scene.add(ball);

let holding = true;
let ballVel = {x:0,y:0,z:0};

// =========================
// HOOP
// =========================

const backboard = new THREE.Mesh(
    new THREE.BoxGeometry(0.3,4,2),
    new THREE.MeshStandardMaterial({color:0xffffff})
);
backboard.position.set(15,6,0);
scene.add(backboard);

const rim = new THREE.Mesh(
    new THREE.TorusGeometry(0.8,0.05,16,100),
    new THREE.MeshStandardMaterial({color:0xff0000})
);
rim.position.set(14,5,0);
rim.rotation.x = Math.PI/2;
scene.add(rim);

// =========================
// INPUT
// =========================

let keys = {};
let score = 0;

document.addEventListener("keydown",(e)=>{
    keys[e.code] = true;

    if(e.code === "Space"){
        shoot();
    }
});

document.addEventListener("keyup",(e)=>{
    keys[e.code] = false;
});

// =========================
// SHOOT
// =========================

function shoot(){
    if(!holding) return;

    holding = false;

    ballVel.x = 0.35;
    ballVel.y = 0.45;
}

// =========================
// RESET
// =========================

function resetBall(){
    holding = true;
    ballVel = {x:0,y:0,z:0};
}

// =========================
// DISTANCE PICKUP SYSTEM (NEW)
// =========================

function tryPickup(){

    let dx = ball.position.x - body.position.x;
    let dy = ball.position.y - body.position.y;
    let dz = ball.position.z - body.position.z;

    let dist = Math.sqrt(dx*dx + dy*dy + dz*dz);

    if(dist < 1.5){
        resetBall();
    }
}

// =========================
// PLAYER UPDATE
// =========================

function updatePlayer(){

    if(keys["KeyA"]) body.position.x -= 0.2;
    if(keys["KeyD"]) body.position.x += 0.2;
    if(keys["KeyW"]) body.position.z -= 0.2;
    if(keys["KeyS"]) body.position.z += 0.2;

    head.position.set(
        body.position.x,
        body.position.y + 1.4,
        body.position.z
    );

    // BALL IN HANDS
    if(holding){
        ball.position.set(
            body.position.x + 0.6,
            body.position.y + 1.1,
            body.position.z
        );
    } else {
        tryPickup(); // NEW: pickup system
    }
}

// =========================
// BALL UPDATE
// =========================

function updateBall(){

    if(holding) return;

    ball.position.x += ballVel.x;
    ball.position.y += ballVel.y;
    ball.position.z += ballVel.z;

    ballVel.y -= 0.015;

    // floor
    if(ball.position.y < 0.3){
        ball.position.y = 0.3;
        ballVel.y *= -0.5;
    }

    // backboard bounce
    if(
        ball.position.x > 14.5 &&
        ball.position.y < 7 &&
        ball.position.y > 3
    ){
        ballVel.x *= -0.8;
    }

    // SCORE
    let dx = ball.position.x - 14;
    let dy = ball.position.y - 5;

    if(Math.sqrt(dx*dx + dy*dy) < 0.7 && ballVel.y < 0){

        score++;
        document.getElementById("score").innerText = score;

        resetBall();
    }

    // OUT OF BOUNDS → RETURN TO PLAYER
    if(
        ball.position.x < -24 ||
        ball.position.x > 24 ||
        ball.position.z < -14 ||
        ball.position.z > 14 ||
        ball.position.y < -5
    ){
        resetBall();
    }
}

// =========================
// LOOP
// =========================

function animate(){
    requestAnimationFrame(animate);

    updatePlayer();
    updateBall();

    renderer.render(scene,camera);
}

animate();

// resize
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
