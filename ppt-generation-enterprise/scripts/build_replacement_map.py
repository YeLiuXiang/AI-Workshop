import argparse
import json
from copy import deepcopy
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dig_value(source: object, path: str) -> object | None:
    current = source
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
            continue
        return None
    return current


def base_style(inventory: dict, inventory_slide: str, shape_key: str, shrink: float = 0) -> dict:
    shape = inventory[inventory_slide][shape_key]
    paragraphs = shape.get("paragraphs", [])
    style = {}
    if paragraphs:
        source = paragraphs[0]
        for key in [
            "alignment",
            "font_name",
            "font_size",
            "bold",
            "italic",
            "underline",
            "color",
            "theme_color",
            "line_spacing",
            "space_before",
            "space_after",
        ]:
            if key in source:
                style[key] = source[key]
    if "font_size" in style and shrink:
        style["font_size"] = max(8.0, float(style["font_size"]) - float(shrink))
    return style


def make_paragraph(inventory: dict, inventory_slide: str, shape_key: str, text: str, shrink: float = 0, **overrides) -> dict:
    paragraph = base_style(inventory, inventory_slide, shape_key, shrink=shrink)
    paragraph.update(overrides)
    paragraph["text"] = text
    return paragraph


def make_paragraphs(inventory: dict, inventory_slide: str, shape_key: str, texts: list[str], shrink: float = 0, **overrides) -> dict:
    return {
        "paragraphs": [
            make_paragraph(inventory, inventory_slide, shape_key, text, shrink=shrink, **overrides)
            for text in texts
            if text is not None and str(text).strip()
        ]
    }


def lookup_source_value(plan: dict, slide: dict, source_name: str, theme: dict) -> str | list[str]:
    if source_name == "title":
        return slide.get("title", "")
    if source_name == "subtitle":
        return slide.get("subtitle", "")
    if source_name == "title_lines":
        if slide.get("title_lines"):
            return slide["title_lines"]
        lines = [slide.get("title", "")]
        if slide.get("subtitle"):
            lines.append(slide["subtitle"])
        return lines
    if source_name == "summary_lines":
        if slide.get("summary_lines"):
            return slide["summary_lines"]
        return slide.get("key_points", [])[:2]
    if source_name == "footer":
        return slide.get("footer") or theme.get("footer", {}).get("brand_text", "")
    if source_name == "eyebrow":
        return slide.get("eyebrow") or plan.get("title", "PRESENTATION")
    if source_name.startswith("point_"):
        return slide.get("slots", {}).get(source_name, "")
    if source_name.startswith("slide."):
        value = dig_value(slide, source_name.removeprefix("slide."))
        return value if value is not None else ""
    if source_name.startswith("plan."):
        value = dig_value(plan, source_name.removeprefix("plan."))
        return value if value is not None else ""
    if source_name.startswith("theme."):
        value = dig_value(theme, source_name.removeprefix("theme."))
        return value if value is not None else ""

    nested_slide_value = dig_value(slide, source_name)
    if nested_slide_value is not None:
        return nested_slide_value

    nested_plan_value = dig_value(plan, source_name)
    if nested_plan_value is not None:
        return nested_plan_value

    return slide.get(source_name, "")


def resolve_layout_name(slide: dict, layout_map: dict) -> str:
    if slide.get("layout_key") and slide["layout_key"] in layout_map["layouts"]:
        return slide["layout_key"]
    defaults = layout_map.get("slide_defaults", {})
    return defaults.get(slide.get("slide_type", "scenario"), "bullets-3")


def build_replacement_map(plan: dict, inventory: dict, layout_map: dict, theme: dict) -> dict:
    replacement_map = {}

    for zero_index, slide in enumerate(plan.get("slides", [])):
        slide_key = f"slide-{zero_index}"
        layout_name = resolve_layout_name(slide, layout_map)
        layout_spec = layout_map["layouts"][layout_name]
        inventory_slide = layout_spec["inventory_slide"]
        replacement_map[slide_key] = {}

        for slot_name, slot_spec in layout_spec["slots"].items():
            shape_key = slot_spec["shape"]
            source_name = slot_spec.get("source", slot_name)
            shrink = slot_spec.get("shrink", 0)
            mode = slot_spec.get("mode", "single")
            overrides = deepcopy(slot_spec.get("overrides", {}))
            value = lookup_source_value(plan, slide, source_name, theme)

            if isinstance(value, list) or mode == "paragraphs":
                texts = value if isinstance(value, list) else [value]
                replacement_map[slide_key][shape_key] = make_paragraphs(
                    inventory,
                    inventory_slide,
                    shape_key,
                    texts,
                    shrink=shrink,
                    **overrides,
                )
            else:
                replacement_map[slide_key][shape_key] = {
                    "paragraphs": [
                        make_paragraph(
                            inventory,
                            inventory_slide,
                            shape_key,
                            str(value),
                            shrink=shrink,
                            **overrides,
                        )
                    ]
                }

    return replacement_map


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a template replacement map from a presentation plan")
    parser.add_argument("--plan", required=True, help="Path to presentation-plan.json")
    parser.add_argument("--inventory", required=True, help="Path to template inventory JSON")
    parser.add_argument("--layout-map", required=True, help="Path to layout map JSON")
    parser.add_argument("--theme-file", help="Optional theme JSON file")
    parser.add_argument("--output", required=True, help="Path to replacement-map.json")
    args = parser.parse_args()

    plan = load_json(args.plan)
    inventory = load_json(args.inventory)
    layout_map = load_json(args.layout_map)
    theme = load_json(args.theme_file) if args.theme_file else {}

    replacement_map = build_replacement_map(plan, inventory, layout_map, theme)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(replacement_map, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
