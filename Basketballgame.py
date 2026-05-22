import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Basketball Pro", layout="wide")

st.title("🏀 3D Basketball Pro (Boundaries + Animation + 3PT Line)")

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
    padding: 10px;
    background: rgba(0,0,0,0.5);
    color: white;
    border-radius: 10px;
}

/* mobile controls */
#controls {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
}

button {
    font-size: 18px;
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

// ============================
// SCENE
// ============================

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

// ============================
// COURT FLOOR
// ============================

const floor = new THREE.Mesh(
    new THREE.PlaneGeometry(40, 25),
    new THREE.MeshStandardMaterial({color:0xd2691e})
);
floor.rotation.x = -Math.PI/2;
scene.add(floor);

// ============================
// COURT BORDERS (NO OUT OF BOUNDS)
// ============================

function createWall(x,z,w,h,d){
    const wall = new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d),
        new THREE.MeshStandardMaterial({color:0x333333})
    );
    wall.position.set(x,h/2,z);
    scene.add(wall);
    return wall;
}

// 4 walls
createWall(0, -12.5, 40, 4, 1); // back
createWall(0, 12.5, 40, 4, 1);  // front
createWall(-20, 0, 1, 4, 25);   // left
createWall(20, 0, 1, 4, 25);    // right

// ============================
// THREE POINT LINE
// ============================

const curve = new THREE.EllipseCurve(
    -8, 0,
    10, 7,
    0, Math.PI,
    false,
    0
);

const points = curve.getPoints(50);
const geometry = new THREE.BufferGeometry().setFromPoints(points);

const line = new THREE.Line(
    geometry,
    new THREE.LineBasicMaterial({color:0xffffff})
);

line.rotation.x = -Math.PI/2;
scene.add(line);

// ============================
// PLAYER
// ============================

const body = new THREE.Mesh(
    new THREE.BoxGeometry(1,2,1),
    new THREE.MeshStandardMaterial({color:0x2563eb})
);
body.position.set(-10,1,0);
scene.add(body);

// head
const head = new THREE.Mesh(
    new THREE.SphereGeometry(0.4,16,16),
    new THREE.MeshStandardMaterial({color:0xffd39b})
);
scene.add(head);

// ============================
// BALL
// ============================

const ball = new THREE.Mesh(
    new THREE.SphereGeometry(0.3,16,16),
    new THREE.MeshStandardMaterial({color:0xff8800})
);
scene.add(ball);

let holding = true;
let ballVel = {x:0,y:0,z:0};

// ============================
// HOOP (FIXED)
// ============================

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

// ============================
// ANIMATION STATE
// ============================

let shootAnim = 0;
let score = 0;

// ============================
// INPUT
// ============================

let keys = {};

document.addEventListener("keydown",(e)=>{
    keys[e.code] = true;
    if(e.code === "Space") jump();
});

document.addEventListener("keyup",(e)=>{
    keys[e.code] = false;
});

// mobile
function left(){ body.position.x -= 0.6; }
function right(){ body.position.x += 0.6; }

function jump(){
    if(body.position.y <= 1){
        body.position.y = 3;
    }
}

// ============================
// SHOOT (WITH ANIMATION)
// ============================

function shoot(){
    if(!holding) return;

    shootAnim = 1; // start animation
}

// ============================
// UPDATE PLAYER + BALL HOLD
// ============================

function updatePlayer(){

    if(keys["ArrowLeft"]) body.position.x -= 0.2;
    if(keys["ArrowRight"]) body.position.x += 0.2;

    head.position.set(
        body.position.x,
        body.position.y + 1.4,
        body.position.z
    );

    // HOLD BALL IN HANDS
    if(holding){

        ball.position.set(
            body.position.x + 0.6,
            body.position.y + 1.2,
            body.position.z
        );
    }
}

// ============================
// SHOOT ANIMATION + BALL PHYSICS
// ============================

function updateBall(){

    // SHOOT ANIMATION (arm delay)
    if(shootAnim > 0){

        shootAnim -= 0.05;

        // release moment
        if(shootAnim <= 0.5 && holding){

            holding = false;

            ballVel.x = 0.3;
            ballVel.y = 0.4;
            ballVel.z = 0;
        }
    }

    if(holding) return;

    ball.position.x += ballVel.x;
    ball.position.y += ballVel.y;
    ball.position.z += ballVel.z;

    ballVel.y -= 0.015;

    // COURT BOUNDARIES (NO OUT OF BOUNDS)
    ball.position.x = Math.max(-19, Math.min(19, ball.position.x));
    ball.position.z = Math.max(-12, Math.min(12, ball.position.z));

    if(ball.position.y < 0.3){
        ball.position.y = 0.3;
        ballVel.y *= -0.5;
    }

    // SCORE
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

// ============================
// RESET
// ============================

function resetBall(){
    holding = true;
    ballVel = {x:0,y:0,z:0};
}

// ============================
// LOOP
// ============================

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
