import csv
import difflib
import unicodedata
from copy import deepcopy
from functools import lru_cache
from pathlib import Path


ZONE_KEY_BY_LABEL = {
    "1业务场景区": "business_scenario",
    "2输入感知区": "input_perception",
    "3理解分析区": "understanding_analysis",
    "4生成交互区": "generation_interaction",
    "5执行闭环区": "execution_closure",
}


def ensure_text(value: object) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else ""


def ensure_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def ensure_dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def dedupe(items: list[str]) -> list[str]:
    result = []
    for item in items:
        if item and item not in result:
            result.append(item)
    return result


def normalize_text(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).strip().lower()
    return "".join(char for char in text if char.isalnum())


def normalize_zone_key(label: object) -> str:
    text = str(label or "").strip()
    for zone_label, zone_key in ZONE_KEY_BY_LABEL.items():
        if zone_label in text:
            return zone_key
    return ""


def parse_products(value: object) -> list[str]:
    text = ensure_text(value)
    if not text:
        return []
    normalized = text.replace("，", ",").replace("、", ",")
    return dedupe([item.strip() for item in normalized.split(",") if item.strip()])


def resolve_default_csv_path() -> Path:
    csv_name = "AI Discovery Card Workshop_卡牌数据.csv"
    candidates = [
        Path(__file__).resolve().parents[2] / csv_name,
        Path(__file__).resolve().parents[1] / csv_name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


@lru_cache(maxsize=4)
def load_card_catalog(csv_path: str | None = None) -> list[dict]:
    resolved = Path(csv_path) if csv_path else resolve_default_csv_path()
    cards = []
    with resolved.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=1):
            title = ensure_text(row.get("标题"))
            if not title:
                continue
            cards.append(
                {
                    "card_id": f"card-{index:03d}",
                    "title": title,
                    "category": ensure_text(row.get("分类")),
                    "zone_label": ensure_text(row.get("使用区")),
                    "zone_key": normalize_zone_key(row.get("使用区")),
                    "group": ensure_text(row.get("卡片分组")),
                    "description": ensure_text(row.get("描述")),
                    "details": ensure_text(row.get("详细说明")),
                    "products": parse_products(row.get("产品")),
                }
            )
    return cards


@lru_cache(maxsize=4)
def load_card_index(csv_path: str | None = None) -> dict[str, dict]:
    index = {}
    for card in load_card_catalog(csv_path):
        index[normalize_text(card["title"])] = card
    return index


def match_card(title: str, csv_path: str | None = None) -> dict | None:
    normalized = normalize_text(title)
    if not normalized:
        return None

    index = load_card_index(csv_path)
    if normalized in index:
        return index[normalized]

    candidates = []
    for card in load_card_catalog(csv_path):
        card_key = normalize_text(card["title"])
        if normalized in card_key or card_key in normalized:
            candidates.append(card)
    if candidates:
        return sorted(candidates, key=lambda item: len(item["title"]))[0]

    fuzzy_candidates = []
    for card in load_card_catalog(csv_path):
        ratio = difflib.SequenceMatcher(None, title, card["title"]).ratio()
        if ratio >= 0.8:
            fuzzy_candidates.append((ratio, card))
    if fuzzy_candidates:
        fuzzy_candidates.sort(key=lambda item: (-item[0], len(item[1]["title"])))
        return fuzzy_candidates[0][1]
    return None


def normalize_recognized_cards(source: dict) -> list[dict]:
    raw_cards = source.get("recognized_cards")
    if not isinstance(raw_cards, list):
        raw_cards = source.get("ocr_titles")

    normalized = []
    if not isinstance(raw_cards, list):
        return normalized

    for index, item in enumerate(raw_cards, start=1):
        if isinstance(item, str):
            title = ensure_text(item)
            if not title:
                continue
            normalized.append(
                {
                    "title": title,
                    "order_index": index,
                    "source": "manual-title-list",
                }
            )
            continue

        if isinstance(item, dict):
            title = ensure_text(item.get("title") or item.get("name") or item.get("value"))
            if not title:
                continue
            normalized.append(
                {
                    "title": title,
                    "order_index": item.get("order_index", index),
                    "source": ensure_text(item.get("source")) or "ocr",
                    "ocr_text": ensure_text(item.get("ocr_text")) or title,
                    "confidence": item.get("confidence"),
                    "position": item.get("position"),
                }
            )

    return sorted(normalized, key=lambda item: item.get("order_index", 0))


def build_mapping_rows(cards: list[dict]) -> list[dict]:
    rows = []
    seen = set()
    for card in cards:
        title = ensure_text(card.get("title"))
        if not title or title in seen:
            continue
        seen.add(title)
        rows.append(
            {
                "capability": title,
                "products": ensure_list(card.get("products")),
                "delivery": ensure_text(card.get("description")) or ensure_text(card.get("category")) or "卡牌能力说明",
            }
        )
    return rows


def build_process_from_cards(cards: list[dict]) -> list[str]:
    ordered_titles = [ensure_text(card.get("title")) for card in cards if ensure_text(card.get("title"))]
    return dedupe(ordered_titles)


def merge_product_mapping(existing_rows: object, card_rows: list[dict]) -> list[dict]:
    merged = []
    seen = set()

    if isinstance(existing_rows, list):
        for row in existing_rows:
            if not isinstance(row, dict):
                continue
            capability = ensure_text(row.get("capability") or row.get("card"))
            if not capability:
                continue
            normalized = {
                "capability": capability,
                "products": ensure_list(row.get("products")),
                "delivery": ensure_text(row.get("delivery") or row.get("deliverable")) or "交付形式",
            }
            merged.append(normalized)
            seen.add(capability)

    for row in card_rows:
        capability = ensure_text(row.get("capability"))
        if not capability or capability in seen:
            continue
        merged.append(row)
        seen.add(capability)

    return merged


def enrich_source_with_recognized_cards(source: dict, csv_path: str | None = None) -> dict:
    recognized = normalize_recognized_cards(source)
    if not recognized:
        return source

    enriched = deepcopy(source)
    matched_cards = []
    unmatched = []
    catalog_missing = False
    for card in recognized:
        try:
            matched = match_card(card.get("title", ""), csv_path)
        except FileNotFoundError:
            catalog_missing = True
            break
        if not matched:
            unmatched.append(card.get("title", ""))
            continue
        matched_cards.append(
            {
                **card,
                "card_id": matched["card_id"],
                "title": matched["title"],
                "category": matched["category"],
                "zone_key": matched["zone_key"],
                "zone_label": matched["zone_label"],
                "group": matched["group"],
                "description": matched["description"],
                "details": matched["details"],
                "products": matched["products"],
            }
        )

    if catalog_missing:
        if not ensure_list(enriched.get("current_process")):
            enriched["current_process"] = build_process_from_cards(recognized)
        return enriched

    enriched["recognized_cards"] = matched_cards
    if unmatched:
        enriched["unmatched_recognized_cards"] = unmatched

    detected = ensure_dict(enriched.get("detected_cards"))
    merged_detected = {
        "business_scenario": dedupe(ensure_list(detected.get("business_scenario"))),
        "input_perception": dedupe(ensure_list(detected.get("input_perception"))),
        "understanding_analysis": dedupe(ensure_list(detected.get("understanding_analysis"))),
        "generation_interaction": dedupe(ensure_list(detected.get("generation_interaction"))),
        "execution_closure": dedupe(ensure_list(detected.get("execution_closure"))),
    }

    for card in matched_cards:
        zone_key = ensure_text(card.get("zone_key"))
        title = ensure_text(card.get("title"))
        if zone_key and title and title not in merged_detected[zone_key]:
            merged_detected[zone_key].append(title)
    enriched["detected_cards"] = merged_detected

    if not ensure_list(enriched.get("current_process")) and matched_cards:
        enriched["current_process"] = build_process_from_cards(matched_cards)

    enriched["product_mapping"] = merge_product_mapping(enriched.get("product_mapping"), build_mapping_rows(matched_cards))

    event_input = ensure_dict(enriched.get("event_input"))
    if event_input and not ensure_text(event_input.get("scenario_summary")) and matched_cards:
        ordered_titles = [card["title"] for card in matched_cards[:4]]
        event_input["scenario_summary"] = f"围绕 {' -> '.join(ordered_titles)} 搭建 AI Flow"
        enriched["event_input"] = event_input

    return enriched
