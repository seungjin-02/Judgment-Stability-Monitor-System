from pause_policy import PausePolicyResult, PauseState
from output_prompt import build_reflection_prompt
from stability_signals import StabilitySignal

def test_clear_policy_prompt():
    policy_result = PausePolicyResult(
        state = PauseState.CLEAR,
        reason = "현재 기록된 상태값에서 뚜렷한 점검 신호가 감지되지 않았습니다."
        )
    signals = []
    prompt = build_reflection_prompt(policy_result, signals)

    assert prompt.state == PauseState.CLEAR
    assert prompt.title == "뚜렷한 점검 신호 없음"
    assert prompt.message == policy_result.reason
    assert prompt.signals == []
    assert prompt.check_items == [
        "현재 판단 기준이 명확한지 확인하기",
        "새로운 정보가 추가되었는지 확인하기"
    ]

def test_check_needed_policy_prompt():
    policy_result = PausePolicyResult(
        state = PauseState.CHECK_NEEDED,
        reason = "일부 상태 신호가 감지되었습니다. 판단을 확정하기 전 조건이나 기준을 확인할 필요가 있습니다."
    )
    signals = [
        StabilitySignal(
            name = "high_ambiguity",
            source_field = "ambiguity_level",
            reason = "상황의 애매함이 높아 판단을 확정하기 전 기준과 필요한 정보를 다시 확인할 필요가 있습니다."
        ),
        StabilitySignal(
            name = "confidence_change",
            source_field = "confidence_change",
            reason = "판단에 대한 확신 변화가 크게 기뢱되었으므로 확정 전에 판단 근거를 다시 확인할 필요가 있습니다."
        )
    ]
    prompt = build_reflection_prompt(policy_result, signals)

    assert prompt.state == PauseState.CHECK_NEEDED
    assert prompt.title == "확정 전 기준 확인 필요"
    assert prompt.message == policy_result.reason
    assert prompt.signals == signals
    assert prompt.check_items == [
        "상황의 애매함이 높아 판단을 확정하기 전 기준과 필요한 정보를 다시 확인할 필요가 있습니다.",
        "판단에 대한 확신 변화가 크게 기뢱되었으므로 확정 전에 판단 근거를 다시 확인할 필요가 있습니다."
    ]

def test_pause_suggested_policy_prompt():
    policy_result = PausePolicyResult(
        state = PauseState.PAUSE_SUGGESTED,
        reason = "여러 상태 신호가 함께 감지되었습니다. 바로 확정하기보다 잠시 멈추고 판단 기준과 근거를 다시 확인하는 것을 권장합니다."
    )
    signals = [
        StabilitySignal(
            name = "high_ambiguity",
            source_field = "ambiguity_level",
            reason = "상황의 애매함이 높아 판단을 확정하기 전 기준과 필요한 정보를 다시 확인할 필요가 있습니다."
        ),
        StabilitySignal(
            name="repeated_revision",
            source_field="revision_count",
            reason="같은 판단이 반복적으로 수정되고 있으므로 판단이 틀렸다는 의미는 아니지만 기준 자체를 다시 확인할 필요가 있습니다"
        ),
        StabilitySignal(
            name = "confidence_change",
            source_field = "confidence_change",
            reason = "판단에 대한 확신 변화가 크게 기뢱되었으므로 확정 전에 판단 근거를 다시 확인할 필요가 있습니다."
        )
    ]
    prompt = build_reflection_prompt(policy_result, signals)

    assert prompt.state == PauseState.PAUSE_SUGGESTED
    assert prompt.title == "잠시 멈추고 기준 재확인 권장"
    assert prompt.message == policy_result.reason
    assert prompt.signals == signals
    assert prompt.check_items == [
        "상황의 애매함이 높아 판단을 확정하기 전 기준과 필요한 정보를 다시 확인할 필요가 있습니다.",
        "같은 판단이 반복적으로 수정되고 있으므로 판단이 틀렸다는 의미는 아니지만 기준 자체를 다시 확인할 필요가 있습니다",
        "판단에 대한 확신 변화가 크게 기뢱되었으므로 확정 전에 판단 근거를 다시 확인할 필요가 있습니다."
    ]

def test_pressure_revision_combo_policy_prompt():
    policy_result = PausePolicyResult(
        state = PauseState.PAUSE_SUGGESTED,
        reason = "시간 압박과 반복 수정 신호가 함께 감지되었습니다. 판단이 틀렸다는 의미는 아니지만 확정 전 기준을 다시 확인할 필요가 있습니다."
    )
    signals = [
        StabilitySignal(
            name  = "high_time_pressure",
            source_field = "time_pressure",
            reason = "시간 압박이 높아 판단을 빠르게 확정하려는 경향이 생길 수 있으므로 결정 전 최소 기준을 다시 확인할 필요가 있습니다."
        ),
        StabilitySignal(
            name = "repeated_revision",
            source_field = "revision_count",
            reason = "같은 판단이 반복적으로 수정되고 있으므로 판단이 틀렸다는 의미는 아니지만 기준 자체를 다시 확인할 필요가 있습니다"
        )
    ]
    prompt = build_reflection_prompt(policy_result, signals)

    assert prompt.state == PauseState.PAUSE_SUGGESTED
    assert prompt.title == "잠시 멈추고 기준 재확인 권장"
    assert prompt.message == policy_result.reason
    assert prompt.signals == signals
    assert prompt.check_items == [
        "시간 압박이 높아 판단을 빠르게 확정하려는 경향이 생길 수 있으므로 결정 전 최소 기준을 다시 확인할 필요가 있습니다.",
        "같은 판단이 반복적으로 수정되고 있으므로 판단이 틀렸다는 의미는 아니지만 기준 자체를 다시 확인할 필요가 있습니다"
    ]










