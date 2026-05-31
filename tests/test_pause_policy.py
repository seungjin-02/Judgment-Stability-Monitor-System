from stability_signals import StabilitySignal
from pause_policy import PauseState, interpret_pause_policy

def make_signal(name: str) -> StabilitySignal:
    return StabilitySignal(
        name = name,
        source_field = "test_field",
        reason = "test reason"
    )

def test_no_signal():
    result = interpret_pause_policy([])

    assert result.state == PauseState.CLEAR

def test_one_signal():
    signals = [make_signal("high_ambiguity")]
    result = interpret_pause_policy(signals)

    assert result.state == PauseState.CHECK_NEEDED

def test_two_signals():
    signals = [
        make_signal("high_ambiguity"),
        make_signal("high_fatigue")
    ]
    result = interpret_pause_policy(signals)

    assert result.state == PauseState.CHECK_NEEDED

def test_three_signals():
    signals = [
        make_signal("high_ambiguity"),
        make_signal("high_fatigue"),
        make_signal("confidence_change")
    ]
    result = interpret_pause_policy(signals)

    assert result.state == PauseState.PAUSE_SUGGESTED

def test_pressure_revision_combo():
    signals = [
        make_signal("high_time_pressure"),
        make_signal("repeated_revision")
    ]
    result = interpret_pause_policy(signals)

    assert result.state == PauseState.PAUSE_SUGGESTED
