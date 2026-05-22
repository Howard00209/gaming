import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Basketball Game", layout="wide")

st.title("🏀 3D Basketball Game (Clean Version)")

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
// SCENE
// =========================

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);

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
// COURT BACKGROUND (REAL LOOK)
// =========================

const court = new THREE.Mesh(
    new THREE.PlaneGeometry(50, 30),
    new THREE.MeshStandardMaterial({color:0xd2691e})
);
court.rotation.x = -Math.PI/2;
scene.add(court);

// court lines
function line(x,z,w,h){
    const g = new THREE.Mesh(
        new THREE.PlaneGeometry(w,h),
        new THREE.MeshBasicMaterial({color:0xffffff})
    );
    g.rotation.x = -Math.PI/2;
    g.position.set(x,0.01,z);
    scene.add(g);
}

// center line
line(0,0,50,0.2);
// key
line(13,0,4,10);

// =========================
// BORDERS (INVISIBLE WALLS)
// =========================

function wall(x,z,w,h,d){
    const m = new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d),
        new THREE.MeshBasicMaterial({visible:false})
    );
    m.position.set(x,h/2,z);
    scene.add(m);
    return m;
}

wall(0,-15,50,5,1);
wall(0,15,50,5,1);
wall(-25,0,1,5,30);
wall(25,0,1,5,30);

// =========================
// PLAYER
// =========================

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

// hands
const hand = new THREE.Mesh(
    new THREE.BoxGeometry(0.3,0.3,0.3),
    new THREE.MeshStandardMaterial({color:0xffd39b})
);
scene.add(hand);

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

    if(e.code === "Space" && holding){
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
    holding = false;

    ballVel.x = 0.3;
    ballVel.y = 0.4;
}

// =========================
// RESET BALL
// =========================

function resetBallToPlayer(){
    holding = true;
    ballVel = {x:0,y:0,z:0};
}

// =========================
// UPDATE PLAYER
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

    hand.position.set(
        body.position.x + 0.6,
        body.position.y + 1.1,
        body.position.z
    );

    // HOLD BALL
    if(holding){
        ball.position.set(
            body.position.x + 0.6,
            body.position.y + 1.1,
            body.position.z
        );
    }
}

// =========================
// BALL UPDATE
// =========================

function updateBall(){

    if(!holding){

        ball.position.x += ballVel.x;
        ball.position.y += ballVel.y;
        ball.position.z += ballVel.z;

        ballVel.y -= 0.015;

        // floor bounce
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
            resetBallToPlayer();
        }

        // OUT OF BOUNDS → RESET TO PLAYER (IMPORTANT)
        if(
            ball.position.x < -24 ||
            ball.position.x > 24 ||
            ball.position.z < -14 ||
            ball.position.z > 14 ||
            ball.position.y < -5
        ){
            resetBallToPlayer();
        }
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
