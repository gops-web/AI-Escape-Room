# 🔐 AI Escape Room — The Secret Library

An interactive, AI-powered escape room built using Python, Streamlit and Google Gemini.

## Project Overview

This project compares two approaches to building an AI-powered escape room.

**Version 1 — LLM Game Master:** Gemini manages the story, puzzles and game progression through natural-language conversation.

**Version 2 — Python-Validated Game:** Python controls puzzle validation, inventory and escape conditions, while Gemini narrates the results.

The objective is to understand how application architecture affects reliability, state management and resistance to attempts to bypass game rules.

## Game Story

The player wakes up inside a mysterious locked library and must explore the room, discover clues, solve puzzles, collect a brass key and unlock the exit.

The library contains six objects:

- Bookshelf
- Wooden desk
- Painting
- Locked drawer
- Antique clock
- Exit door

## Technologies

- Python
- Streamlit
- Google Gemini API
- python-dotenv
- pytest
- Git and GitHub

## Installation

1. Clone or download the repository.
2. Open the project folder.
3. Create a virtual environment:

   `python -m venv .venv`

4. Activate it on Windows:

   `.\.venv\Scripts\Activate.ps1`

5. Install dependencies:

   `pip install streamlit google-genai python-dotenv pytest`

6. Create a `.env` file in the project root with:

   `GEMINI_API_KEY=your_api_key_here`

   `GEMINI_MODEL=your_working_model_name`

Never commit your actual API key.

## Run Version 1

`python -m streamlit run version1/app.py`

## Run Version 2

`python -m streamlit run version2/app.py`

## Run Tests

`python -m pytest version2/test_game_logic.py -v`

## Testing

Five automated Python tests cover:

1. Successful escape after completing the required steps.
2. Incorrect drawer code.
3. Attempting to collect the key before opening the drawer.
4. Attempting to escape without the required clues and key.
5. Incorrect final door code.

Additional manual testing includes attempting to unlock the door early and entering a prompt-injection instruction.

## Key Findings

Version 1 supports flexible conversation but relies on the LLM to follow game rules and maintain consistent state.

Version 2 separates game logic from narration. Python decides whether actions are valid, while Gemini describes their outcomes.

This improves the reliability of game progression, although the prototype still has limitations in natural-language parsing and AI-generated narration.

## Security

The Gemini API key is stored locally in `.env`, which is excluded from Git using `.gitignore`.

## Author

Master's Data Science project — AI Escape Room Portfolio.
