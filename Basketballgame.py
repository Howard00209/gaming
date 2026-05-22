import streamlit as st
import random
import time
import math

# ======================================================
# PAGE SETUP
# ======================================================

st.set_page_config(
    page_title="🏀 Hardcore Basketball Game",
    page_icon="🏀",
    layout="wide"
)

# ======================================================
# CUSTOM CSS + HTML
# ======================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background: #07111f;
    color: white;
    font-family: 'Trebuchet MS', sans-serif;
}

.title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: orange;
    text-shadow: 0px 0px 20px red;
    margin-bottom: 20px;
}

.scoreboard {
    background: linear-gradient(90deg,#ff5e00,#ff0000);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 25px;
    box-shadow: 0px 0px 20px rgba(255,100,0,0.6);
}

.court {
    background: #c26a00;
    border: 10px solid white;
    border-radius: 20px;
    height: 450px;
    position: relative;
    overflow: hidden;
}

.hoop {
    position: absolute;
    top: 80px;
    right: 80px;
    font-size: 90px;
}

.ball {
    position: absolute;
    bottom: 50px;
    left: 60px;
    font-size: 70px;
    animation: bounce 0.7s infinite;
}

.defender {
    position: absolute;
    bottom: 60px;
    left: 45%;
    font-size: 80px;
    animation: moveDefender 2s infinite alternate;
}

@keyframes moveDefender {
    from { transform: translateX(-100px); }
    to { transform: translateX(100px); }
}

@keyframes bounce {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-25px); }
    100% { transform: translateY(0px); }
}

.success {
    color: lime;
    font-size: 40px;
    font-weight: bold;
    text-align: center;
}

.fail {
    color: red;
    font-size: 40px;
    font-weight: bold;
    text-align: center;
}

.warning {
    color: yellow;
    font-size: 25px;
    text-align: center;
}

.energy {
    font-size: 22px;
    color: cyan;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE
# ======================================================

if "score" not in st.session_state:
    st.session_state.score = 0

if "shots" not in st.session_state:
    st.session_state.shots = 0

if "energy" not in st.session_state:
    st.session_state.energy = 100

if "combo" not in st.session_state:
    st.session_state.combo = 0

if "level" not in st.session_state:
    st.session_state.level = 1

# ======================================================
# TITLE
# ======================================================

st.markdown('<div class="title">🏀 HARDCORE BASKETBALL</div>', unsafe_allow_html=True)

# ======================================================
# SCOREBOARD
# ======================================================

st.markdown(f"""
<div class="scoreboard">
Score: {st.session_state.score} &nbsp;&nbsp;&nbsp;
Shots: {st.session_state.shots} &nbsp;&nbsp;&nbsp;
Combo: {st.session_state.combo} 🔥 &nbsp;&nbsp;&nbsp;
Level: {st.session_state.level}
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="energy">
⚡ Energy: {st.session_state.energy}/100
</div>
""", unsafe_allow_html=True)

# ======================================================
# BASKETBALL COURT
# ======================================================

st.markdown("""
<div class="court">
    <div class="hoop">🧺</div>
    <div class="defender">🧍</div>
    <div class="ball">🏀</div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("## 🎮 Precision Shooting Controls")

# ======================================================
# GAME CONTROLS
# ======================================================

col1, col2 = st.columns(2)

with col1:
    power = st.slider("💪 Shot Power", 0, 100, 50)

with col2:
    angle = st.slider("📐 Shot Angle", 0, 90, 45)

curve = st.slider("🌀 Curve Control", -50, 50, 0)

# ======================================================
# DIFFICULTY SYSTEM
# ======================================================

ideal_power = random.randint(45, 75)
ideal_angle = random.randint(35, 60)
ideal_curve = random.randint(-15, 15)

# Accuracy calculations
power_diff = abs(power - ideal_power)
angle_diff = abs(angle - ideal_angle)
curve_diff = abs(curve - ideal_curve)

accuracy = 100 - (
    power_diff * 0.9 +
    angle_diff * 1.2 +
    curve_diff * 0.5
)

# Make higher levels harder
accuracy -= (st.session_state.level * 5)

# Clamp accuracy
accuracy = max(0, min(100, accuracy))

# ======================================================
# SHOOT BUTTON
# ======================================================

if st.button("🏀 SHOOT BALL", use_container_width=True):

    if st.session_state.energy <= 0:
        st.error("💀 You are too exhausted to shoot!")
        st.stop()

    st.session_state.shots += 1
    st.session_state.energy -= 5

    with st.spinner("Ball in the air..."):
        time.sleep(2)

    randomness = random.randint(-15, 15)
    final_score = accuracy + randomness

    if final_score > 75:

        combo_bonus = st.session_state.combo * 2
        earned = 2 + combo_bonus

        st.session_state.score += earned
        st.session_state.combo += 1

        st.markdown(
            f'<div class="success">🔥 SWISH! +{earned} points!</div>',
            unsafe_allow_html=True
        )

        st.balloons()

    elif final_score > 55:

        st.session_state.score += 1
        st.session_state.combo = 0

        st.markdown(
            '<div class="warning">😮 Rim Shot! Only 1 point.</div>',
            unsafe_allow_html=True
        )

    else:

        st.session_state.combo = 0

        st.markdown(
            '<div class="fail">❌ BLOCKED BY DEFENDER!</div>',
            unsafe_allow_html=True
        )

    # Level Up System
    if st.session_state.score >= st.session_state.level * 10:
        st.session_state.level += 1

        st.success(f"🚀 LEVEL UP! Welcome to Level {st.session_state.level}")

# ======================================================
# REST BUTTON
# ======================================================

if st.button("😴 Rest (+20 Energy)"):

    st.session_state.energy = min(
        100,
        st.session_state.energy + 20
    )

# ======================================================
# RESET GAME
# ======================================================

if st.button("🔄 FULL RESET"):

    st.session_state.score = 0
    st.session_state.shots = 0
    st.session_state.energy = 100
    st.session_state.combo = 0
    st.session_state.level = 1

    st.rerun()

# ======================================================
# STATS PANEL
# ======================================================

with st.expander("📊 Advanced Stats"):

    shooting_percent = 0

    if st.session_state.shots > 0:
        shooting_percent = round(
            (st.session_state.score / (st.session_state.shots * 2)) * 100,
            1
        )

    st.write(f"🎯 Shooting Efficiency: {shooting_percent}%")
    st.write(f"🔥 Current Combo Streak: {st.session_state.combo}")
    st.write(f"⚡ Remaining Energy: {st.session_state.energy}")
    st.write(f"🏆 Current Difficulty Level: {st.session_state.level}")

# ======================================================
# GAME RULES
# ======================================================

with st.expander("📖 Hardcore Rules"):

    st.write("""
    ### Welcome to Hardcore Basketball

    This is NOT easy.

    You must:
    - Control shot power
    - Aim the angle correctly
    - Add proper curve
    - Beat the defender
    - Manage energy
    - Build combo streaks

    ### Difficulty Features
    - Random hidden target values
    - Defender blocks shots
    - Accuracy penalties
    - Increasing level difficulty
    - Energy exhaustion
    - Random shot physics

    ### Tips
    - Medium power works best
    - Angles around 45° are safer
    - Extreme curve is risky
    - Higher combos give bonus points
    """)

# ======================================================
# FOOTER
# ======================================================

st.markdown("""
<hr>

<center>
<h2 style='color:orange'>
🏀 Built with Streamlit + HTML + CSS
</h2>

<h4 style='color:gray'>
Can you survive Level 10?
</h4>
</center>
""", unsafe_allow_html=True)
