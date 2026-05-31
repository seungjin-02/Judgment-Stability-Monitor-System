from judgment_log import JudgmentLog
from stability_signals import StabilitySignal, build_stability_signals

def make_log(
    ambiguity_level: int = 1,
    time_pressure: int = 1,
    fatigue_level: int = 1,
    revision_count: int = 0,
    confidence_change: int = 0
) -> JudgmentLog:
    return JudgmentLog(
        log_id = "test_log",
        task_context= "test_context",
        ambiguity_level = ambiguity_level,
        time_pressure = time_pressure,
        fatigue_level = fatigue_level,
        revision_count = revision_count,
        confidence_change = confidence_change,
        note = ""
    )

def get_signal_names(signals: list[StabilitySignal]) -> list[str]:
    return [signal.name for signal in signals]

def test_no_signal():
    log = make_log()
    signals = build_stability_signals(log)

    assert signals == []

def test_high_ambiguity_signal():
    log = make_log(ambiguity_level = 4)
    signals = build_stability_signals(log)
    signal_names = get_signal_names(signals)

    assert "high_ambiguity" in signal_names

def test_high_time_pressure_signal():
    log = make_log(time_pressure = 4)
    signals = build_stability_signals(log)
    signal_names = get_signal_names(signals)

    assert "high_time_pressure" in signal_names

def test_high_fatigue_signal():
    log = make_log(fatigue_level = 4)
    signals = build_stability_signals(log)
    signal_names = get_signal_names(signals)

    assert "high_fatigue" in signal_names

def test_repeated_revision_signal():
    log = make_log(revision_count = 3)
    signals = build_stability_signals(log)
    signal_names = get_signal_names(signals)

    assert "repeated_revision" in signal_names

def test_confidence_change_signal():
    log = make_log(confidence_change = 3)
    signals = build_stability_signals(log)
    signal_names = get_signal_names(signals)

    assert "confidence_change" in signal_names

def test_multiple_signal():
    log = make_log(
        ambiguity_level = 4,
        time_pressure = 4,
        fatigue_level = 4,
        revision_count = 3,
        confidence_change = 3
    )
    signals = build_stability_signals(log)
    signal_names = get_signal_names(signals)

    assert signal_names[0] == "high_ambiguity"
    assert signals[1].source_field == "time_pressure"

    for signal in signals:
        if signal.name == "repeated_revision":
            repeated_revision_signal = signal

    assert repeated_revision_signal.source_field == "revision_count"
    assert repeated_revision_signal.observed_value == 3
    assert repeated_revision_signal.threshold == 3

def test_no_multiple_signal():
    log = make_log(
        ambiguity_level = 3,
        time_pressure = 3,
        fatigue_level = 3,
        revision_count = 2,
        confidence_change = 2
    )
    signals = build_stability_signals(log)

    assert signals == []






















