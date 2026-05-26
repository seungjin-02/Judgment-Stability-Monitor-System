from dataclasses import asdict
import json
from judgment_log import JudgmentLog
from output import StabilityOutput

def print_output(output: StabilityOutput) -> None:
    print(json.dumps(asdict(output), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    log = JudgmentLog(
        log_id="j_001",
        task_context="project_decision",
        ambiguity_level=4,
        time_pressure=5,
        fatigue_level=3,
        revision_count=3,
        confidence_change=2,
        note="결정을 확정하기 전에 기준을 계속 바꾸고 있음",
    )

    output = StabilityOutput(
        log_id=log.log_id,
        state="PAUSE_SUGGESTED",
        signals=[
            "high_ambiguity",
            "high_time_pressure",
            "repeated_revision",
        ],
        prompt=(
            "현재 판단이 틀렸다는 의미는 아닙니다. 하지만 판단을 확정하기 전 기준을 다시 확인할 신호가 감지되었습니다."
        ),
    )
    print_output(output)