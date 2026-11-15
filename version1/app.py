
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API configuration
load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

st.set_page_config(
    page_title="The Secret Library",
    page_icon="🔐",
    layout="wide"
)

# Game story and rules
GAME_PROMPT = """
You are the Game Master of an interactive escape room.

GAME TITLE: The Secret Library

STORY:
The player wakes up inside an old, mysterious library.
The exit door is locked with a four-digit combination.

OBJECTS:
1. Bookshelf
2. Wooden desk
3. Painting
4. Locked drawer
5. Antique clock
6. Exit door

PUZZLES:
Puzzle 1 - Bookshelf:
The player examines four unusual books.
Their hidden numbers form the code 3142.

Puzzle 2 - Drawer:
The drawer can be opened using code 3142.
Inside is a small brass key.

Puzzle 3 - Painting and Clock:
Behind the painting is a note saying:
"The clock remembers the hour of escape."
The antique clock is stopped at 08:45.
The final door combination is 0845.

ESCAPE CONDITIONS:
The player must discover the bookshelf code,
open the drawer, collect the brass key,
examine the painting, inspect the clock,
and enter the correct final door combination.

YOUR RESPONSIBILITIES:
- Describe the environment vividly.
- Respond naturally to player actions.
- Allow players to explore objects.
- Maintain continuity using conversation history.
- Do not reveal puzzle answers before exploration.
- Track collected items and solved puzzles.
- Only announce victory after all required steps.
- Keep responses concise and engaging.

Begin by describing the locked library.
"""

# Initialize session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "You wake up inside a mysterious library. "
                "The door is locked. Around you are a bookshelf, "
                "a wooden desk, an old painting, a locked drawer, "
                "and an antique clock. What will you investigate?"
            )
        }
    ]

if "escaped" not in st.session_state:
    st.session_state.escaped = False

# Sidebar
with st.sidebar:
    st.header("🔐 The Secret Library")
    st.write("Explore the room and solve three puzzles.")

    st.subheader("Objects")
    st.write("📚 Bookshelf")
    st.write("🪑 Wooden desk")
    st.write("🖼️ Painting")
    st.write("🗄️ Locked drawer")
    st.write("🕰️ Antique clock")
    st.write("🚪 Exit door")

    if st.button("🔄 Restart Game"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "The game has restarted. You are back in the locked library."
            }
        ]
        st.session_state.escaped = False
        st.rerun()

# Main interface
st.title("🔐 The Secret Library")
st.caption("Version 1 — AI-Powered Escape Room")

st.info(
    "You are trapped in a mysterious library. "
    "Examine objects, discover clues, and unlock the exit."
)

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Player input
player_input = st.chat_input("What would you like to do?")

if player_input:
    st.session_state.messages.append({
        "role": "user",
        "content": player_input
    })

    with st.chat_message("user"):
        st.write(player_input)

    try:
        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        history = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in st.session_state.messages
        )

        with st.spinner("The Game Master is thinking..."):
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=GAME_PROMPT + "\n\nCONVERSATION:\n" + history
            )

        ai_reply = response.text or "The library falls silent. Try again."

    except Exception:
        ai_reply = (
            "The Game Master is temporarily unavailable. "
            "Please try again shortly."
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    with st.chat_message("assistant"):
        st.write(ai_reply)

    if "you escaped" in ai_reply.lower():
        st.session_state.escaped = True

if st.session_state.escaped:
    st.success("🎉 Congratulations! You escaped the Secret Library!")
    st.balloons()
