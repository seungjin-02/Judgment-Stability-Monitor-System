from judgment_log import JudgmentLog

AMBIGUITY_THRESHOLD = 4
TIME_PRESSURE_THRESHOLD = 4
FATIGUE_THRESHOLD = 4
REPEATED_REVISION_THRESHOLD = 3
CONFIDENCE_CHANGE_THRESHOLD = 3

def has_high_ambiguity(log: JudgmentLog) -> bool:
    
    return log.ambiguity_level >= AMBIGUITY_THRESHOLD

def has_high_time_pressure(log: JudgmentLog) -> bool:

    return log.time_pressure >= TIME_PRESSURE_THRESHOLD

def has_high_fatigue(log: JudgmentLog) -> bool:

    return log.fatigue_level >= FATIGUE_THRESHOLD

def has_repeated_revision(log: JudgmentLog) -> bool:

    return log.revision_count >= REPEATED_REVISION_THRESHOLD

def has_confidence_change(log: JudgmentLog) -> bool:

    return log.confidence_change >= CONFIDENCE_CHANGE_THRESHOLD
