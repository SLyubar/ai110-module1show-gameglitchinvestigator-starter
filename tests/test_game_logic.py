from streamlit.testing.v1 import AppTest

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

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


def test_range_for_easy_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_range_for_normal_difficulty():
    # Regression test: Normal and Hard ranges were swapped, giving Normal
    # the bigger range even though Hard has fewer attempts. Normal should
    # be the smaller, in-between range.
    assert get_range_for_difficulty("Normal") == (1, 50)


def test_range_for_hard_difficulty():
    # Regression test: Hard should have the bigger range since it also
    # has fewer attempts, making it the hardest setting overall.
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_valid_float_is_truncated():
    ok, value, err = parse_guess("42.9")
    assert ok is True
    assert value == 42


def test_parse_guess_empty_string_is_invalid():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_non_numeric_is_invalid():
    ok, value, err = parse_guess("banana")
    assert ok is False
    assert value is None
    assert err is not None


def test_update_score_win_awards_points():
    assert update_score(current_score=0, outcome="Win", attempt_number=1) == 80


def test_update_score_too_low_deducts_points():
    assert update_score(current_score=0, outcome="Too Low", attempt_number=1) == -5


def test_update_score_too_high_always_deducts_points():
    # Regression test: "Too High" used to alternate between +5 and -5
    # depending on whether attempt_number was even or odd, letting a wrong
    # guess sometimes award points. It should always deduct, like "Too Low".
    assert update_score(current_score=0, outcome="Too High", attempt_number=1) == -5
    assert update_score(current_score=0, outcome="Too High", attempt_number=2) == -5


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


def test_fresh_game_shows_full_attempts_before_any_guess():
    # Regression test: attempts used to be initialized to 1 instead of 0,
    # so "Attempts left" showed one fewer than attempt_limit before the
    # player had made any guess at all.
    at = AppTest.from_file("app.py")
    at.run()

    assert at.session_state.attempts == 0
    assert "Attempts left: 8" in at.info[0].value


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


def test_guess_prompt_matches_difficulty_range():
    # Regression test: the guess prompt used to hardcode "between 1 and 100"
    # no matter the difficulty, which was wrong for Easy (1-20) and Normal
    # (1-50). It should reflect the actual range for the selected difficulty.
    at = AppTest.from_file("app.py")
    at.run()

    at.selectbox[0].set_value("Easy").run()

    low, high = get_range_for_difficulty("Easy")
    assert f"between {low} and {high}" in at.info[0].value


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
