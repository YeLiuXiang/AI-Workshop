import argparse
import json
from pathlib import Path

from card_catalog import enrich_source_with_recognized_cards


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str, payload: dict) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_text(value: object) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else ""


def ensure_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def keyword_hits(corpus: str, keywords: list[str]) -> int:
    lowered = corpus.lower()
    return sum(1 for keyword in keywords if keyword and keyword.lower() in lowered)


def choose_scenario_name(live_summary: str, asset_name: str) -> str:
    summary = ensure_text(live_summary)
    if not summary:
        return asset_name
    if len(summary) <= 24 and not summary.startswith("希望"):
        return summary
    return asset_name or summary


def merge_unique(primary: list[str], secondary: list[str]) -> list[str]:
    merged = []
    for item in [*primary, *secondary]:
        if item and item not in merged:
            merged.append(item)
    return merged


def detect_lane(live_input: dict) -> str:
    corpus = " ".join(
        [
            ensure_text(live_input.get("customer_type")),
            ensure_text(live_input.get("scenario_summary")),
            ensure_text(live_input.get("target_role")),
            ensure_text(live_input.get("current_pain_point")),
            ensure_text(live_input.get("expected_value")),
            ensure_text(live_input.get("prototype_preference")),
        ]
    )

    consumer_iot_keywords = [
        "消费电子",
        "iot",
        "设备",
        "终端",
        "售后",
        "工单",
        "质检",
        "安装",
        "联网",
        "遥测",
        "故障",
        "维保",
        "维修",
        "硬件",
        "家电",
        "智能家居",
        "固件",
        "巡检",
    ]
    ecommerce_keywords = [
        "电商",
        "跨境",
        "跨界",
        "营销",
        "客群",
        "流失",
        "内容",
        "增长",
        "履约",
        "库存",
        "订单",
        "退货",
        "复购",
        "会员",
        "商品",
        "仓配",
        "渠道",
    ]

    if keyword_hits(corpus, ecommerce_keywords) > keyword_hits(corpus, consumer_iot_keywords):
        return "cross-border-ecommerce"
    return "consumer-electronics-iot"


def score_case(case_payload: dict, live_input: dict, detected_cards: dict) -> int:
    score = 0
    corpus = " ".join(
        [
            ensure_text(live_input.get("customer_type")),
            ensure_text(live_input.get("scenario_summary")),
            ensure_text(live_input.get("target_role")),
            ensure_text(live_input.get("current_pain_point")),
            ensure_text(live_input.get("expected_value")),
            ensure_text(live_input.get("prototype_preference")),
        ]
    )
    all_cards = []
    for value in detected_cards.values():
        all_cards.extend(ensure_list(value))

    lowered = corpus.lower()
    for keyword in case_payload.get("keywords", []):
        if keyword and keyword.lower() in lowered:
            score += 3
    for keyword in case_payload.get("keywords", []):
        if keyword in all_cards:
            score += 1
    return score


def load_best_reference_case(base_dir: Path, lane: str, live_input: dict, detected_cards: dict) -> tuple[str, dict]:
    case_dir = base_dir / "reference-cases" / lane
    best_id = ""
    best_score = -1
    best_payload = {}
    for file_path in sorted(case_dir.glob("*.json")):
        payload = load_json(str(file_path))
        score = score_case(payload, live_input, detected_cards)
        if score > best_score:
            best_score = score
            best_payload = payload
            best_id = payload.get("id", file_path.stem)
    if not best_payload:
        raise FileNotFoundError(f"No reference case found for lane: {lane}")
    return best_id, best_payload


def merge_cards(live_cards: dict, recommended_cards: dict) -> dict:
    result = {}
    keys = set(live_cards.keys()) | set(recommended_cards.keys())
    for key in keys:
        result[key] = merge_unique(ensure_list(live_cards.get(key)), ensure_list(recommended_cards.get(key)))
    return result


def compose_payload(source: dict, base_dir: Path) -> dict:
    source = enrich_source_with_recognized_cards(source)
    workshop = source.get("workshop", {}) if isinstance(source.get("workshop"), dict) else {}
    live_input = source.get("event_input", {}) if isinstance(source.get("event_input"), dict) else {}
    detected_cards = source.get("detected_cards", {}) if isinstance(source.get("detected_cards"), dict) else {}
    mvp_spec = source.get("mvp_spec", {}) if isinstance(source.get("mvp_spec"), dict) else {}

    lane = detect_lane(live_input)
    outline_pack = load_json(str(base_dir / "outlines" / "opportunity-prototype-deck.json"))
    snippets = load_json(str(base_dir / "snippets" / "industry-defaults.json"))
    snippet_pack = snippets.get(lane, {})
    case_id, reference_case = load_best_reference_case(base_dir, lane, live_input, detected_cards)

    live_problem = ensure_text(live_input.get("current_pain_point"))
    live_value = ensure_text(live_input.get("expected_value"))
    scenario_summary = ensure_text(live_input.get("scenario_summary"))
    target_role = ensure_text(live_input.get("target_role"))
    prototype_preference = ensure_text(live_input.get("prototype_preference"))

    scenario_asset = reference_case.get("scenario", {})
    opportunity_asset = reference_case.get("opportunity", {})
    prototype_asset = reference_case.get("prototype", {})
    business_value_asset = reference_case.get("business_value", {})
    poc_asset = reference_case.get("poc", {})

    composed = {
        "workshop": {
            "title": ensure_text(workshop.get("title")) or "AI Discovery Card Workshop",
            "customer": ensure_text(workshop.get("customer")) or "待补充：客户名称",
            "industry": ensure_text(workshop.get("industry")) or ensure_text(live_input.get("customer_type")) or lane,
            "group_name": ensure_text(workshop.get("group_name")) or "待补充：小组名称",
            "date": ensure_text(workshop.get("date")) or "待补充：活动日期"
        },
        "scenario": {
            "name": choose_scenario_name(scenario_summary, scenario_asset.get("name", "待补充：业务场景")),
            "target_users": target_role or scenario_asset.get("target_users", "待补充：目标角色"),
            "business_problem": live_problem or scenario_asset.get("business_problem", "待补充：业务问题"),
            "improvement_goal": live_value or scenario_asset.get("improvement_goal", "待补充：改善目标")
        },
        "opportunity": {
            "statement": opportunity_asset.get("statement", ""),
            "why_now": opportunity_asset.get("why_now", "") or snippet_pack.get("opportunity_frame", ""),
            "supporting_points": merge_unique(
                ensure_list(opportunity_asset.get("supporting_points")),
                [live_value] if live_value else []
            )
        },
        "current_process": ensure_list(source.get("current_process")) or ensure_list(reference_case.get("current_process")),
        "pain_points": merge_unique([live_problem] if live_problem else [], ensure_list(reference_case.get("pain_points"))),
        "selected_cards": merge_cards(detected_cards, reference_case.get("recommended_cards", {})),
        "ai_flow": reference_case.get("ai_flow", {}),
        "prototype": {
            "name": prototype_preference or prototype_asset.get("name", "待补充：原型名称"),
            "goal": prototype_asset.get("goal", ""),
            "surface": prototype_preference or prototype_asset.get("surface", ""),
            "user_flow": ensure_list(prototype_asset.get("user_flow")),
            "mock_scope": ensure_list(prototype_asset.get("mock_scope")),
            "value_statement": prototype_asset.get("value_statement", "") or snippet_pack.get("prototype_prompt", "")
        },
        "product_mapping": reference_case.get("product_mapping", []),
        "business_value": {
            "outcomes": merge_unique([live_value] if live_value else [], ensure_list(business_value_asset.get("outcomes"))),
            "kpis": ensure_list(business_value_asset.get("kpis")),
            "deliverables": ensure_list(business_value_asset.get("deliverables"))
        },
        "poc": {
            "scope": poc_asset.get("scope", ""),
            "validation_points": ensure_list(poc_asset.get("validation_points")),
            "stakeholders": ensure_list(poc_asset.get("stakeholders")),
            "next_actions": merge_unique(
                ensure_list(poc_asset.get("next_actions")),
                ensure_list(snippet_pack.get("fallback_next_actions"))
            )
        },
        "mvp_spec": mvp_spec,
        "selected_assets": {
            "industry_lane": lane,
            "outline_pack": outline_pack.get("id", "opportunity-prototype-deck"),
            "reference_case": case_id,
            "snippet_pack": f"industry-defaults:{lane}",
            "card_photo_paths": ensure_list(source.get("card_photo_paths"))
        },
        "source_type": "asset-composed-workshop"
    }

    return composed


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose workshop content from sparse live input and reusable content packs")
    parser.add_argument("--input", required=True, help="Path to sparse live workshop input JSON")
    parser.add_argument("--assets-dir", default="content-packs", help="Path to content packs directory")
    parser.add_argument("--output", required=True, help="Path to composed scenario JSON")
    args = parser.parse_args()

    source = load_json(args.input)
    assets_dir = Path(args.assets_dir)
    composed = compose_payload(source, assets_dir)
    save_json(args.output, composed)
    print(args.output)


if __name__ == "__main__":
    main()