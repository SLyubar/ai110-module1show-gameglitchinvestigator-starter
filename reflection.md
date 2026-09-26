# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game asked me to guess a number between 1 and 100 with a text box entry field. There is a hint enabled that tells me to go higher and lower after each guess. I was allowed 8 guesses and it defaulted to Normal difficulty.

- List at least two concrete bugs you noticed at the start  

The hints kept telling me to go higher even when I guessed 100 which is the upper bound limit on the range and it told me to go lower when it should have been go higher. The secret number was 56 so the hints were backwards. Additionally, the game said I had 8 attempts but ended after 7, the developer debug info shows 7 attempts, and the history only shows my first 5 guesses. The debug info says my score is -10 while the overall game score is -15. Lastly, clicking new game shows a console message but does not actually start a new game. More bugs were added below while fixing the initial ones.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error | Suspected Code Location
|-------|-------------------|-----------------|------------------------| ------------------------|
| Guessed 100 | Hint should say "Go Lower" | Hint says "Go Higher" | No errors | `app.py`, `check_guess` function
| Guessed 1 | Hint should say "Go Higher" | Hint says "Go Lower" | No errors | `app.py`, `check_guess` function
| Clicked "New Game" | New game starts| I'm stuck on the previous game's screen | "Game over. Start a new game to try again." | `app.py`
| Make a guess | Score changes after each guess | The developer debug score does not match the total game score | No errors | `app.py`
| Make a guess and press enter | Hint displays, attempts increase in debug mode, and the guess is added to the guess list | The attempt increases but no hint is displayed and the guess is not added to the guess list in debug info | No errors | `app.py`
| Change the game difficulty | The printed instructions display the different guess ranges | The guess ranges are hardcoded and always show between 1 and 100 | No errors | `app.py`
| No action taken | full attempts display in the UI based on difficulty | The actual attempts show 1 before any guesses are made | No errors | `app.py`

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code with Sonnet 5 only. I used Claude as a partner to identify bugs, suggest solutions, and implement tests and fixes with permission.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

The AI suggested changing the hint messaging for the check_guess function to fix the backward hint bug. I verified the result by asking Claude to create or update the test_game_logic.py file with tests. I validated that all tests passed.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

Claude suggested updating the logic for the parse_guess function to implement rounding. For example, if a user enters 49.9, the current logic truncates to 49 so they would get a "Too Low" message. Claude wanted to add rounding so this scenario would actually result in a "Win" message. I rejected this change and kept it as is because that guess is in fact too low. Granted the opposite scenario of a player guessing 50.1 would result in win so this may be more of a developer preference. It made more logical sense for me to either keep the truncation or not allow floats to begin with.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I had Claude generate tests and ensured they passed. I also tested the fix in the UI by trying to reproduce the original bug and verifying it no longer appears.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

I ran pytest after Claude fixed the high/low bug and confirmed the result passed. There were actually three related tests to check if the code correctly returned messages and outcomes for winning gueses, low guess, or high guesses. These tests showed that the code fixed worked as designed.
  
- Did AI help you design or understand any tests? How?

Yes, I asked Claude to generate tests or update existing tests to verify that the bugs were fixed. It explained the tests as it created them so I did not need further explanation.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
