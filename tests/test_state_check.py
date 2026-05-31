from judgment_log import JudgmentLog
from state_checks import (
    has_high_ambiguity,
    has_high_time_pressure,
    has_high_fatigue,
    has_repeated_revision,
    has_confidence_change,
)

def make_log(
    ambiguity_level: int = 2,
    time_pressure: int = 3,
    fatigue_level: int = 1,
    revision_count: int = 0,
    confidence_change: int = 1,
) -> JudgmentLog:
    return JudgmentLog(
        log_id = "test_log_001",
        task_context = "test_context",
        ambiguity_level = ambiguity_level,
        time_pressure = time_pressure,
        fatigue_level = fatigue_level,
        revision_count = revision_count,
        confidence_change = confidence_change,
        note = "",
    )

def test_high_ambiguity_detected():
    log = make_log(ambiguity_level=4)

    assert has_high_ambiguity(log) is True


def test_low_ambiguity_not_detected():
    log = make_log(ambiguity_level=3)

    assert has_high_ambiguity(log) is False


def test_high_time_pressure_detected():
    log = make_log(time_pressure=4)

    assert has_high_time_pressure(log) is True


def test_low_time_pressure_not_detected():
    log = make_log(time_pressure=3)

    assert has_high_time_pressure(log) is False


def test_high_fatigue_detected():
    log = make_log(fatigue_level=4)

    assert has_high_fatigue(log) is True


def test_low_fatigue_not_detected():
    log = make_log(fatigue_level=3)

    assert has_high_fatigue(log) is False


def test_repeated_revision_detected():
    log = make_log(revision_count=3)

    assert has_repeated_revision(log) is True


def test_low_revision_count_not_detected():
    log = make_log(revision_count=2)

    assert has_repeated_revision(log) is False


def test_confidence_change_detected():
    log = make_log(confidence_change=3)

    assert has_confidence_change(log) is True


def test_low_confidence_change_not_detected():
    log = make_log(confidence_change=2)

    assert has_confidence_change(log) is False