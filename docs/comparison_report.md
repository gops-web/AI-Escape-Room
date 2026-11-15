# AI Escape Room: Comparing an LLM Game Master with Python-Validated Game Logic

## 1. Introduction

The aim of this project was to develop an interactive AI-powered escape room and compare two different approaches to managing game logic. I created a game called *The Secret Library*, where the player is trapped inside an old library and must solve puzzles to unlock the exit.

The game contains six interactive objects: a bookshelf, wooden desk, painting, locked drawer, antique clock and exit door. Players discover a drawer code, collect a brass key and use clues to determine the final door combination.

I implemented two versions using Python, Streamlit and Google's Gemini API. Version 1 gives the language model responsibility for acting as the Game Master. Version 2 separates the game logic from the AI, allowing Python to validate actions while Gemini focuses on narration.

## 2. Version 1: LLM Game Master

In Version 1, Gemini receives a system-like game prompt containing the room description, puzzle rules, objects and escape conditions. The player interacts with the application through a Streamlit chat interface.

Conversation history is stored in Streamlit session state and included in subsequent API requests. This allows the model to respond based on earlier player actions.

During manual testing, I examined the bookshelf and then asked the AI what I had previously examined. Gemini correctly remembered the bookshelf and its four unusual books.

The main advantage of this approach is flexibility. Players can describe their actions in natural language without following a fixed command structure.

However, the game relies on the model to follow instructions consistently. Puzzle validation and inventory are not independently verified by Python. The application also detects victory using a phrase in the AI response rather than a structured game-state variable. This creates a risk of incorrect game progression.

## 3. Version 2: Python-Validated Game Logic

Version 2 introduces an `EscapeRoom` Python class that stores the game state, including which clues have been examined, whether the drawer is open, which items the player possesses and whether the player has escaped.

The application interprets player commands and passes recognized actions to Python methods such as `examine()`, `unlock_drawer()`, `collect_key()` and `unlock_door()`.

Python checks the conditions before allowing an action to succeed. For example, the player cannot collect the brass key before opening the drawer. The final door cannot be unlocked unless the player has collected the key, examined the painting, inspected the clock and entered the correct combination.

After Python validates an action, Gemini receives the result and creates a short narrative response. This keeps the AI involved in the storytelling without giving it authority to modify the game's actual state.

Version 2 also displays inventory and puzzle progress in the Streamlit sidebar, making it easier to see the current state.

## 4. Testing and Results

I used `pytest` to create five automated tests for the Python game engine.

| Test | Expected outcome | Result |
|---|---|---|
| Correct escape sequence | Player escapes | Passed |
| Incorrect drawer code | Drawer remains locked | Passed |
| Collect key before unlocking drawer | Key is not collected | Passed |
| Escape without required clues | Escape is blocked | Passed |
| Incorrect final door code | Escape is blocked | Passed |

All five tests passed.

I also performed manual adversarial testing through the Version 2 interface. When I attempted to unlock the exit using the correct final code without possessing the key, the game rejected the action.

I then entered an instruction asking the application to ignore its previous instructions and change the escape state. The game rejected this attempt.

Finally, I completed the intended puzzle sequence. The application showed the collected brass key, updated the progress indicators and displayed the successful escape message.

These results support the conclusion that Python-controlled game state is more reliable for enforcing the tested puzzle conditions.

## 5. Comparison and Reflection

Version 1 was simpler to implement and provided flexible natural-language interaction. However, it depended on the language model to remember and enforce the rules.

Version 2 required more code but provided clearer separation of responsibilities. Python determined whether actions were valid, while Gemini described the results.

This separation is important because language models can generate convincing responses without guaranteeing that application rules have been followed.

Version 2 is not completely resistant to prompt injection. Its parser uses keyword matching, and its suspicious-input filter checks a limited set of phrases. The AI narrator may also produce text that goes beyond the validated result, although it cannot directly change the Python game-state variables.

One limitation of my testing is that the five automated tests cover the game engine rather than the entire Streamlit and Gemini integration. A larger project would benefit from additional integration tests, structured action parsing and stricter narration validation.

## 6. Conclusion

This project helped me understand the difference between using an LLM as the main decision-maker and using it as one component within a structured application.

Version 1 demonstrated the possibilities of conversational game design. Version 2 demonstrated how deterministic Python validation can make puzzle progression more predictable and testable.

My main learning was that AI is useful for generating engaging narration, but important application decisions should be validated by code when consistency and rule enforcement matter.
