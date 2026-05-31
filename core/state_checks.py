from judgment_log import JudgmentLog

AMBIGUITY_THRESHOLD = 4
TIME_PRESSURE_THRESHOLD = 4
FATIGUE_THRESHOLD = 4
REPEATED_REVISION_THRESHOLD = 3
CONFIDENCE_CHANGE_THRESHOLD = 3

def has_high_ambiguity(log: JudgmentLog) -> bool:
    """
    상황의 애매함이 높은지 확인
    이 함수는 판단 내용의 옳고 그름을 평가하지 않으며
    오직 판단을 확정하기 전 상황이 충분히 명확하지 않을 수 있는지 확인한다
    """
    return log.ambiguity_level >= AMBIGUITY_THRESHOLD

def has_high_time_pressure(log: JudgmentLog) -> bool:
    """
    시간 압박이 높은지 확인
    시간 압박은 판단이 단순화되거나 성급하게 확정될 가능성을 높힐 수 잇으므로
    확정 전 확인이 필요한 상태 신호로 다룬다
    """
    return log.time_pressure >= TIME_PRESSURE_THRESHOLD

def has_high_fatigue(log: JudgmentLog) -> bool:
    """
    피로 또는 인지 부하가 높은지 확인
    이 함수는 사용자의 능력이나 성향을 평가하지 않는다
    현재 판단 상태에서 피로 신호가 있는지만 확인한다
    """
    return log.fatigue_level >= FATIGUE_THRESHOLD

def has_repeated_revision(log: JudgmentLog) -> bool:
    """
    같은 판단을 반복적으로 수정하는지 확인
    반복 수정은 판단이 틀렸다는 뜻은 아니라
    하지만 판단 기준을 다시 확인할 필요가 있는 상태 신호이다
    """
    return log.revision_count >= REPEATED_REVISION_THRESHOLD

def has_confidence_change(log: JudgmentLog) -> bool:
    """
    확신 변화가 큰지 확인
    확신 변화는 판단 품질 평가가 아니라
    판단 근거를 다시 확인할 필요가 있는 상태 신호이다
    """
    return log.confidence_change >= CONFIDENCE_CHANGE_THRESHOLD