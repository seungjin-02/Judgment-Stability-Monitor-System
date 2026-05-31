from dataclasses import dataclass
from enum import Enum
from stability_signals import StabilitySignal

class PauseState(str, Enum):
    CLEAR = "CLEAR"
    CHECK_NEEDED = "CHECK_NEEDED"
    PAUSE_SUGGESTED = "PAUSE_SUGGESTED"

@dataclass(frozen=True)
class PausePolicyResult:
    state: PauseState
    reason: str

def interpret_pause_policy(signals: list[StabilitySignal]) -> PausePolicyResult:
    signal_names = {signal.name for signal in signals}
    signal_count = len(signals)

    if _has_pressure_revision_combo(signal_names):
        return PausePolicyResult(
            state = PauseState.PAUSE_SUGGESTED,
            reason = "시간 압박과 반복 수정 신호가 함께 감지되었습니다. 판단이 틀렸다는 의미는 아니지만 확정 전 기준을 다시 확인할 필요가 있습니다."
        )
    elif signal_count == 0:
        return PausePolicyResult(
            state = PauseState.CLEAR,
            reason = "현재 기록된 상태값에서 뚜렷한 점검 신호가 발생하지 않았습니다."
        )
    elif signal_count <= 2:
        return PausePolicyResult(
            state = PauseState.CHECK_NEEDED,
            reason = "일부 상태 신호가 감지되었습니다. 판단을 확정하기 전 조건이나 기준을 확인할 필요가 있습니다."
        )
    else:
        return PausePolicyResult(
            state=PauseState.PAUSE_SUGGESTED,
            reason="여러 상태 신호가 함께 감지되었습니다. 바로 확정하기보다 잠시 멈추고 판단 기준과 근거를 다시 확인하는 것을 권장합니다."
        )

def _has_pressure_revision_combo(signal_names: set[str]) -> bool:
    return (
        "high_time_pressure" in signal_names and "repeated_revision" in signal_names
    )