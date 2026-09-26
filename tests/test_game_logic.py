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
