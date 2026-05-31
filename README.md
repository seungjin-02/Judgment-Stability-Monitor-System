# Judgment Stability Monitor System

Judgment Stability Monitor System은 판단의 옳고 그름을 평가하지 않고 판단을 확정하기 전 확인이 필요한 **상태 신호**를 감지하는 rule-based Mini MVP입니다.

이 프로젝트는 사용자의 판단이 맞는지, 틀렸는지, 좋은지, 나쁜지를 판단하지 않습니다. 또한 사용자의 성향을 분류하거나 판단 능력을 점수화하지 않습니다.

대신 **애매함, 시간 압박, 피로, 반복 수정, 확신 변화**와 같은 상태 신호를 기반으로 판단을 바로 확정하기 전에 기준과 근거를 다시 확인할 필요가 있는지 알려주는 것을 목표로 합니다.

---

## Project Position

이 프로젝트는 독립적인 대형 서비스 구현이 아니라 메인 프로젝트에서 사용한 판단을 대신하지 않는 구조화 패턴을 인간 판단 상태 점검 영역에 적용해본 Mini MVP입니다.

| Project                                   | Focus                                         |
| ----------------------------------------- | --------------------------------------------- |
| AI Decision Risk Signal Monitoring System | AI 의사결정 이벤트의 위험 신호와 불확실성 구조화 |
| Judgment Stability Monitor System         | 인간 판단 상태의 불안정 신호 구조화             |

두 프로젝트는 동일한 설계 철학을 공유하지만 다루는 대상과 출력 언어는 다릅니다.

---

## Core Idea

이 프로젝트의 핵심은 판단을 평가하거나 대신하는 것이 아니라 판단을 확정하기 전 현재 상태를 점검할 수 있도록 돕는 것입니다.

### 1. This project does not do

- 판단 평가 ❌
- 예측 ❌
- 성향 분석 ❌
- 결정 추천 ❌
- 판단 능력 점수화 ❌

### 2. This project does

- 상태 신호 감지 ⭕
- 기준 확인 유도 ⭕
- 잠시 멈춤 제안 ⭕
- 점검 근거 제공 ⭕

---

## System Flow

```text
JudgmentLog
→ State Checks
→ StabilitySignal
→ PausePolicyResult
→ ReflectionPrompt
```

| Step              | Role                                         |
| ----------------- | -------------------------------------------- |
| JudgmentLog       | 사용자가 기록한 판단 당시의 상태 입력           |
| State Checks      | 각 상태값이 감지 기준을 넘는지 확인             |
| StabilitySignal | 감지된 상태 신호를 구조화                        |
| PausePolicyResult | CLEAR / CHECK_NEEDED / PAUSE_SUGGESTED 상태 해석|
| ReflectionPrompt  | 판단 확정 전 확인할 메시지와 점검 항목 제공     |

---

## Input Model

`JudgmentLog`는 판단의 내용이 아니라 판단 당시의 상태를 기록합니다.

```python
@dataclass(frozen=True)
class JudgmentLog:
    log_id: str
    task_context: str
    ambiguity_level: int
    time_pressure: int
    fatigue_level: int
    revision_count: int
    confidence_change: int
    note: str = ""
```

| Field               | Meaning          |
| ------------------- | ---------------- |
| `log_id`            | 판단 기록 식별자        |
| `task_context`      | 판단이 이루어진 상황 맥락   |
| `ambiguity_level`   | 상황의 애매함 정도       |
| `time_pressure`     | 시간 압박 정도         |
| `fatigue_level`     | 피로 또는 인지 부하 정도   |
| `revision_count`    | 같은 판단을 반복 수정한 횟수 |
| `confidence_change` | 판단에 대한 확신 변화 정도  |
| `note`              | 사용자가 남긴 자유 기록    |


`note`는 현재 MVP에서 자동 분석하지 않습니다. 이는 자연어 기반 심리 추정이나 판단 평가로 확장되는 것을 방지하기 위한 의도적 제한입니다.

즉 `note`는 판단 로직에 사용되지 않고 사용자가 남긴 맥락 정보로만 보존됩니다.

---

## Level and Threshold

- 각 상태값은 사용자의 능력이나 판단 품질을 평가하기 위한 점수가 아닙니다.
- 각 값은 판단을 확정하기 전 현재 상태를 점검하기 위한 상태값 입니다.

### 1. 공통 범위 LEVEL

| Level | Meaning          |
| ----: | ---------------- |
|     0 | 해당 신호 없음         |
|     1 | 매우 낮음            |
|     2 | 낮음               |
|     3 | 보통 / 주의 시작       |
|     4 | 높음 / 점검 필요       |
|     5 | 매우 높음 / 강한 점검 신호 |

### 2. Current thresholds

| Field               | Threshold | Signal               |
| ------------------- | --------: | -------------------- |
| `ambiguity_level`   |    `>= 4` | `high_ambiguity`     |
| `time_pressure`     |    `>= 4` | `high_time_pressure` |
| `fatigue_level`     |    `>= 4` | `high_fatigue`       |
| `revision_count`    |    `>= 3` | `repeated_revision`  |
| `confidence_change` |    `>= 3` | `confidence_change`  |

각 threshold는 `state_checks.py`에서 관리합니다.

`stability_signals.py`는 이 기준을 참조하여 감지된 신호에 `observed_value`와 `threshold`를 함께 포함합니다.

---

## Stability Signal

감지된 상태 신호는 `StabilitySignal`로 구조화됩니다.

```python
@dataclass(frozen=True)
class StabilitySignal:
    name: str
    source_field: str
    observed_value: int
    threshold: int
    reason: str
```

| Field            | Meaning                                |
| ---------------- | -------------------------------------- |
| `name`           | 감지된 상태 신호 이름                    |
| `source_field`   | 어떤 입력 필드에서 나온 신호인지          |
| `observed_value` | 실제 입력된 값                          |
| `threshold`      | 해당 신호가 감지되는 기준값              |
| `reason`         | 왜 이 신호를 확인해야 하는지에 대한 설명  |

이 구조를 통해 최종 상태만 보여주는 것이 아니라 어떤 상태값이 어떤 기준을 넘어서 신호로 감지되었는지 투명하게 확인할 수 있습니다.

### Example

```json
{
  "name": "high_time_pressure",
  "source_field": "time_pressure",
  "observed_value": 5,
  "threshold": 4,
  "reason": "시간 압박이 높아 판단을 빠르게 확정하려는 경향이 생길 수 있으므로 결정 전 최소 기준을 다시 확인할 필요가 있습니다."
}
```

---

## Pause States

최종 상태는 세 가지로 구분됩니다.

| State             | Meaning                                                                                         |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| `CLEAR`           | 현재 기록된 상태값에서 뚜렷한 점검 신호가 감지되지 않은 상태                                         |
| `CHECK_NEEDED`    | 일부 상태 신호가 감지되어 판단 확정 전 조건이나 기준 확인이 필요한 상태                               |
| `PAUSE_SUGGESTED` | 여러 상태 신호 또는 강한 조합 신호가 감지되어 바로 확정하기보다 잠시 멈추고 기준 재확인이 권장되는 상태 |

`PAUSE_SUGGESTED`는 판단이 틀렸다는 의미가 아닙니다.

현재 상태에서 판단을 바로 확정하기보다 기준과 근거를 다시 확인하는 것이 좋다는 의미입니다.

---

## Pause Policy

현재 MVP의 상태 해석 규칙은 다음과 같습니다.

```text
signal_count == 0
→ CLEAR

signal_count == 1 or 2
→ CHECK_NEEDED

signal_count >= 3
→ PAUSE_SUGGESTED
```

단, 다음 조합은 신호 개수가 2개여도 `PAUSE_SUGGESTED`로 처리합니다.

```text
high_time_pressure + repeated_revision
→ PAUSE_SUGGESTED
```

이 조합은 시간 압박이 높은 상태에서 같은 판단을 반복 수정하고 있음을 의미합니다.

이는 판단이 틀렸다는 뜻이 아니라 확정 전 기준을 다시 확인할 필요가 크다는 신호입니다.

---

## Output Prompt

최종 출력은 `OutputPrompt`입니다.

```python
@dataclass(frozen=True)
class OutputPrompt:
    state: PauseState
    title: str
    message: str
    signals: list[StabilitySignal]
    check_items: list[str]
```

| Field         | Meaning                     |
| ------------- | --------------------------- |
| `state`       | 최종 점검 상태               |
| `title`       | 사용자에게 보여줄 짧은 제목   |
| `message`     | 상태 해석 메시지             |
| `signals`     | 감지된 StabilitySignal 목록 |
| `check_items` | 판단 확정 전 확인할 항목     |

특히 `signals`에는 감지된 `StabilitySignal`이 그대로 보존됩니다.

따라서 사용자는 최종 상태뿐 아니라 어떤 상태 신호 때문에 해당 상태가 나왔는지 확인할 수 있습니다.

---

## 10. Example Output

```json
{
  "log_id": "log_001",
  "task_context": "deadline_sensitive_decision",
  "note": "시간 압박이 있고 같은 판단을 반복 수정하고 있는 상태",
  "prompt": {
    "state": "PAUSE_SUGGESTED",
    "title": "잠시 멈추고 기준 재확인 권장",
    "message": "시간 압박과 반복 수정 신호가 함께 감지되었습니다. 판단이 틀렸다는 의미는 아니지만 확정 전 기준을 다시 확인할 필요가 있습니다.",
    "signals": [
      {
        "name": "high_time_pressure",
        "source_field": "time_pressure",
        "observed_value": 5,
        "threshold": 4,
        "reason": "시간 압박이 높아 판단을 빠르게 확정하려는 경향이 생길 수 있으므로 결정 전 최소 기준을 다시 확인할 필요가 있습니다."
      },
      {
        "name": "repeated_revision",
        "source_field": "revision_count",
        "observed_value": 4,
        "threshold": 3,
        "reason": "같은 판단이 반복적으로 수정되고 있으므로 판단이 틀렸다는 의미는 아니지만 기준 자체를 다시 확인할 필요가 있습니다."
      }
    ],
    "check_items": [
      "시간 압박이 높아 판단을 빠르게 확정하려는 경향이 생길 수 있으므로 결정 전 최소 기준을 다시 확인할 필요가 있습니다.",
      "같은 판단이 반복적으로 수정되고 있으므로 판단이 틀렸다는 의미는 아니지만 기준 자체를 다시 확인할 필요가 있습니다."
    ]
  }
}
```

---

## Design Boundary

이 프로젝트의 핵심 경계는 다음과 같습니다.

### 1. The system does

- 현재 입력된 상태값을 기준으로 판단 확정 전 점검 신호를 제공한다.
- 감지된 상태 신호와 기준값을 투명하게 보여준다.
- 판단 확정 전 기준과 근거를 다시 확인하도록 돕는다.

### 2. The system does not

- 사용자의 판단 내용 자체를 평가하지 않는다.
- 어떤 결정을 내려야 하는지 추천하지 않는다.
- 사용자의 성향이나 심리 상태를 추정하지 않는다.

즉 이 시스템은 판단자가 아닙니다.
판단을 확정하기 전 상태와 기준을 다시 확인하도록 돕는 구조화 도구입니다.

---

## Future Considerations

현재 버전에서는 다음 기능을 의도적으로 구현하지 않았습니다.

- note 자동 분석
- 개인별 threshold 조정
- 장기 기록 기반 패턴 분석
- UI 구현
- AI 기반 상태 추정

이 기능들은 프로젝트 범위를 크게 확장시키며 판단 평가나 심리 추정으로 오해될 가능성이 있습니다.

따라서 현재 MVP에서는 rule-based signal detection과 transparent output에 집중합니다.
