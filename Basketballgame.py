import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Basketball Pro", layout="wide")

st.title("🏀 3D Basketball Pro (Rotations Added)")

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
    color: white;
    background: rgba(0,0,0,0.5);
    border-radius: 10px;
}
</style>
</head>

<body>

<div id="ui">Score: <span id="score">0</span></div>

<script>

// =========================
// SCENE
// =========================

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);

const camera = new THREE.PerspectiveCamera(70, window.innerWidth/window.innerHeight, 0.1, 1000);
camera.position.set(0, 6, 18);

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
    new THREE.PlaneGeometry(40, 25),
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
// 3-POINT LINE (ROTATED 3D ARC)
// =========================

const curve = new THREE.EllipseCurve(
    0, 0,
    10, 7,
    0, Math.PI,
    false,
    0
);

const points = curve.getPoints(80);

const lineGeo = new THREE.BufferGeometry().setFromPoints(points);

const threePointLine = new THREE.Line(
    lineGeo,
    new THREE.LineBasicMaterial({color:0xffffff})
);

// MOVE + ROTATE INTO COURT SPACE (IMPORTANT FIX)
threePointLine.position.set(5,0,0);
threePointLine.rotation.x = -Math.PI/2;
threePointLine.rotation.z = Math.PI/8;

scene.add(threePointLine);

// =========================
// INPUT
// =========================

let keys = {};
let facing = 1; // NEW: player direction

document.addEventListener("keydown",(e)=>{
    keys[e.code] = true;
});

document.addEventListener("keyup",(e)=>{
    keys[e.code] = false;
});

// =========================
// UPDATE PLAYER (ROTATION FIXED)
// =========================

function updatePlayer(){

    let moved = false;

    if(keys["KeyA"]){
        body.position.x -= 0.2;
        facing = -1;
        moved = true;
    }

    if(keys["KeyD"]){
        body.position.x += 0.2;
        facing = 1;
        moved = true;
    }

    if(keys["KeyW"]){
        body.position.z -= 0.2;
        moved = true;
    }

    if(keys["KeyS"]){
        body.position.z += 0.2;
        moved = true;
    }

    // ROTATE PLAYER TOWARD MOVEMENT
    if(moved){
        body.rotation.y = facing === 1 ? 0 : Math.PI;
    }

    // HEAD FOLLOW
    head.position.set(
        body.position.x,
        body.position.y + 1.4,
        body.position.z
    );

    // BALL IN HANDS
    if(holding){
        ball.position.set(
            body.position.x + (0.6 * facing),
            body.position.y + 1.1,
            body.position.z
        );
    }
}

// =========================
// BALL
// =========================

let score = 0;

function updateBall(){

    if(holding) return;

    ball.position.x += ballVel.x;
    ball.position.y += ballVel.y;
    ball.position.z += ballVel.z;

    ballVel.y -= 0.015;

    if(ball.position.y < 0.3){
        ball.position.y = 0.3;
        ballVel.y *= -0.5;
    }

    // SCORE CHECK
    let dx = ball.position.x - 14;
    let dy = ball.position.y - 5;

    if(Math.sqrt(dx*dx + dy*dy) < 0.7 && ballVel.y < 0){

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

// =========================
// SHOOT
// =========================

document.addEventListener("keydown",(e)=>{
    if(e.code === "Space" && holding){

        holding = false;

        ballVel.x = 0.3 * facing;
        ballVel.y = 0.4;
        ballVel.z = 0;
    }
});

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

// RESIZE
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
