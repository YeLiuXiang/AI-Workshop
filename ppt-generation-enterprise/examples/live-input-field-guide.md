# Live Workshop Input Field Guide

Use this guide when collecting sparse live input before running `scripts/compose_workshop_assets.py`.

## Collection Goal

The live input is not expected to describe the full solution. Its job is to do three things well:

1. identify the customer lane
2. identify the highest-value problem family
3. hint the preferred prototype shape

If these three are clear, the asset-first workflow can safely select and tailor a reusable reference case.

## Canonical File

Start from `examples/live-input-capture-template.json`.

Keep the structure unchanged. Fill values into the existing fields rather than adding ad hoc fields.

## Field Rules

`workshop.customer`

- Fill the actual customer or brand name.
- If the name cannot be shared, use a stable alias such as `某出海智能硬件客户`.

`workshop.industry`

- Use the business-facing label shown in the workshop, for example `消费电子 IoT` or `跨界电商`.
- Do not use overly broad labels such as `制造业` unless the workshop is really that generic.

`event_input.customer_type`

- This is the strongest lane signal.
- Prefer one short label only, such as `消费电子 IoT` or `跨界电商`.
- Do not mix multiple lanes in one value.

`event_input.scenario_summary`

- One sentence only.
- Use the pattern: `希望针对 <业务环节>，设计一个能结合 <关键数据/资料> 的 AI <流程/场景>.`
- Keep it concrete. Mention the workflow and the key inputs.
- Good example: `希望针对设备接入安全场景，设计一个能结合认证日志、证书状态和审计事件的 AI 风险治理流程。`
- Avoid vague summaries such as `想做一个 AI 平台`.

`event_input.target_role`

- Fill the person who will act on the output, not every stakeholder.
- Use one primary role such as `售后负责人`, `安全负责人`, `全球运营负责人`, `营销负责人`.

`event_input.current_pain_point`

- Describe one urgent pain point only.
- Prefer one sentence with current-state friction and impact.
- Good example: `各区域指标口径不统一，区域异常和固件风险发现不及时。`
- Avoid bundling three unrelated issues into one field.

`event_input.expected_value`

- Describe the business result the customer wants to see first.
- Prefer one sentence with verbs such as `提升`, `缩短`, `降低`, `建立`.
- Good example: `希望建立统一的全球运营监控和动作协同机制。`

`event_input.prototype_preference`

- Use a concrete prototype shape if the customer already reacts positively to one.
- Prefer patterns such as `工作台`, `控制塔`, `助手`, `中枢`, `门户`, `看板`.
- If unknown, leave a short neutral placeholder such as `运营工作台` rather than a long explanation.

`current_process`

- Optional.
- Add 3 to 5 current-state steps only if they are already visible from the workshop board or facilitator notes.
- Do not invent this section when it is missing.

`detected_cards`

- Record only cards actually seen or clearly inferred from the workshop board.
- Use the five existing buckets only.
- The card names inside those buckets must come from the SOP card-type lists, not ad hoc scenario labels.
- A small but accurate card set is better than a large guessed card set.

`card_photo_paths`

- Optional.
- Only store relative or local file names that the operator can map back to the workshop image source.

## Minimum Required Set

If time is tight, collect these six fields first:

- `event_input.customer_type`
- `event_input.scenario_summary`
- `event_input.target_role`
- `event_input.current_pain_point`
- `event_input.expected_value`
- `event_input.prototype_preference`

This is the minimum set needed for reliable lane selection and case matching.

## Recommended Writing Pattern

When facilitating live workshops, collect the fields in this order:

1. customer type
2. scenario summary
3. target role
4. current pain point
5. expected value
6. prototype preference
7. detected cards

This order follows the way `compose_workshop_assets.py` selects lanes and scores reference cases.

## Anti-Patterns

- Do not paste long meeting notes into `scenario_summary`.
- Do not write multi-line paragraphs into `current_pain_point`.
- Do not mix customer request, solution idea, and KPI target into one field.
- Do not create new keys unless the scripts are updated to consume them.
- Do not use generic labels like `AI 赋能` as the only business description.

## Quick Check Before Running

Before running composition, confirm:

1. one clear lane is visible from `customer_type`
2. one clear problem family is visible from `scenario_summary` and `current_pain_point`
3. one usable prototype direction is visible from `prototype_preference`

If any of these three are missing, improve the input first instead of forcing generation.