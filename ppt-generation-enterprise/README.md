# PPT Generation Enterprise

A portable PPT generation skill package for enterprise-style presentations.

This package now includes a workshop-specific route for AI Discovery Card Workshop outputs, where the default deliverable is a customer-ready package: PPT proposal plus lightweight MVP spec docs for fast frontend-shell prototyping.

## Doc Map

Use these three files as the main entry points:

- `README.md`: overall architecture and commands
- `SKILL.md`: workflow constraints and generation rules
- `WORKSHOP-INPUT-PLAYBOOK.md`: live workshop input guidance, examples, card-flow text, and scenario copy

## Goal

This package is a reusable fork of the current `ppt-generation` skill. It is designed for:

- outline-to-PPT workflows driven by structured Markdown
- enterprise presentation templates with stable layouts
- theme-based branding and color control
- template filling through inventory + replacement map
- optional post-processing rules for spacing and image-safe areas

## Architecture

The package is split into five layers:

1. `outline_to_plan.py`
   Parses Markdown outlines into a canonical `presentation-plan.json`.
2. `workshop_to_plan.py`
  Converts a normalized AI Discovery workshop scenario JSON into a deterministic `presentation-plan.json`.
3. `compose_workshop_assets.py`
  Merges sparse live workshop input with reusable outline packs, reference cases, and content snippets.
4. `build_replacement_map.py`
   Converts the plan into a template replacement map using a template inventory and layout map.
5. `templates/`
   Holds template-specific inventory, slot mapping, and layout rules.
6. `themes/`
   Holds brand tokens such as colors, fonts, logo, footer, and accent rules.
7. `workshop_to_mvp_docs.py`
  Converts a normalized workshop scenario JSON into `需求PRD.md` and `方案设计.md`.

The existing `scripts/generate.py` is included as the image-to-PPTX composer for compatibility. The primary enterprise route is template-driven rather than image-driven.

The current default workshop package should contain:

- a customer-ready PPT proposal
- `需求PRD.md`
- `方案设计.md`

The two Markdown files are intentionally lightweight and optimized for quick vibe coding of a frontend-only shell MVP.

## 5-Minute Mode

For live workshops, use the fast route when you need a usable result in under 5 minutes and do not want asset matching or replacement-map generation.

Recommended command:

```powershell
python scripts/generate_workshop_package.py `
  --input examples/live-fast-template.json `
  --workspace-root Workspace `
  --fast
```

Fast mode keeps only the essential path:

- sparse input -> deterministic normalized scenario
- normalized scenario -> PPT plan
- PPT plan -> PPTX
- normalized scenario -> `需求PRD.md` + `方案设计.md`

It skips reference-case selection and `替换映射.json` generation by default so现场输出更稳定、更快。

## Directory Layout

```text
ppt-generation-enterprise/
  SKILL.md
  README.md
  scripts/
    generate.py
    outline_to_plan.py
    compose_workshop_assets.py
    workshop_to_plan.py
    build_replacement_map.py
    generate_workshop_package.py
  content-packs/
    outlines/
    reference-cases/
    snippets/
  templates/
    enterprise-forum/
      README.md
      inventory.example.json
      layout-map.example.json
  themes/
    eden-enterprise/
      theme.json
  examples/
    ai-discovery-workshop-scenario.example.json
    live-input-capture-template.json
    live-input-field-guide.md
    live-sparse-consumer-electronics.json
    live-sparse-consumer-global-operations.json
    live-sparse-consumer-knowledge-hub.json
    live-sparse-consumer-security-governance.json
    live-sparse-consumer-visual-service.json
    live-sparse-cross-border.json
    live-sparse-cross-border-fulfillment.json
    office-efficiency-mini-outline.md
  Workspace/
```

## AI Discovery Workshop Route

Use this route when the source content is produced from the workshop SOP, card photo recognition, or structured facilitator notes.

The default workshop model is now `asset-first`: live input should be sparse and should mainly activate or tailor prebuilt assets rather than generate most of the deck from scratch.

Recommended flow:

1. Upstream recognition or manual整理 captures card photo plus short workshop fields
2. `generate_workshop_package.py` creates `Workspace/<客户名-场景名>/` and writes all standard artifacts there
3. For sparse live input, `compose_workshop_assets.py` selects the appropriate outline pack, reference case, and content snippets
4. `workshop_to_plan.py` generates the workshop deck plan
5. `build_replacement_map.py` binds the plan to the template inventory
6. `workshop_to_mvp_docs.py` generates `需求PRD.md` and `方案设计.md`
7. `plan_to_pptx.py` or a downstream PPTX writer renders the final deck

This route keeps recognition, asset selection, business composition, and template rendering decoupled.

## Standard Output Rule

From now on, the default workshop output root is `Workspace/`.

For every customer scenario, the project should create one Chinese-named subdirectory under `Workspace/`:

- directory naming rule: `客户名称-场景名称`
- PPT naming rule: `客户名称-场景名称方案.pptx`

Recommended artifact layout:

```text
Workspace/
  客户名称-场景名称/
    原始输入.json
    组合场景.json
    演示文稿方案.json
    替换映射.json
    需求PRD.md
    方案设计.md
    客户名称-场景名称方案.pptx
```

If the input is already a normalized scenario JSON, the folder may contain `场景输入.json` instead of `原始输入.json` and `组合场景.json`.

## Content Pack Model

The reusable content system is organized into:

- `content-packs/outlines/`: default narrative skeletons such as `opportunity-prototype-deck`
- `content-packs/reference-cases/`: industry and scenario specific reusable cases
- `content-packs/snippets/`: reusable value statements, next-step wording, and prototype phrasing

The first implementation focuses on two customer lanes:

- consumer electronics / IoT
- cross-border ecommerce

Representative cases already included:

- consumer electronics / IoT: after-sales service, predictive maintenance, visual field diagnosis, global operations, security governance, knowledge hub
- cross-border ecommerce: growth marketing, inventory and fulfillment, multilingual customer service

## Canonical Plan Schema

The generated `presentation-plan.json` uses this shape:

```json
{
  "title": "Presentation Title",
  "aspect_ratio": "16:9",
  "template": "enterprise-forum",
  "theme": "eden-enterprise",
  "slides": [
    {
      "slide_number": 1,
      "title": "Cover title",
      "subtitle": "Optional subtitle",
      "slide_type": "cover",
      "layout_key": "cover-basic",
      "key_points": ["Point A", "Point B"],
      "speaker_notes": ["note 1", "note 2"]
    }
  ]
}
```

For workshop decks, each slide may also contain structured `fields` such as `process_lines`, `pain_lines`, `mapping_lines`, `value_lines`, `kpi_lines`, and `next_action_lines` so the template layer can render stage-specific content without guessing from free text.

## Canonical Workshop Scenario Schema

The normalized workshop scenario input is expected to follow this shape:

```json
{
  "workshop": {
    "title": "AI Discovery Card Workshop",
    "customer": "客户名称",
    "industry": "行业",
    "group_name": "第 1 组",
    "date": "2026-05-07"
  },
  "scenario": {
    "name": "场景名称",
    "target_users": "目标用户",
    "business_problem": "业务问题",
    "improvement_goal": "改善目标"
  },
  "current_process": ["步骤 1", "步骤 2"],
  "pain_points": ["痛点 1", "痛点 2"],
  "selected_cards": {
    "business_scenario": ["卡片 A"],
    "input_perception": ["卡片 B"],
    "understanding_analysis": ["卡片 C"],
    "generation_interaction": ["卡片 D"],
    "execution_closure": ["卡片 E"]
  },
  "ai_flow": {
    "trigger": "业务触发",
    "steps": ["To-Be 步骤 1", "To-Be 步骤 2"],
    "closure": "闭环结果",
    "narrative": "供讲解或备注使用的完整描述"
  },
  "product_mapping": [
    {
      "capability": "能力点",
      "products": ["产品 A", "产品 B"],
      "delivery": "交付形式"
    }
  ],
  "business_value": {
    "outcomes": ["价值 1"],
    "kpis": ["指标 1"],
    "deliverables": ["交付物 1"]
  },
  "poc": {
    "scope": "POC 范围",
    "validation_points": ["验证点 1"],
    "stakeholders": ["角色 1"],
    "next_actions": ["动作 1"]
  }
}
```

For sparse live event input, use a lighter schema such as the examples under `examples/live-sparse-*.json`. That input should contain only the card workflow context and a few short descriptive fields, then be enriched by `compose_workshop_assets.py`.

If you also want a prototype-oriented delivery package, you may include an optional `mvp_spec` block in the input. Recommended fields are:

- `prototype_mode`
- `primary_user`
- `core_task`
- `screens`
- `modules`
- `key_actions`
- `sample_data`
- `style_keywords`
- `tech_stack_preference`
- `out_of_scope`

Use [WORKSHOP-INPUT-PLAYBOOK.md](f:/VsCodeProject/AI-Workshop/ppt-generation-enterprise/WORKSHOP-INPUT-PLAYBOOK.md) as the primary operator guide. Use [examples/live-input-capture-template.json](f:/VsCodeProject/AI-Workshop/ppt-generation-enterprise/examples/live-input-capture-template.json) as the canonical capture file.

Recommended collection rules:

- `customer_type` should identify one lane only.
- `scenario_summary` should be one concrete sentence about one workflow.
- `current_pain_point` should describe one urgent problem, not a paragraph.
- `expected_value` should describe the first business result the customer wants.
- `prototype_preference` should be a short prototype label such as `工作台`, `控制塔`, `助手`, or `中枢`.
- `mvp_spec` should stay lightweight and prototype-oriented rather than becoming a full technical design.

## Example Commands

Recommended end-to-end workshop command:

```powershell
python scripts/generate_workshop_package.py `
  --input examples/live-input-capture-template.json `
  --workspace-root Workspace
```

This command will automatically create one Chinese-named subdirectory under `Workspace/` and place the PPT and intermediate artifacts into that subdirectory.
The same command now also generates `需求PRD.md` and `方案设计.md` for a frontend-shell MVP handoff.

Lower-level commands are still available when you need to debug one stage manually.

Create a plan from an outline:

```powershell
python scripts/outline_to_plan.py `
  --input examples/office-efficiency-mini-outline.md `
  --output Workspace/示例方案/presentation-plan.json `
  --template enterprise-forum `
  --theme eden-enterprise
```

Create a workshop plan from a normalized scenario:

```powershell
python scripts/workshop_to_plan.py `
  --input examples/ai-discovery-workshop-scenario.example.json `
  --output Workspace/示例方案/presentation-plan.json `
  --template enterprise-forum `
  --theme eden-enterprise
```

Compose a workshop scenario from sparse live input and content packs:

```powershell
python scripts/compose_workshop_assets.py `
  --input examples/live-input-capture-template.json `
  --assets-dir content-packs `
  --output Workspace/示例方案/组合场景.json
```

Validate a different case family under the same lane:

```powershell
python scripts/compose_workshop_assets.py `
  --input examples/live-sparse-cross-border-fulfillment.json `
  --assets-dir content-packs `
  --output Workspace/跨境电商-库存与履约控制塔/组合场景.json
```

Validate a global operations / governance style consumer IoT case:

```powershell
python scripts/compose_workshop_assets.py `
  --input examples/live-sparse-consumer-global-operations.json `
  --assets-dir content-packs `
  --output Workspace/消费电子客户-全球设备运营/组合场景.json
```

Create a replacement map from a plan:

```powershell
python scripts/build_replacement_map.py `
  --plan Workspace/示例方案/presentation-plan.json `
  --inventory templates/enterprise-forum/inventory.example.json `
  --layout-map templates/enterprise-forum/layout-map.example.json `
  --output Workspace/示例方案/replacement-map.json
```

## Design Notes

- All file references are relative.
- Templates are page-type driven, not deck-specific.
- Theme data is separated from template geometry.
- The replacement map preserves source text styles from inventory and allows shrink rules.
- Workshop decks should prefer deterministic structured fields over keyword-based page inference.
- The generic Markdown parser remains a compatibility route, not the recommended SOP route.
- Sparse live input should select assets, not drive long freeform generation.
- The default workshop deck should explain business opportunity, AI flow, prototype direction, value, and next step.

## Next Recommended Extensions

1. Replace the example inventory with a real production PPT template inventory.
2. Expand the content pack library with more validated customer cases and outline variants.
3. Add workshop-specific table and flow geometries to the real template.
4. Add a direct PPTX writer that fills textboxes from the replacement map.
5. Add regression fixtures using real workshop scenarios from different industries.

## Service Layer

The repository now includes a cross-platform service wrapper under `workshop_service/`.

Use this when you want to:

- call the workshop pipeline from a frontend form
- keep the current Python generation chain
- optionally let Codex CLI normalize sparse input before PPT generation
- run the same codebase on Windows now and Linux VM later

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the service:

```powershell
python -m workshop_service
```

The service will auto-load a project-local `.env` if present. Copy [.env.example](</f:/VsCodeProject/AI-Workshop/ppt-generation-enterprise/.env.example>) to `.env` and keep the same file on Windows and Ubuntu.

Shortcut scripts:

```powershell
./scripts/start_workshop_service.ps1
```

```bash
./scripts/start_workshop_service.sh
```

For Ubuntu VM deployment, start from [deploy/workshop-service.service.example](</f:/VsCodeProject/AI-Workshop/ppt-generation-enterprise/deploy/workshop-service.service.example>) and only replace the working directory, Python path, and Linux user.
For a step-by-step Linux rollout, use [deploy/ubuntu-migration.md](</f:/VsCodeProject/AI-Workshop/ppt-generation-enterprise/deploy/ubuntu-migration.md>) together with [deploy/nginx.workshop.conf.example](</f:/VsCodeProject/AI-Workshop/ppt-generation-enterprise/deploy/nginx.workshop.conf.example>).

Then open the built-in frontend at the service root:

```text
http://127.0.0.1:8000/
```

Main endpoints:

- `GET /healthz`
- `POST /api/jobs/json`
- `POST /api/jobs/form`
- `GET /api/jobs/{job_id}`
- `GET /api/jobs/{job_id}/artifacts`
- `GET /api/jobs/{job_id}/artifacts/{artifact_name}`

Recommended runtime modes:

- `python-fast`
  Directly runs the existing fast workshop path.
- `python-assets`
  Uses the existing asset composition path without Codex CLI.
- `codex-cli`
  Runs `codex exec` first to produce a normalized scenario JSON, then hands that JSON to the Python generator.

Recommended environment variables:

- `WORKSHOP_PROJECT_ROOT`
- `WORKSHOP_OUTPUT_ROOT`
- `WORKSHOP_JOB_ROOT`
- `WORKSHOP_DEFAULT_MODE`
- `CODEX_CLI_BIN`
- `CODEX_MODEL`
- `CODEX_REASONING_EFFORT`
- `CODEX_SANDBOX`
- `CODEX_APPROVAL_POLICY`
- `CODEX_USE_EPHEMERAL`
- `CODEX_SKIP_GIT_REPO_CHECK`
- `CODEX_FALLBACK_MODE`
- `PPT_ACCENT_IMAGE_DIR`
