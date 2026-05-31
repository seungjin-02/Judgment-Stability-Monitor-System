from dataclasses import asdict
import json
from judgment_log import JudgmentLog
from stability_signals import build_stability_signals
from pause_policy import interpret_pause_policy
from output_prompt import build_reflection_prompt

def run_judgment_stability_check(log: JudgmentLog) -> dict:
    signals = build_stability_signals(log)
    policy_result = interpret_pause_policy(signals)
    prompt = build_reflection_prompt(policy_result, signals)

    return {
        "log_id": log.log_id,
        "task_context": log.task_context,
        "note": log.note,
        "prompt": asdict(prompt)
    }

def print_result(result: dict) -> None:
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    log = JudgmentLog(
        log_id = "log_001",
        task_context = "deadline_sensitive_decision",
        ambiguity_level = 3,
        time_pressure = 5,
        fatigue_level = 2,
        revision_count = 4,
        confidence_change = 1,
        note = "시간 압박이 있고 같은 판단을 반복 수정하고 있는 상태"
    )

    result = run_judgment_stability_check(log)
    print_result(result)


