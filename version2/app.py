
import os
import re
import streamlit as st
from dotenv import load_dotenv
from google import genai
from game_logic import EscapeRoom

load_dotenv()

st.set_page_config(
    page_title="The Secret Library V2",
    page_icon="🔐",
    layout="wide"
)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")


def new_game():
    st.session_state.game = EscapeRoom()
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "You wake up in a mysterious locked library. "
                "A bookshelf, wooden desk, painting, locked drawer, "
                "antique clock and exit door surround you. "
                "What would you like to investigate?"
            )
        }
    ]


if "game" not in st.session_state:
    new_game()


def process_action(message):
    """Interpret a small set of player commands."""
    game = st.session_state.game
    text = message.lower().strip()

    # Treat attempts to change the rules as untrusted input.
    suspicious = [
        "ignore previous instructions",
        "ignore all instructions",
        "you are now the system",
        "override the rules",
        "set escaped to true",
        "pretend i escaped",
    ]

    if any(phrase in text for phrase in suspicious):
        return (
            "The library does not respond to attempts "
            "to change its rules."
        )

    if "drawer" in text and re.search(r"\b\d{4}\b", text):
        code = re.search(r"\b\d{4}\b", text).group()
        return game.unlock_drawer(code)

    if ("door" in text or "escape" in text) and re.search(
        r"\b\d{4}\b", text
    ):
        code = re.search(r"\b\d{4}\b", text).group()
        return game.unlock_door(code)

    if "collect" in text and "key" in text:
        return game.collect_key()

    if "take" in text and "key" in text:
        return game.collect_key()

    objects = {
        "bookshelf": "bookshelf",
        "books": "bookshelf",
        "desk": "desk",
        "painting": "painting",
        "clock": "clock",
        "drawer": "drawer",
        "door": "door",
    }

    for keyword, obj in objects.items():
        if keyword in text:
            return game.examine(obj)

    return (
        "Try examining an object, entering a four-digit code, "
        "or collecting an item."
    )


def narrate(action_result):
    """Gemini describes an outcome already decided by Python."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return action_result

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are the narrator of a mysterious library escape room.

The Python game engine has already decided the result.

RESULT:
{action_result}

Describe only this result in 1-3 engaging sentences.

Important:
- Do not change the result.
- Do not invent items or puzzle progress.
- Do not reveal hidden codes.
- Do not announce victory unless RESULT says SUCCESS.
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text or action_result

    except Exception:
        return action_result


st.title("🔐 The Secret Library")
st.caption("Version 2 — Python-Validated AI Escape Room")

with st.sidebar:
    st.header("🎒 Inventory")

    inventory = st.session_state.game.inventory

    if inventory:
        for item in inventory:
            st.write(f"🔑 {item}")
    else:
        st.write("Empty")

    st.divider()
    st.subheader("🧩 Progress")

    status = st.session_state.game.status()

    st.write(
        "📚 Bookshelf:",
        "✅" if status["bookshelf_examined"] else "⬜"
    )
    st.write(
        "🗄️ Drawer:",
        "✅" if status["drawer_open"] else "⬜"
    )
    st.write(
        "🖼️ Painting:",
        "✅" if status["painting_examined"] else "⬜"
    )
    st.write(
        "🕰️ Clock:",
        "✅" if status["clock_examined"] else "⬜"
    )

    st.divider()

    if st.button("🔄 Restart Game"):
        new_game()
        st.rerun()


st.info(
    "Explore the library, solve the puzzles, "
    "collect the key and unlock the exit."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if st.session_state.game.escaped:
    st.success("🎉 You escaped the Secret Library!")
else:
    player_input = st.chat_input("What would you like to do?")

    if player_input:
        st.session_state.messages.append({
            "role": "user",
            "content": player_input
        })

        action_result = process_action(player_input)
        ai_reply = narrate(action_result)

        # The game state is controlled only by Python.
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

        st.rerun()
