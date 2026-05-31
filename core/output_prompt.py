from dataclasses import dataclass, field
from pause_policy import PausePolicyResult, PauseState
from stability_signals import StabilitySignal

@dataclass(frozen=True)
class OutputPrompt:
    state: PauseState
    title: str
    message: str
    signals: list[StabilitySignal] = field(default_factory=list)
    check_items: list[str] = field(default_factory=list)

def build_reflection_prompt(
    policy_result: PausePolicyResult,
    signals: list[StabilitySignal]
) -> OutputPrompt:
    return OutputPrompt(
        state = policy_result.state,
        title = _build_title(policy_result.state),
        message = policy_result.reason,
        signals = signals,
        check_items = _build_check_items(signals)
    )

def _build_title(state: PauseState) -> str:
    if state == PauseState.CLEAR:
        return "뚜렷한 점검 신호 없음"
    elif state == PauseState.CHECK_NEEDED:
        return "확정 전 기준 확인 필요"
    else:
        return "잠시 멈추고 기준 재확인 권장"

def _build_check_items(signals: list[StabilitySignal]) -> list[str]:
    if not signals:
        return [
            "현재 판단 기준이 명확한지 확인하기",
            "새로운 정보가 추가되었는지 확인하기"
        ]
    return [signal.reason for signal in signals]