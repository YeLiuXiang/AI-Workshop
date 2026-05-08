import argparse
import json
from pathlib import Path

from build_replacement_map import build_replacement_map
from compose_workshop_assets import compose_payload
from plan_to_pptx import write_pptx
from workshop_fast_path import normalize_fast_payload
from workshop_to_mvp_docs import generate_docs
from workshop_to_plan import build_workshop_plan


INVALID_WINDOWS_CHARS = '<>:"/\\|?*'


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def sanitize_name(value: object, fallback: str, max_length: int = 48) -> str:
    text = str(value).strip() if value is not None else ""
    if not text:
        text = fallback

    normalized = []
    for char in text:
        if char in INVALID_WINDOWS_CHARS:
            normalized.append("-")
        elif char in {"\r", "\n", "\t"}:
            normalized.append(" ")
        else:
            normalized.append(char)

    cleaned = " ".join("".join(normalized).split())
    cleaned = cleaned.strip(" .")
    if not cleaned:
        cleaned = fallback
    return cleaned[:max_length].rstrip(" .")


def is_sparse_workshop_input(payload: dict) -> bool:
    return isinstance(payload.get("event_input"), dict) and not isinstance(payload.get("scenario"), dict)


def derive_customer_name(payload: dict) -> str:
    workshop = payload.get("workshop", {}) if isinstance(payload.get("workshop"), dict) else {}
    return sanitize_name(workshop.get("customer"), "未命名客户")


def derive_scenario_name(payload: dict) -> str:
    scenario = payload.get("scenario", {}) if isinstance(payload.get("scenario"), dict) else {}
    if isinstance(scenario, dict) and scenario.get("name"):
        return sanitize_name(scenario.get("name"), "未命名场景")

    live_input = payload.get("event_input", {}) if isinstance(payload.get("event_input"), dict) else {}
    return sanitize_name(live_input.get("scenario_summary"), "未命名场景")


def build_case_directory_name(customer_name: str, scenario_name: str) -> str:
    return sanitize_name(f"{customer_name}-{scenario_name}", "未命名客户-未命名场景", max_length=72)


def resolve_theme_file(args) -> Path:
    return Path(args.theme_file or f"themes/{args.theme}/theme.json")


def resolve_inventory_file(args) -> Path:
    return Path(args.inventory or f"templates/{args.template}/inventory.example.json")


def resolve_layout_map_file(args) -> Path:
    return Path(args.layout_map or f"templates/{args.template}/layout-map.example.json")


def generate_package(args) -> Path:
    source = load_json(args.input)
    workspace_root = Path(args.workspace_root)

    if is_sparse_workshop_input(source):
        if args.fast:
            scenario_payload = normalize_fast_payload(source)
        else:
            scenario_payload = compose_payload(source, Path(args.assets_dir))
        input_file_name = "原始输入.json"
        normalized_file_name = "组合场景.json"
    else:
        scenario_payload = source
        input_file_name = "场景输入.json"
        normalized_file_name = None

    customer_name = derive_customer_name(scenario_payload)
    scenario_name = derive_scenario_name(scenario_payload)
    case_dir = workspace_root / build_case_directory_name(customer_name, scenario_name)
    case_dir.mkdir(parents=True, exist_ok=True)

    save_json(case_dir / input_file_name, source)
    if normalized_file_name:
        save_json(case_dir / normalized_file_name, scenario_payload)

    plan = build_workshop_plan(scenario_payload, args.template, args.theme, args.aspect_ratio)
    plan_path = case_dir / "演示文稿方案.json"
    save_json(plan_path, plan)

    theme = load_json(str(resolve_theme_file(args)))

    if not args.skip_replacement_map and not args.fast:
        inventory_path = resolve_inventory_file(args)
        layout_map_path = resolve_layout_map_file(args)
        if inventory_path.exists() and layout_map_path.exists():
            inventory = load_json(str(inventory_path))
            layout_map = load_json(str(layout_map_path))
            replacement_map = build_replacement_map(plan, inventory, layout_map, theme)
            save_json(case_dir / "替换映射.json", replacement_map)

    ppt_file_name = sanitize_name(f"{customer_name}-{scenario_name}方案", "客户方案", max_length=80) + ".pptx"
    ppt_path = case_dir / ppt_file_name
    write_pptx(plan, theme, str(ppt_path))

    generate_docs(scenario_payload, case_dir, "需求PRD.md", "方案设计.md")
    return case_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a workshop PPT package into Workspace/<客户名-场景名>/ with Chinese artifact names"
    )
    parser.add_argument("--input", required=True, help="Path to sparse live input JSON or normalized scenario JSON")
    parser.add_argument("--workspace-root", default="Workspace", help="Root directory for all generated customer cases")
    parser.add_argument("--assets-dir", default="content-packs", help="Path to content packs directory for sparse input")
    parser.add_argument("--template", default="enterprise-forum", help="Template key for plan generation")
    parser.add_argument("--theme", default="eden-enterprise", help="Theme key for plan generation")
    parser.add_argument("--theme-file", help="Optional explicit theme JSON file path")
    parser.add_argument("--aspect-ratio", default="16:9", help="Presentation aspect ratio")
    parser.add_argument("--inventory", help="Optional template inventory JSON path")
    parser.add_argument("--layout-map", help="Optional layout map JSON path")
    parser.add_argument("--skip-replacement-map", action="store_true", help="Skip replacement map generation")
    parser.add_argument("--fast", action="store_true", help="Use the 5-minute workshop path: deterministic sparse-input normalization and skip replacement map generation")
    args = parser.parse_args()

    case_dir = generate_package(args)
    print(case_dir)


if __name__ == "__main__":
    main()