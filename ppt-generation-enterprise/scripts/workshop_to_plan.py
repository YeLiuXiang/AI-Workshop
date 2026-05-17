import argparse
import json
from pathlib import Path

from workshop_to_mvp_docs import normalize_mvp_spec


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ensure_text(value: object, placeholder: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return f"待补充：{placeholder}"


def ensure_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        items = []
        for entry in value:
            if isinstance(entry, str) and entry.strip():
                items.append(entry.strip())
            elif isinstance(entry, dict):
                candidate = entry.get("name") or entry.get("title") or entry.get("value")
                if isinstance(candidate, str) and candidate.strip():
                    items.append(candidate.strip())
        return items
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def numbered_lines(items: list[str], placeholder: str, limit: int | None = None) -> list[str]:
    if not items:
        return [f"1. 待补充：{placeholder}"]
    selected = items[:limit] if limit else items
    return [f"{index}. {item}" for index, item in enumerate(selected, start=1)]


def join_cards(items: list[str], placeholder: str) -> str:
    if not items:
        return f"待补充：{placeholder}"
    return " / ".join(items)


def format_mapping_rows(rows: object) -> list[str]:
    if not isinstance(rows, list) or not rows:
        return ["待补充：能力卡 -> 产品映射 -> 交付形式"]

    formatted = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        capability = ensure_text(row.get("capability") or row.get("card"), "能力卡")
        products_value = row.get("products")
        if isinstance(products_value, list):
            products = ", ".join([str(item).strip() for item in products_value if str(item).strip()])
        else:
            products = ensure_text(products_value, "产品")
        delivery = ensure_text(row.get("delivery") or row.get("deliverable"), "交付形式")
        formatted.append(f"{capability} -> {products} | 交付：{delivery}")

    return formatted or ["待补充：能力卡 -> 产品映射 -> 交付形式"]


def summarize_platforms(rows: object) -> str:
    if not isinstance(rows, list) or not rows:
        return "优先产品栈：待补充"

    products = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        value = row.get("products")
        if isinstance(value, list):
            products.extend([str(item).strip() for item in value if str(item).strip()])
        elif isinstance(value, str) and value.strip():
            products.append(value.strip())

    deduplicated = []
    for product in products:
        if product not in deduplicated:
            deduplicated.append(product)

    if not deduplicated:
        return "优先产品栈：待补充"
    return f"优先产品栈：{' / '.join(deduplicated[:4])}"


def combine_scope_lines(scope: object, validation_points: list[str]) -> str:
    scope_text = ensure_text(scope, "POC 范围")
    if not validation_points:
        return f"POC 聚焦：{scope_text}"
    return f"POC 聚焦：{scope_text}；优先验证 {validation_points[0]}"


def first_or_placeholder(items: list[str], placeholder: str) -> str:
    if items:
        return items[0]
    return f"待补充：{placeholder}"


def dedupe_items(items: list[str]) -> list[str]:
    deduped = []
    for item in items:
        if item and item not in deduped:
            deduped.append(item)
    return deduped


def shorten_text(value: str, limit: int = 28) -> str:
    text = value.strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def build_architecture_blocks(
    scenario_problem: str,
    business_cards: list[str],
    input_cards: list[str],
    understanding_cards: list[str],
    generation_cards: list[str],
    execution_cards: list[str],
    flow_steps: list[str],
    flow_closure: str,
    prototype_name: str,
    prototype_mock_scope: list[str],
) -> list[str]:
    input_summary = " / ".join((business_cards + input_cards)[:3]) or scenario_problem
    analysis_summary = " / ".join((understanding_cards + generation_cards)[:3]) or "；".join(flow_steps[:2])
    workspace_summary = prototype_name
    if prototype_mock_scope:
        workspace_summary = f"{prototype_name}，覆盖{'、'.join(prototype_mock_scope[:2])}"
    feedback_summary = " / ".join(execution_cards[:2]) or flow_closure

    return [
        f"场景输入：{shorten_text(input_summary, 30)}",
        f"智能分析：{shorten_text(analysis_summary, 30)}",
        f"业务工作台：{shorten_text(workspace_summary, 30)}",
        f"闭环反馈：{shorten_text(feedback_summary, 30)}",
    ]


def build_architecture_support_lines(product_mapping: list[dict], mapping_lines: list[str], flow_steps: list[str]) -> list[str]:
    support_lines = []
    for row in product_mapping[:3]:
        if not isinstance(row, dict):
            continue
        capability = ensure_text(row.get("capability"), "能力")
        delivery = ensure_text(row.get("delivery") or row.get("deliverable"), "交付")
        support_lines.append(f"{capability}：{delivery}")
    if not support_lines:
        support_lines = mapping_lines[:3]
    if flow_steps:
        support_lines.append(f"关键动作：{'；'.join(flow_steps[:2])}")
    return support_lines[:4]


def build_architecture_chips(product_mapping: list[dict]) -> list[str]:
    chips = []
    for row in product_mapping:
        if not isinstance(row, dict):
            continue
        capability = ensure_text(row.get("capability"), "")
        if capability and capability not in chips:
            chips.append(capability)
        products = row.get("products")
        if isinstance(products, list):
            for product in products:
                item = str(product).strip()
                if item and item not in chips:
                    chips.append(item)
        elif isinstance(products, str) and products.strip() and products.strip() not in chips:
            chips.append(products.strip())
    return chips[:6]


def make_slide(
    slide_number: int,
    title: str,
    slide_type: str,
    layout_key: str,
    key_points: list[str],
    speaker_notes: list[str] | None = None,
    subtitle: str = "",
    fields: dict | None = None,
) -> dict:
    normalized_points = [point for point in key_points if isinstance(point, str) and point.strip()]
    while len(normalized_points) < 3:
        normalized_points.append("")

    return {
        "slide_number": slide_number,
        "title": title,
        "subtitle": subtitle,
        "slide_type": slide_type,
        "layout_key": layout_key,
        "key_points": normalized_points,
        "speaker_notes": speaker_notes or [],
        "summary_lines": normalized_points[:2],
        "slots": {
            "point_1": normalized_points[0],
            "point_2": normalized_points[1],
            "point_3": normalized_points[2],
        },
        "fields": fields or {},
    }


def build_workshop_plan(payload: dict, template: str, theme: str, aspect_ratio: str) -> dict:
    workshop = payload.get("workshop", {})
    scenario = payload.get("scenario", {})
    opportunity = payload.get("opportunity", {}) if isinstance(payload.get("opportunity"), dict) else {}
    current_process = ensure_list(payload.get("current_process"))
    pain_points = ensure_list(payload.get("pain_points"))
    selected_cards = payload.get("selected_cards", {}) if isinstance(payload.get("selected_cards"), dict) else {}
    ai_flow = payload.get("ai_flow", {}) if isinstance(payload.get("ai_flow"), dict) else {}
    prototype = payload.get("prototype", {}) if isinstance(payload.get("prototype"), dict) else {}
    product_mapping = payload.get("product_mapping", [])
    business_value = payload.get("business_value", {}) if isinstance(payload.get("business_value"), dict) else {}
    poc = payload.get("poc", {}) if isinstance(payload.get("poc"), dict) else {}
    selected_assets = payload.get("selected_assets", {}) if isinstance(payload.get("selected_assets"), dict) else {}
    mvp_spec = normalize_mvp_spec(payload)

    workshop_title = ensure_text(workshop.get("title"), "Workshop 标题")
    customer = ensure_text(workshop.get("customer"), "客户名称")
    industry = ensure_text(workshop.get("industry"), "行业")
    group_name = ensure_text(workshop.get("group_name"), "小组名称")
    event_date = ensure_text(workshop.get("date"), "活动日期")

    scenario_name = ensure_text(scenario.get("name"), "业务场景")
    scenario_target = ensure_text(scenario.get("target_users"), "目标用户")
    scenario_problem = ensure_text(scenario.get("business_problem"), "业务问题")
    scenario_goal = ensure_text(scenario.get("improvement_goal"), "改善目标")

    opportunity_statement = ensure_text(opportunity.get("statement"), "业务机会")
    opportunity_why_now = ensure_text(opportunity.get("why_now"), "Why Now")
    opportunity_supporting_points = ensure_list(opportunity.get("supporting_points"))

    business_cards = ensure_list(selected_cards.get("business_scenario"))
    input_cards = ensure_list(selected_cards.get("input_perception"))
    understanding_cards = ensure_list(selected_cards.get("understanding_analysis"))
    generation_cards = ensure_list(selected_cards.get("generation_interaction"))
    execution_cards = ensure_list(selected_cards.get("execution_closure"))

    flow_trigger = ensure_text(ai_flow.get("trigger"), "业务触发")
    flow_steps = ensure_list(ai_flow.get("steps"))
    flow_closure = ensure_text(ai_flow.get("closure"), "业务闭环")
    flow_narrative = ensure_text(ai_flow.get("narrative"), "AI Flow 描述")

    prototype_name = ensure_text(prototype.get("name"), "原型名称")
    prototype_goal = ensure_text(prototype.get("goal"), "原型目标")
    prototype_surface = ensure_text(prototype.get("surface"), "原型形态")
    prototype_user_flow = ensure_list(prototype.get("user_flow"))
    prototype_mock_scope = ensure_list(prototype.get("mock_scope"))
    prototype_value_statement = ensure_text(prototype.get("value_statement"), "原型价值")

    value_outcomes = ensure_list(business_value.get("outcomes"))
    value_kpis = ensure_list(business_value.get("kpis"))
    value_deliverables = ensure_list(business_value.get("deliverables"))

    poc_scope = ensure_text(poc.get("scope"), "POC 范围")
    poc_validation = ensure_list(poc.get("validation_points"))
    poc_stakeholders = ensure_list(poc.get("stakeholders"))
    poc_next_actions = ensure_list(poc.get("next_actions"))

    mapping_lines = format_mapping_rows(product_mapping)
    platform_line = summarize_platforms(product_mapping)
    architecture_blocks = build_architecture_blocks(
        scenario_problem,
        business_cards,
        input_cards,
        understanding_cards,
        generation_cards,
        execution_cards,
        flow_steps,
        flow_closure,
        prototype_name,
        prototype_mock_scope,
    )
    architecture_support_lines = build_architecture_support_lines(product_mapping, mapping_lines, flow_steps)
    architecture_chips = build_architecture_chips(product_mapping)
    deliverable_line = f"现场交付物：{join_cards(value_deliverables, '现场交付物')}"
    cover_value_line = prototype_value_statement or opportunity_statement or flow_narrative
    cover_title = scenario_name
    cover_subtitle = "AI Discovery Workshop 商机与原型方案"

    slides = [
        {
            "slide_number": 1,
            "title": cover_title,
            "subtitle": cover_subtitle,
            "slide_type": "cover-workshop",
            "layout_key": "cover-workshop",
            "key_points": [
                f"客户：{customer} | 行业：{industry}",
                f"小组：{group_name} | 日期：{event_date}",
                f"Workshop：{workshop_title}",
            ],
            "speaker_notes": [flow_narrative],
            "summary_lines": [
                f"客户：{customer} | 行业：{industry}",
                f"小组：{group_name} | 日期：{event_date}",
            ],
            "slots": {
                "point_1": f"客户：{customer} | 行业：{industry}",
                "point_2": f"小组：{group_name} | 日期：{event_date}",
                "point_3": f"Workshop：{workshop_title}",
            },
            "eyebrow": "AI DISCOVERY WORKSHOP",
            "title_lines": [cover_title, cover_subtitle],
            "footer": customer,
            "fields": {
                "customer_line": f"客户：{customer} | 行业：{industry}",
                "group_line": f"小组：{group_name} | 日期：{event_date}",
                "workshop_line": f"Workshop：{workshop_title}",
                "cover_value_line": cover_value_line,
            },
        },
        make_slide(
            2,
            "当前差距与优先痛点",
            "as-is-pain-map",
            "as-is-pain-map",
            [
                f"现状流程：{'；'.join(numbered_lines(current_process, '现状流程', limit=4))}",
                f"关键痛点：{'；'.join(numbered_lines(pain_points, '关键痛点', limit=3))}",
                f"优先切口：{first_or_placeholder(pain_points, '优先改造环节')}",
            ],
            fields={
                "process_lines": numbered_lines(current_process, "现状流程", limit=4),
                "pain_lines": numbered_lines(pain_points, "关键痛点", limit=3),
                "focus_line": f"优先切口：{first_or_placeholder(pain_points, '优先改造环节')}",
            },
        ),
        make_slide(
            3,
            "业务机会与 Why Now",
            "opportunity-summary",
            "opportunity-summary",
            [
                f"机会判断：{opportunity_statement}",
                f"为什么是现在：{opportunity_why_now}",
                f"价值支撑：{first_or_placeholder(opportunity_supporting_points, '价值支撑点')}",
            ],
            fields={
                "opportunity_line": f"机会判断：{opportunity_statement}",
                "why_now_line": f"为什么是现在：{opportunity_why_now}",
                "proof_line": f"价值支撑：{first_or_placeholder(opportunity_supporting_points, '价值支撑点')}",
                "accent_image": {"enabled": True, "left": 10.0, "top": 2.0, "width": 2.1, "height": 4.7},
            },
        ),
        make_slide(
            4,
            "客户现场卡片流程",
            "capability-selection",
            "capability-selection",
            [
                f"业务场景 / 输入感知：{join_cards(business_cards + input_cards, '业务场景卡与输入感知卡')}",
                f"理解分析：{join_cards(understanding_cards, '理解分析卡')}",
                f"生成交互 / 执行闭环：{join_cards(generation_cards + execution_cards, '生成交互卡与执行闭环卡')}",
            ],
            fields={
                "perception_line": f"业务场景 / 输入感知：{join_cards(business_cards + input_cards, '业务场景卡与输入感知卡')}",
                "analysis_line": f"理解分析：{join_cards(understanding_cards, '理解分析卡')}",
                "action_line": f"生成交互 / 执行闭环：{join_cards(generation_cards + execution_cards, '生成交互卡与执行闭环卡')}",
            },
        ),
        make_slide(
            5,
            "目标 AI Flow",
            "ai-flow-steps",
            "ai-flow-steps",
            [
                f"业务触发：{flow_trigger}",
                f"核心流程：{'；'.join(numbered_lines(flow_steps, 'AI Flow 步骤', limit=5))}",
                f"业务闭环：{flow_closure}",
            ],
            speaker_notes=[flow_narrative],
            fields={
                "trigger_line": f"业务触发：{flow_trigger}",
                "flow_lines": numbered_lines(flow_steps, "AI Flow 步骤", limit=5),
                "closure_line": f"业务闭环：{flow_closure}",
            },
        ),
        make_slide(
            6,
            "解决方案架构",
            "architecture-diagram",
            "architecture-diagram",
            [
                f"架构主线：{flow_narrative}",
                f"架构分层：{join_cards(mvp_spec['architecture_layers'], '架构分层')}",
                platform_line,
            ],
            fields={
                "architecture_title": scenario_name,
                "layer_lines": numbered_lines(mvp_spec["architecture_layers"], "架构分层", limit=4),
                "architecture_blocks": architecture_blocks,
                "support_lines": architecture_support_lines,
                "platform_chips": architecture_chips,
                "platform_line": platform_line,
                "closure_line": f"闭环目标：{flow_closure}",
            },
        ),
        make_slide(
            7,
            "能力映射与交付物",
            "product-mapping-table",
            "product-mapping-table",
            [
                f"能力映射：{'；'.join(mapping_lines[:2])}",
                platform_line,
                deliverable_line,
            ],
            fields={
                "mapping_lines": mapping_lines,
                "platform_line": platform_line,
                "deliverable_line": deliverable_line,
            },
        ),
        make_slide(
            8,
            "业务价值与验证假设",
            "business-value",
            "business-value",
            [
                f"预期价值：{join_cards(value_outcomes, '业务价值')}",
                f"关键指标：{join_cards(value_kpis, '量化指标')}",
                combine_scope_lines(poc_scope, poc_validation),
            ],
            fields={
                "value_lines": value_outcomes or ["待补充：业务价值"],
                "kpi_lines": value_kpis or ["待补充：量化指标"],
                "poc_lines": numbered_lines(poc_validation, "POC 验证点", limit=3),
            },
        ),
        make_slide(
            9,
            "原型与 MVP 设计",
            "prototype-concept",
            "prototype-concept",
            [
                f"原型名称：{prototype_name}",
                f"系统形态：{prototype_surface}；目标：{prototype_goal}",
                f"MVP 交付：{mvp_spec['prototype_mode']}；核心任务：{mvp_spec['core_task']}",
            ],
            fields={
                "top_labels": ["原型名称", "系统形态", "MVP 交付"],
                "prototype_name_line": f"原型名称：{prototype_name}；目标用户：{mvp_spec['primary_user']}",
                "prototype_surface_line": f"系统形态：{prototype_surface}；目标：{prototype_goal}",
                "prototype_value_line": f"MVP 交付：{mvp_spec['prototype_mode']}；核心任务：{mvp_spec['core_task']}；技术栈：{mvp_spec['tech_stack']}",
                "flow_title": "MVP 页面范围",
                "scope_title": "快速开发路径",
                "prototype_flow_lines": numbered_lines(dedupe_items(mvp_spec["screens"] + prototype_mock_scope + prototype_user_flow), "MVP 页面", limit=4),
                "prototype_scope_lines": numbered_lines(dedupe_items(mvp_spec["next_build_steps"] + [prototype_value_statement]), "快速开发路径", limit=4),
                "accent_image": {"enabled": True, "left": 9.8, "top": 2.0, "width": 2.3, "height": 4.7},
            },
        ),
        make_slide(
            10,
            "POC 与下一步",
            "poc-next-step",
            "poc-next-step",
            [
                f"试点范围：{poc_scope}",
                f"关键角色：{join_cards(poc_stakeholders, '关键角色')}",
                f"后续动作：{join_cards(poc_next_actions, '后续动作')}",
            ],
            fields={
                "scope_line": f"试点范围：{poc_scope}",
                "stakeholder_lines": poc_stakeholders or ["待补充：关键角色"],
                "next_action_lines": numbered_lines(poc_next_actions, "后续动作", limit=3),
                "accent_image": {"enabled": True, "left": 9.95, "top": 3.0, "width": 2.15, "height": 3.7},
            },
        ),
    ]

    return {
        "title": scenario_name,
        "subtitle": cover_subtitle,
        "aspect_ratio": aspect_ratio,
        "template": template,
        "theme": theme,
        "workflow_type": "ai-discovery-workshop",
        "source_type": payload.get("source_type", "normalized-workshop-scenario"),
        "selected_assets": selected_assets,
        "slides": slides,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a normalized workshop scenario JSON into a presentation plan")
    parser.add_argument("--input", required=True, help="Path to normalized workshop scenario JSON")
    parser.add_argument("--output", required=True, help="Path to output JSON plan")
    parser.add_argument("--template", default="enterprise-forum")
    parser.add_argument("--theme", default="eden-enterprise")
    parser.add_argument("--aspect-ratio", default="16:9")
    args = parser.parse_args()

    payload = load_json(args.input)
    plan = build_workshop_plan(payload, args.template, args.theme, args.aspect_ratio)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
