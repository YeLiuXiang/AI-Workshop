# Live Workshop Input Field Guide

Use this guide when collecting sparse live input before running `scripts/generate_workshop_package.py` or `scripts/compose_workshop_assets.py`.

## Collection Goal

The live input is not expected to describe the full solution. Its job is to do three things well:

1. identify the customer lane
2. identify the highest-value problem family
3. hint the preferred prototype shape

If these three are clear, the asset-first workflow can safely select and tailor a reusable reference case.

## Canonical File

Start from `examples/live-input-capture-template.json`.

Keep the structure unchanged. Fill values into the existing fields rather than adding ad hoc fields.
The template now includes an optional `mvp_spec` block used to generate `需求PRD.md` and `方案设计.md` for a frontend-shell prototype.

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

`mvp_spec.prototype_mode`

- Optional.
- Recommended default is `前端壳子优先`.
- Use this field when you want the generated spec package to explicitly stay lightweight and demo-oriented.

`mvp_spec.primary_user`

- Optional.
- Fill the person who will actually click through the prototype, such as `营销负责人` or `供应链负责人`.
- If omitted, the generator will fall back to the scenario target user.

`mvp_spec.core_task`

- Optional.
- Describe the single most important thing the prototype should help the user finish.
- Good example: `在一个页面中完成客群查看、文案生成和活动动作判断。`

`mvp_spec.screens`

- Optional.
- Add 3 to 5 page names only.
- Good examples: `首页总览`, `洞察分析页`, `生成结果页`, `动作建议页`.

`mvp_spec.modules`

- Optional.
- Add the main visible modules the page shell must contain.
- Good examples: `客群卡片`, `趋势图`, `推荐动作列表`, `内容生成面板`.

`mvp_spec.key_actions`

- Optional.
- Record the 3 to 5 click paths or demo actions you want available in the shell.
- Good examples: `切换客群`, `查看 AI 洞察`, `生成页面草稿`, `打开动作建议抽屉`.

`mvp_spec.sample_data`

- Optional.
- Use this when the future prototype should preload realistic fake data.
- Good examples: `客户画像样例`, `活动结果样例`, `高风险客户清单`.

`mvp_spec.style_keywords`

- Optional.
- Use 2 to 4 short style keywords only.
- Good examples: `企业级`, `简洁`, `卡片式布局`, `深色运营看板`.

`mvp_spec.tech_stack_preference`

- Optional.
- Use this if the team already prefers a frontend stack.
- Good example: `Next.js + Tailwind CSS`.

`mvp_spec.out_of_scope`

- Optional.
- Use this to explicitly mark what the first prototype should not do.
- Good examples: `不接真实后端接口`, `不做真实权限`, `不实现自动提交动作`.

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

If you also want a better prototype document package, add these fields when time allows:

- `mvp_spec.primary_user`
- `mvp_spec.core_task`
- `mvp_spec.screens`
- `mvp_spec.modules`
- `mvp_spec.key_actions`
- `mvp_spec.style_keywords`

## Recommended Writing Pattern

When facilitating live workshops, collect the fields in this order:

1. customer type
2. scenario summary
3. target role
4. current pain point
5. expected value
6. prototype preference
7. detected cards
8. MVP spec fields when the customer clearly wants a prototype shell

This order follows the way `compose_workshop_assets.py` selects lanes and scores reference cases.

## Anti-Patterns

- Do not paste long meeting notes into `scenario_summary`.
- Do not write multi-line paragraphs into `current_pain_point`.
- Do not mix customer request, solution idea, and KPI target into one field.
- Do not create new keys unless the scripts are updated to consume them.
- Do not use generic labels like `AI 赋能` as the only business description.
- Do not write `mvp_spec` as a full technical design. Keep it short and demo-oriented.

## Quick Check Before Running

Before running composition, confirm:

1. one clear lane is visible from `customer_type`
2. one clear problem family is visible from `scenario_summary` and `current_pain_point`
3. one usable prototype direction is visible from `prototype_preference`
4. if a frontend shell is expected, one clear demo path is visible from `mvp_spec.core_task` or `mvp_spec.key_actions`

If any of these signals are missing, improve the input first instead of forcing generation.