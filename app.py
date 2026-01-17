import streamlit as st
import random

# ------------------ WORD DATABASE ------------------
WORDS = {
    "Easy": ["apple", "ball", "cat", "dog", "fish"],
    "Medium": ["python", "orange", "laptop", "school", "garden"],
    "Hard": ["algorithm", "developer", "interface", "database", "framework"]
}

# ------------------ INITIALIZE SESSION ------------------
if "word" not in st.session_state:
    st.session_state.word = ""
    st.session_state.guessed = set()
    st.session_state.lives = 6
    st.session_state.score = 0
    st.session_state.hint_used = False
    st.session_state.game_started = False

# ------------------ FUNCTIONS ------------------
def start_game(difficulty):
    st.session_state.word = random.choice(WORDS[difficulty])
    st.session_state.guessed = set()
    st.session_state.lives = 6
    st.session_state.score = 0
    st.session_state.hint_used = False
    st.session_state.game_started = True

def display_word():
    return " ".join(
        letter if letter in st.session_state.guessed else "_"
        for letter in st.session_state.word
    )

# ------------------ UI ------------------
st.title("🎮 Advanced Word Guessing Game")

difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

if st.button("Start Game"):
    start_game(difficulty)

if st.session_state.game_started:
    st.subheader("🔤 Guess the Word")
    st.markdown(f"### `{display_word()}`")

    st.info(f"❤️ Lives: {st.session_state.lives} | ⭐ Score: {st.session_state.score}")

    guess = st.text_input("Enter a letter", max_chars=1).lower()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Submit Guess"):
            if guess.isalpha() and len(guess) == 1:
                if guess not in st.session_state.guessed:
                    st.session_state.guessed.add(guess)
                    if guess in st.session_state.word:
                        st.success("✅ Correct!")
                        st.session_state.score += 10
                    else:
                        st.error("❌ Wrong!")
                        st.session_state.lives -= 1
                else:
                    st.warning("⚠️ Already guessed!")
            else:
                st.warning("⚠️ Enter one valid letter!")

    with col2:
        if st.button("Hint 💡"):
            if not st.session_state.hint_used:
                hint_letter = random.choice(
                    [l for l in st.session_state.word if l not in st.session_state.guessed]
                )
                st.session_state.guessed.add(hint_letter)
                st.session_state.hint_used = True
                st.info(f"Hint revealed: **{hint_letter}**")
            else:
                st.warning("Hint already used!")

    # ------------------ WIN / LOSE ------------------
    if all(letter in st.session_state.guessed for letter in st.session_state.word):
        st.balloons()
        st.success(f"🎉 You WON! Word: **{st.session_state.word}**")

    elif st.session_state.lives == 0:
        st.error(f"💀 Game Over! Word was **{st.session_state.word}**")

    if st.button("Restart Game 🔄"):
        st.session_state.game_started = False
