---
name: ppt-generation-enterprise
description: Use this skill when you need to generate enterprise-style PPT or PPTX files from structured outlines, Markdown decks, template inventories, or branded presentation themes. Supports outline-to-plan conversion, template-driven slide filling, theme configuration, and portable PPT generation workflows.
---

# PPT Generation Enterprise Skill

Primary operator doc: `WORKSHOP-INPUT-PLAYBOOK.md`

## Overview

This skill is a portable enterprise-focused fork of a PPT generation workflow. It is optimized for business presentations that need:

- consistent corporate layout
- brand-controlled typography and color
- predictable page types such as cover, comparison, step flow, capability matrix, deployment table, and risk/control slides
- conversion from a structured outline into a reusable intermediate plan
- template filling via inventory and replacement map

For AI Discovery Card Workshop scenarios, this skill should use a workshop-specific route rather than the generic Markdown outline route. The default output should be a customer-ready package: workshop deck plus lightweight MVP spec docs for fast frontend-shell prototyping.

The current workshop workflow is asset-first. Sparse现场输入 should select and tailor prebuilt assets instead of forcing the model to generate most of the deck content from scratch.

The initial content library should cover multiple reusable case families per lane instead of a single default scenario. At minimum, the system should support service, operations, security, and knowledge directions that are common for `consumer-electronics-iot` and `cross-border-ecommerce` customers.

The default visual style for workshop decks should reference the existing forum template language:

- strong title hierarchy with restrained enterprise color usage
- light content panels with centered text blocks when the content sits inside a visual card
- consistent shallow rounded corners across all panels
- conclusion banners and emphasis strips for the key takeaway of each page
- avoid oversized curvature or overly decorative shapes

## Recommended Route

Use the template-driven route by default:

### Default enterprise route

1. Parse the Markdown outline into `presentation-plan.json`
2. Choose a `template` and `theme`
3. Build `replacement-map.json` from the plan and template inventory
4. Fill the PPTX template or hand off the replacement map to a downstream PPTX writer

### AI Discovery Workshop route

Use this route when the source material comes from the workshop SOP, card photos, board notes, or a structured scenario summary:

1. Collect card photo plus short workshop fields such as customer type, scenario summary, target role, pain point, expected value, and prototype preference
2. Run `scripts/generate_workshop_package.py` as the default entrypoint
3. Let the pipeline create `Workspace/<客户名-场景名>/` automatically
4. For sparse input, let `scripts/compose_workshop_assets.py` select outline packs, reference cases, and content snippets
5. Generate `presentation-plan.json` with `scripts/workshop_to_plan.py`
6. Generate `需求PRD.md` and `方案设计.md` with `scripts/workshop_to_mvp_docs.py`
7. Build `replacement-map.json` with the workshop-aware layout map or render directly with the PPTX writer

The canonical live capture template is `examples/live-input-capture-template.json`. The simplest operator-facing guide is `WORKSHOP-INPUT-PLAYBOOK.md`.

Keep image-driven slide generation only as an optional compatibility route.

Do not use freeform Markdown as the system of record for workshop decks. If card recognition is partial, collect the missing business metadata instead of guessing.

## Inputs

Typical inputs include:

- a Markdown outline with `Page` sections
- extracted PPT content used as a source outline
- a template inventory JSON extracted from a PPTX
- a layout map defining which logical slot goes to which shape
- a theme JSON defining colors, fonts, accents, footer, and logo metadata

Workshop-specific input should be a normalized scenario JSON with these minimum sections:

- `workshop`: title, customer, industry, group name, date
- `scenario`: name, target users, business problem, improvement goal
- `current_process`: current-state workflow steps
- `pain_points`: highest-value bottlenecks to improve
- `selected_cards`: grouped by business scenario, input/perception, understanding/analysis, generation/interaction, execution/closure
- `ai_flow`: trigger, target steps, closure, narrative
- `product_mapping`: capability-to-product rows and delivery forms
- `business_value`: outcomes, KPIs, deliverables
- `poc`: scope, validation points, stakeholders, next actions

Sparse live event input may also start from a lighter schema with:

- `event_input.customer_type`
- `event_input.scenario_summary`
- `event_input.target_role`
- `event_input.current_pain_point`
- `event_input.expected_value`
- `event_input.prototype_preference`
- optional `mvp_spec.prototype_mode`
- optional `mvp_spec.primary_user`
- optional `mvp_spec.core_task`
- optional `mvp_spec.screens`
- optional `mvp_spec.modules`
- optional `mvp_spec.key_actions`
- optional `mvp_spec.style_keywords`
- optional `mvp_spec.tech_stack_preference`
- `detected_cards`
- optional `card_photo_paths`

When collecting this sparse input, follow these constraints:

- `customer_type` must identify one lane clearly.
- `scenario_summary` must be one sentence about one workflow.
- `target_role` should name one primary actor.
- `current_pain_point` should contain one urgent current-state problem.
- `expected_value` should contain one near-term business result.
- `prototype_preference` should be a short prototype label, not a paragraph.
- `detected_cards` should only contain cards actually observed or confidently inferred.

When expanding the asset library, add new reference cases under `content-packs/reference-cases/<lane>/` using the existing JSON schema. `scripts/compose_workshop_assets.py` will auto-discover those files and rank them by lane and keyword match.

For consumer electronics / IoT, the current asset library should not stop at after-sales service. It should also cover global operations, security governance, and knowledge-hub style scenarios that commonly appear in AI Discovery workshops.

## Output Artifacts

The standard workshop output root is `Workspace/`.

For each customer scenario, create one Chinese-named subdirectory:

- directory naming rule: `客户名称-场景名称`
- PPT naming rule: `客户名称-场景名称方案.pptx`

The default artifact set is:

- `Workspace/<客户名称-场景名称>/原始输入.json` or `场景输入.json`
- `Workspace/<客户名称-场景名称>/组合场景.json` when the source is sparse live input
- `Workspace/<客户名称-场景名称>/演示文稿方案.json`
- `Workspace/<客户名称-场景名称>/替换映射.json`
- `Workspace/<客户名称-场景名称>/需求PRD.md`
- `Workspace/<客户名称-场景名称>/方案设计.md`
- `Workspace/<客户名称-场景名称>/<客户名称-场景名称>方案.pptx`

## Supported Slide Types

The current implementation recognizes and/or maps these page patterns:

- `cover`
- `cover-workshop`
- `opportunity-summary`
- `company-intro`
- `capability-grid`
- `problem-statement`
- `comparison`
- `principles`
- `step-flow`
- `scenario`
- `table`
- `risk`
- `control`
- `conclusion`
- `scenario-summary`
- `as-is-pain-map`
- `capability-selection`
- `ai-flow-steps`
- `prototype-concept`
- `product-mapping-table`
- `business-value`
- `poc-next-step`

## Workshop Deck Narrative

For AI Discovery Workshop decks, the default slide order should be:

1. Cover
2. Business opportunity and why now
3. Current gap and priority pain point
4. Customer-built card workflow
5. Target AI Flow
6. Prototype concept
7. Product mapping and deliverables
8. Business value and validation assumptions
9. POC and next-step recommendation

## Notes

- Prefer template-driven generation for enterprise decks.
- Prefer the workshop route for all SOP-derived workshop scenarios.
- Prefer `scripts/generate_workshop_package.py` over manually chaining individual scripts for workshop delivery.
- Prefer the generated Markdown docs to stay lightweight and prototype-oriented instead of expanding into a full implementation specification.
- When rendering directly to PPTX, prefer centered content within background blocks and use a consistent small-radius rounded rectangle treatment.
- Keep themes and template geometry separate.
- Store only relative paths so the package can be moved into another project without edits.
- Add real template inventories under `templates/` as they become available.
