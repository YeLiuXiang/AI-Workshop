You are running inside the workshop repository.

Task:

1. Read the request JSON at `{request_path}`.
2. Review the local workshop guidance files as needed, especially:
   - `WORKSHOP-INPUT-PLAYBOOK.md`
   - `README.md`
   - `examples/live-input-capture-template.json`
3. If image files are attached, use them as supporting context:
{image_paths}
4. Produce exactly one normalized workshop scenario JSON as your final answer.

Required output rules:

- The JSON must follow the canonical scenario structure expected by `scripts/generate_workshop_package.py`.
- Return valid UTF-8 JSON with no markdown fence.
- Keep all business-facing text in Chinese unless the input clearly requires English.
- Preserve customer intent from the request; do not invent unrelated scenarios.
- Do not modify repository files.
- The service will save your final JSON to `{scenario_output_path}`.

Expected top-level sections:

- `workshop`
- `scenario`
- `opportunity`
- `current_process`
- `pain_points`
- `selected_cards`
- `ai_flow`
- `product_mapping`
- `business_value`
- `poc`
- optional `prototype`
- optional `mvp_spec`

Input compatibility note:

- if `event_input.scene_name` exists, treat it as the preferred scenario title
- `event_input.scenario_summary` should remain the business description or workflow description

The `opportunity` section is required. Use this shape:

```json
{
  "statement": "一句话说明为什么这是值得优先验证的业务机会",
  "why_now": "一句话说明为什么现在值得做",
  "supporting_points": ["支撑点 1", "支撑点 2", "支撑点 3"]
}
```

When the request is sparse:

- infer the minimum missing structure needed by the workshop pipeline
- prefer concise, presentation-ready wording
- keep values deterministic and practical for workshop delivery
- avoid placeholders such as `待补充`
