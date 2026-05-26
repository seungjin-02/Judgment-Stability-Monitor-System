from dataclasses import dataclass, field

@dataclass(frozen=True)
class StabilityOutput:
    """
    판단 상태 점검 결과를 표현한다.
    이 출력은 판단의 정답 여부를 말하지 않는다.
    사용자의 성향을 분류하지 않는다.
    판단 품질을 점수화하지 않는다.
    오직 판단을 확정하기 전 확인이 필요한 상태 신호가 있는지 표현한다.
    """

    log_id: str
    state: str
    signals: list[str] = field(default_factory=list)
    prompt: str = ""

