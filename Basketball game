import streamlit as st
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🏀 Streamlit Basketball Game",
    page_icon="🏀",
    layout="centered"
)

# ---------------- CUSTOM HTML + CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: orange;
    text-shadow: 2px 2px 8px black;
}

.score-board {
    background: linear-gradient(90deg, #ff6600, #ff3300);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

.court {
    background-color: #d97706;
    border: 8px solid white;
    border-radius: 20px;
    height: 300px;
    position: relative;
    margin-top: 20px;
}

.hoop {
    position: absolute;
    top: 40px;
    right: 40px;
    font-size: 70px;
}

.ball {
    position: absolute;
    bottom: 40px;
    left: 40px;
    font-size: 60px;
    animation: bounce 1s infinite;
}

@keyframes bounce {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}

.success {
    color: lime;
    font-size: 30px;
    text-align: center;
    font-weight: bold;
}

.fail {
    color: red;
    font-size: 30px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "shots" not in st.session_state:
    st.session_state.shots = 0

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">🏀 Basketball Challenge</div>', unsafe_allow_html=True)

# ---------------- SCOREBOARD ----------------
st.markdown(
    f"""
    <div class="score-board">
        Score: {st.session_state.score} <br>
        Shots Taken: {st.session_state.shots}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- COURT ----------------
st.markdown("""
<div class="court">
    <div class="hoop">🧺</div>
    <div class="ball">🏀</div>
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("## Take Your Shot!")

# ---------------- DIFFICULTY ----------------
difficulty = st.selectbox(
    "Choose Difficulty",
    ["Easy", "Medium", "Hard"]
)

# Win chance based on difficulty
difficulty_chance = {
    "Easy": 0.8,
    "Medium": 0.5,
    "Hard": 0.3
}

# ---------------- SHOOT BUTTON ----------------
if st.button("🏀 SHOOT!"):

    st.session_state.shots += 1

    with st.spinner("Ball is flying..."):
        time.sleep(1.5)

    shot_result = random.random()

    if shot_result < difficulty_chance[difficulty]:
        st.session_state.score += 2

        st.markdown(
            '<div class="success">🔥 SWISH! You scored 2 points!</div>',
            unsafe_allow_html=True
        )

        st.balloons()

    else:
        st.markdown(
            '<div class="fail">❌ Missed Shot!</div>',
            unsafe_allow_html=True
        )

# ---------------- RESET BUTTON ----------------
if st.button("🔄 Reset Game"):
    st.session_state.score = 0
    st.session_state.shots = 0
    st.rerun()

# ---------------- GAME RULES ----------------
with st.expander("📖 Game Rules"):
    st.write("""
    - Press the **SHOOT** button to take a basketball shot.
    - Different difficulties change your chance to score.
    - Each successful shot gives **2 points**.
    - Try to get the highest score possible!
    """)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<center>
<h4 style='color:orange;'>
Built with ❤️ using Streamlit
</h4>
</center>
""", unsafe_allow_html=True)
