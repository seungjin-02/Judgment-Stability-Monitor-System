from dataclasses import dataclass
from judgment_log import JudgmentLog
from state_checks import (
    AMBIGUITY_THRESHOLD,
    TIME_PRESSURE_THRESHOLD,
    FATIGUE_THRESHOLD,
    REPEATED_REVISION_THRESHOLD,
    CONFIDENCE_CHANGE_THRESHOLD,
    has_high_ambiguity,
    has_high_time_pressure,
    has_high_fatigue,
    has_repeated_revision,
    has_confidence_change
)

@dataclass(frozen=True)
class StabilitySignal:
    name: str
    source_field: str
    observed_value: int
    threshold: int
    reason: str

def build_stability_signals(log: JudgmentLog) -> list[StabilitySignal]:
    signals: list[StabilitySignal] = []

    if has_high_ambiguity(log):
        signals.append(
            StabilitySignal(
                name = "high_ambiguity",
                source_field = "ambiguity_level",
                observed_value = log.ambiguity_level,
                threshold = AMBIGUITY_THRESHOLD,
                reason = "상황의 애매함이 높아 판단을 확정하기 전 기준과 필요한 정보를 다시 확인할 필요가 있습니다."
            )
        )
    if has_high_time_pressure(log):
        signals.append(
            StabilitySignal(
                name = "high_time_pressure",
                source_field = "time_pressure",
                observed_value = log.time_pressure,
                threshold = TIME_PRESSURE_THRESHOLD,
                reason = "시간 압박이 높아 판단을 빠르게 확정하려는 경향이 생길 수 있으므로 결정 전 최소 기준을 다시 확인할 필요가 있습니다."
            )
        )
    if has_high_fatigue(log):
        signals.append(
            StabilitySignal(
                name = "high_fatigue",
                source_field = "fatigue_level",
                observed_value = log.fatigue_level,
                threshold = FATIGUE_THRESHOLD,
                reason = "피로 또는 인지 부하가 높게 기록되었으므로 판단을 확정하기 전 검토 누락이 없는지 확인할 필요가 있습니다."
            )
        )
    if has_repeated_revision(log):
        signals.append(
            StabilitySignal(
                name = "repeated_revision",
                source_field = "revision_count",
                observed_value = log.revision_count,
                threshold = REPEATED_REVISION_THRESHOLD,
                reason = "같은 판단이 반복적으로 수정되고 있으므로 판단이 틀렸다는 의미는 아니지만 기준 자체를 다시 확인할 필요가 있습니다."
            )
        )
    if has_confidence_change(log):
        signals.append(
            StabilitySignal(
                name = "confidence_change",
                source_field = "confidence_change",
                observed_value = log.confidence_change,
                threshold = CONFIDENCE_CHANGE_THRESHOLD,
                reason = "판단에 대한 확신 변화가 크게 기뢱되었으므로 확정 전에 판단 근거를 다시 확인할 필요가 있습니다."
            )
        )

    return signals