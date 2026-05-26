from dataclasses import dataclass

@dataclass(frozen=True)
class JudgmentLog:
    log_id: str             # 판단 기록 식별자
    task_context: str       # 상황 맥락
    ambiguity_level: int    # 애매함 정도
    time_pressure: int      # 시간 압박 정도
    fatigue_level: int      # 피로 또는 인지 부하 정도
    revision_count: int     # 같은 판단을 반복 수정한 횟수
    confidence_change: int  # 확신 변화 정도
    note: str = ""          # 자유 기록
