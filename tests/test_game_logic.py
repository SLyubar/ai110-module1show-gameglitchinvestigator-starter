from streamlit.testing.v1 import AppTest

from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    # and the hint should tell the player to go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    # and the hint should tell the player to go HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_new_game_resets_state_after_loss():
    # Play a full game out to a loss, then click "New Game" and make
    # sure the app is actually playable again (status/score/history/attempts).
    at = AppTest.from_file("app.py")
    at.run()

    # app.py doesn't assign explicit keys to these buttons, so they're
    # addressed by position: col1 -> Submit Guess, col2 -> New Game.
    # Each widget reference is stale after a rerun, so re-fetch by index every time.
    attempt_limit = 8  # Normal difficulty is the default selectbox index
    for _ in range(attempt_limit):
        at.text_input(key="guess_input_Normal").set_value("-1")
        at.button[0].click().run()

    assert at.session_state.status == "lost"
    assert at.session_state.score != 0 or at.session_state.attempts > 0

    at.button[1].click().run()

    assert at.session_state.status == "playing"
    assert at.session_state.attempts == 0
    assert at.session_state.score == 0
    assert at.session_state.history == []


def test_submit_updates_attempts_history_and_hint_together():
    # Regression test: pressing Enter in the guess box used to trigger a
    # rerun that only updated the text_input's value, leaving the guess
    # unprocessed (no attempt increment, no history entry, no hint) because
    # the button and text input were separate, unlinked widgets. Wrapping
    # them in an st.form means a single submission always updates attempts,
    # history, and the hint message together.
    at = AppTest.from_file("app.py")
    at.run()

    attempts_before = at.session_state.attempts

    at.text_input(key="guess_input_Normal").set_value("1000000")
    at.button[0].click().run()  # form's submit button

    assert at.session_state.attempts == attempts_before + 1
    assert at.session_state.history == [1000000]
    assert len(at.warning) == 1


def test_debug_score_matches_game_score_after_guess():
    # Regression test: the "Developer Debug Info" panel must show the
    # same score as the rest of the game on the same rerun. It used to
    # render before update_score() ran, so it displayed a stale,
    # one-guess-behind score instead of the current one.
    at = AppTest.from_file("app.py")
    at.run()

    # A guess this high is always "Too High" no matter the random secret
    # (Normal difficulty range is 1-100), and it's the first attempt, so
    # update_score deterministically subtracts 5.
    at.text_input(key="guess_input_Normal").set_value("1000000")
    at.button[0].click().run()

    assert at.session_state.score == -5

    debug_score_line = at.expander[0].markdown[2].value
    assert f"`{at.session_state.score}`" in debug_score_line
