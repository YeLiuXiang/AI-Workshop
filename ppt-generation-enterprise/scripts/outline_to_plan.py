import argparse
import json
import re
from pathlib import Path


PAGE_PATTERN = re.compile(r"^###\s*Page\s+(\d+)(?:\s*[·\-]\s*(.+))?$", re.MULTILINE)
FIELD_PATTERN = re.compile(r"^\*\*(.+?)\*\*：\s*(.+)$")


def infer_slide_type(title: str, page_label: str, key_points: list[str]) -> str:
    header_joined = " ".join([title, page_label]).strip()
    joined = " ".join([header_joined, *key_points])
    if any(token in header_joined for token in ["封面", "标题页"]):
        return "cover"
    if any(token in joined for token in ["公司简介", "公司介绍"]):
        return "company-intro"
    if any(token in joined for token in ["服务能力", "能力矩阵"]):
        return "capability-grid"
    if any(token in joined for token in ["为什么", "大量办公时间", "痛点"]):
        return "problem-statement"
    if any(token in joined for token in ["从问答助手到数字同事", "对比", "差异"]):
        return "comparison"
    if any(token in joined for token in ["工作原理", "核心构件", "四种能力"]):
        return "principles"
    if any(token in joined for token in ["Step 1", "Step 2", "Step 3", "浏览器自动化", "流程"]):
        return "step-flow"
    if any(token in joined for token in ["场景", "知识管理", "信息处理", "会议纪要"]):
        return "scenario"
    if any(token in joined for token in ["部署", "选型", "矩阵", "适合谁"]):
        return "table"
    if any(token in joined for token in ["攻击面", "风险"]):
        return "risk"
    if any(token in joined for token in ["防线", "治理", "守住"]):
        return "control"
    if any(token in joined for token in ["结论", "落地", "先跑通", "扩展"]):
        return "conclusion"
    return "scenario"


def default_layout_key(slide_type: str) -> str:
    mapping = {
        "cover": "cover-basic",
        "conclusion": "bullets-3",
        "scenario": "bullets-3",
        "comparison": "bullets-3",
        "problem-statement": "bullets-3",
        "company-intro": "bullets-3",
        "capability-grid": "bullets-3",
        "principles": "bullets-3",
        "step-flow": "bullets-3",
        "table": "bullets-3",
        "risk": "bullets-3",
        "control": "bullets-3",
    }
    return mapping.get(slide_type, "bullets-3")


def extract_section_block(text: str, start: int, end: int) -> str:
    return text[start:end].strip()


def parse_field_value(line: str) -> tuple[str, str] | None:
    match = FIELD_PATTERN.match(line.strip())
    if not match:
        return None
    return match.group(1).strip(), match.group(2).strip()


def parse_page_block(page_number: int, page_label: str, block: str) -> dict:
    title = page_label.strip() if page_label else f"Page {page_number}"
    subtitle = ""
    key_points = []
    notes = []
    metadata = {}
    current_section = None

    for raw_line in block.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        field = parse_field_value(stripped)
        if field:
            field_name, field_value = field
            if field_name == "页标题":
                title = field_value
            else:
                metadata[field_name] = field_value
            continue

        if stripped == "**页面内容**":
            current_section = "content"
            continue
        if stripped in {"**备注**", "**批注**", "### Notes:"}:
            current_section = "notes"
            continue

        if stripped.startswith("-"):
            value = stripped[1:].strip()
            if current_section == "notes":
                notes.append(value)
            else:
                key_points.append(value)
                if value.startswith("副标题：") and not subtitle:
                    subtitle = value.split("：", 1)[1].strip()
            continue

        if current_section == "notes":
            notes.append(stripped)
        elif current_section == "content":
            key_points.append(stripped)
            if stripped.startswith("副标题：") and not subtitle:
                subtitle = stripped.split("：", 1)[1].strip()

    slide_type = infer_slide_type(title, page_label or "", key_points)
    layout_key = default_layout_key(slide_type)

    slide = {
        "slide_number": page_number,
        "title": title,
        "subtitle": subtitle,
        "slide_type": slide_type,
        "layout_key": layout_key,
        "key_points": key_points,
        "speaker_notes": notes,
        "summary_lines": key_points[:2],
        "slots": {
            "point_1": key_points[0] if len(key_points) > 0 else "",
            "point_2": key_points[1] if len(key_points) > 1 else "",
            "point_3": key_points[2] if len(key_points) > 2 else "",
        },
    }

    if slide_type == "cover":
        slide["eyebrow"] = metadata.get("主题", "ENTERPRISE AI PRESENTATION")
        slide["title_lines"] = [title] + ([subtitle] if subtitle else [])
        slide["footer"] = metadata.get("品牌信息", "EDEN INFORMATION SERVICE LIMITED")

    return slide


def parse_outline(markdown_text: str, template: str, theme: str, aspect_ratio: str) -> dict:
    title = "Presentation"
    subtitle = ""

    for raw_line in markdown_text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            break

    for raw_line in markdown_text.splitlines():
        field = parse_field_value(raw_line.strip())
        if not field:
            continue
        name, value = field
        if name == "主题":
            title = value.strip("《》")
        elif name == "副标题":
            subtitle = value

    matches = list(PAGE_PATTERN.finditer(markdown_text))
    slides = []
    for index, match in enumerate(matches):
        page_number = int(match.group(1))
        page_label = (match.group(2) or "").strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown_text)
        block = extract_section_block(markdown_text, start, end)
        slides.append(parse_page_block(page_number, page_label, block))

    return {
        "title": title,
        "subtitle": subtitle,
        "aspect_ratio": aspect_ratio,
        "template": template,
        "theme": theme,
        "slides": slides,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a Markdown outline into a presentation plan JSON file")
    parser.add_argument("--input", required=True, help="Path to Markdown outline")
    parser.add_argument("--output", required=True, help="Path to output JSON plan")
    parser.add_argument("--template", default="enterprise-forum")
    parser.add_argument("--theme", default="eden-enterprise")
    parser.add_argument("--aspect-ratio", default="16:9")
    args = parser.parse_args()

    markdown_text = Path(args.input).read_text(encoding="utf-8")
    plan = parse_outline(markdown_text, args.template, args.theme, args.aspect_ratio)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
