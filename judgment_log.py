from dataclasses import dataclass

@dataclass(frozen=True)
class JudgmentLog:
    """
    판단의 내용이 아니라, 판단을 확정하기 전의 상태 정보를 기록한다.
    이 모델은 사용자의 판단이 옳은지, 틀린지, 좋은지, 나쁜지를 평가하지 않는다.
    오직 판단 과정에서 점검이 필요한 상태 신호를 감지하기 위한 입력 데이터이다.
    """

    log_id: str             # 판단 기록 식별자
    task_context: str       # 상황 맥락
    ambiguity_level: int    # 애매함 정도
    time_pressure: int      # 시간 압박 정도
    fatigue_level: int      # 피로 또는 인지 부하 정도
    revision_count: int     # 같은 판단을 반복 수정한 횟수
    confidence_change: int  # 확신 변화 정도
    note: str = ""          # 자유 기록