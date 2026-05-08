import argparse
import json
from pathlib import Path


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_text(value: object, fallback: str = "") -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


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


def numbered_lines(items: list[str], fallback: str) -> list[str]:
    values = items or [fallback]
    return [f"{index}. {item}" for index, item in enumerate(values, start=1)]


def bullet_lines(items: list[str], fallback: str) -> list[str]:
    values = items or [fallback]
    return [f"- {item}" for item in values]


def make_section(title: str, lines: list[str]) -> str:
    body = "\n".join(lines).strip()
    return f"## {title}\n\n{body}\n"


def derive_screens(prototype_name: str, mock_scope: list[str], current_process: list[str]) -> list[str]:
    if mock_scope:
        return mock_scope[:4]
    if current_process:
        return [f"{step} 页面" for step in current_process[:4]]
    return [
        f"{prototype_name}首页",
        "洞察分析页",
        "生成结果页",
        "动作建议页",
    ]


def derive_modules(ai_flow_steps: list[str], pain_points: list[str], screens: list[str]) -> list[str]:
    modules = []
    for screen in screens[:4]:
        modules.append(f"{screen} 模块区")
    for step in ai_flow_steps[:3]:
        modules.append(step)
    for pain in pain_points[:2]:
        modules.append(f"围绕“{pain}”的展示与提示")
    return dedupe(modules)[:6]


def derive_sample_data(product_mapping: list[dict], current_process: list[str], customer_name: str) -> list[str]:
    samples = []
    for row in product_mapping[:3]:
        if isinstance(row, dict):
            capability = ensure_text(row.get("capability"), "能力项")
            delivery = ensure_text(row.get("delivery"), "交付结果")
            samples.append(f"{capability}：{delivery}")
    for step in current_process[:2]:
        samples.append(f"场景步骤样例：{step}")
    if not samples:
        samples.append(f"{customer_name} 的示例客户画像、活动结果和风险标签")
    return dedupe(samples)[:5]


def normalize_mvp_spec(payload: dict) -> dict:
    workshop = ensure_dict(payload.get("workshop"))
    scenario = ensure_dict(payload.get("scenario"))
    prototype = ensure_dict(payload.get("prototype"))
    ai_flow = ensure_dict(payload.get("ai_flow"))
    business_value = ensure_dict(payload.get("business_value"))
    poc = ensure_dict(payload.get("poc"))
    mvp_spec = ensure_dict(payload.get("mvp_spec"))

    customer_name = ensure_text(workshop.get("customer"), "待补充：客户名称")
    scenario_name = ensure_text(scenario.get("name"), "待补充：场景名称")
    primary_user = ensure_text(mvp_spec.get("primary_user"), ensure_text(scenario.get("target_users"), "待补充：主要使用角色"))
    core_task = ensure_text(mvp_spec.get("core_task"), ensure_text(scenario.get("improvement_goal"), "待补充：核心任务"))
    prototype_mode = ensure_text(mvp_spec.get("prototype_mode"), "前端壳子优先")
    tech_stack = ensure_text(mvp_spec.get("tech_stack_preference"), "Next.js + Tailwind CSS")

    current_process = ensure_list(payload.get("current_process"))
    pain_points = ensure_list(payload.get("pain_points"))
    ai_flow_steps = ensure_list(ai_flow.get("steps"))
    prototype_flow = ensure_list(prototype.get("user_flow"))
    mock_scope = ensure_list(mvp_spec.get("screens")) or ensure_list(prototype.get("mock_scope"))
    screens = derive_screens(ensure_text(prototype.get("name"), "原型"), mock_scope, current_process)
    modules = dedupe(ensure_list(mvp_spec.get("modules")) + derive_modules(ai_flow_steps, pain_points, screens))[:6]
    key_actions = dedupe(ensure_list(mvp_spec.get("key_actions")) + prototype_flow + ai_flow_steps[:2])[:6]
    style_keywords = dedupe(ensure_list(mvp_spec.get("style_keywords")) or ["企业级", "简洁", "卡片式布局"])
    sample_data = dedupe(ensure_list(mvp_spec.get("sample_data")) + derive_sample_data(ensure_list(payload.get("product_mapping")), current_process, customer_name))[:6]
    out_of_scope = dedupe(
        ensure_list(mvp_spec.get("out_of_scope"))
        or [
            "不接真实后端接口",
            "不实现真实业务流程提交",
            "不做权限体系和数据持久化",
            "不做生产级异常处理",
        ]
    )
    success_metrics = dedupe(
        ensure_list(mvp_spec.get("success_metrics"))
        + ensure_list(business_value.get("kpis"))[:2]
        + ["可以通过静态样例完整演示核心业务路径"]
    )[:5]
    delivery_items = dedupe(
        ensure_list(mvp_spec.get("delivery_items"))
        or [
            "可演示的前端壳子页面",
            "需求PRD.md",
            "方案设计.md",
        ]
    )
    solution_artifacts = dedupe(
        ensure_list(mvp_spec.get("solution_artifacts"))
        or [
            "方案设计：页面结构、模块布局、交互路径",
            "架构设计：展示层、组件层、样例数据层",
            "静态页面原型：可现场演示的前端壳子",
            "样例数据包：支撑页面演示的 mock 数据",
        ]
    )
    architecture_principles = dedupe(
        ensure_list(mvp_spec.get("architecture_principles"))
        or [
            "页面壳子优先，先保证关键业务路径可演示",
            "模块分层组织，页面、组件、样例数据分开维护",
            "Mock 数据驱动，先不接真实系统接口",
        ]
    )
    architecture_layers = dedupe(
        ensure_list(mvp_spec.get("architecture_layers"))
        or [
            "展示层：页面壳子、看板卡片、列表表格、详情抽屉",
            "交互层：筛选切换、建议查看、动作触发、结果回看",
            "数据层：样例数据、页面状态配置、Mock 接口返回",
        ]
    )
    next_build_steps = dedupe(
        ensure_list(mvp_spec.get("next_build_steps"))
        + ensure_list(poc.get("next_actions"))[:3]
        + ["基于方案设计文档快速搭建静态页面和样例数据"]
    )[:5]

    return {
        "customer_name": customer_name,
        "scenario_name": scenario_name,
        "business_problem": ensure_text(scenario.get("business_problem"), "待补充：业务问题"),
        "expected_value": ensure_text(scenario.get("improvement_goal"), "待补充：改善目标"),
        "primary_user": primary_user,
        "prototype_name": ensure_text(prototype.get("name"), "待补充：原型名称"),
        "prototype_surface": ensure_text(prototype.get("surface"), "待补充：原型形态"),
        "prototype_goal": ensure_text(prototype.get("goal"), "待补充：原型目标"),
        "prototype_value": ensure_text(prototype.get("value_statement"), "待补充：原型价值"),
        "prototype_mode": prototype_mode,
        "core_task": core_task,
        "screens": screens,
        "modules": modules,
        "key_actions": key_actions,
        "sample_data": sample_data,
        "style_keywords": style_keywords,
        "tech_stack": tech_stack,
        "out_of_scope": out_of_scope,
        "success_metrics": success_metrics,
        "delivery_items": delivery_items,
        "solution_artifacts": solution_artifacts,
        "architecture_principles": architecture_principles,
        "architecture_layers": architecture_layers,
        "next_build_steps": next_build_steps,
        "ai_flow_steps": ai_flow_steps,
        "pain_points": pain_points,
        "validation_points": ensure_list(poc.get("validation_points")),
    }


def render_prd(spec: dict) -> str:
    sections = [
        f"# 需求PRD\n\n本文档用于快速产出 {spec['customer_name']} 在“{spec['scenario_name']}”场景下的轻量原型。目标是先完成可演示的前端壳子，而不是功能完整的系统。\n",
        make_section(
            "项目概述",
            bullet_lines(
                [
                    f"客户：{spec['customer_name']}",
                    f"场景：{spec['scenario_name']}",
                    f"目标用户：{spec['primary_user']}",
                    f"原型名称：{spec['prototype_name']}",
                    f"原型模式：{spec['prototype_mode']}",
                ],
                "待补充：项目概述",
            ),
        ),
        make_section(
            "问题与目标",
            bullet_lines(
                [
                    f"当前问题：{spec['business_problem']}",
                    f"业务目标：{spec['expected_value']}",
                    f"原型目标：{spec['prototype_goal']}",
                    f"核心任务：{spec['core_task']}",
                ],
                "待补充：问题与目标",
            ),
        ),
        make_section("MVP 范围", numbered_lines(spec["screens"], "待补充：页面清单")),
        make_section("关键模块", numbered_lines(spec["modules"], "待补充：关键模块")),
        make_section("关键动作", numbered_lines(spec["key_actions"], "待补充：关键动作")),
        make_section("样例数据", numbered_lines(spec["sample_data"], "待补充：样例数据")),
        make_section(
            "交付清单",
            bullet_lines(spec["delivery_items"], "待补充：交付清单"),
        ),
        make_section(
            "非目标范围",
            bullet_lines(spec["out_of_scope"], "待补充：非目标范围"),
        ),
        make_section(
            "验收标准",
            bullet_lines(spec["success_metrics"], "待补充：验收标准"),
        ),
    ]
    return "\n".join(sections).strip() + "\n"


def render_solution_design(spec: dict) -> str:
    sections = [
        f"# 方案设计\n\n本文档面向快速 vibe coding。重点是明确页面结构、展示模块、交互路径和前端实现建议，帮助团队直接开始搭建 {spec['prototype_name']} 的原型壳子。\n",
        make_section(
            "设计原则",
            bullet_lines(
                [
                    "优先交付可演示页面，不依赖真实后端",
                    "页面信息结构清晰，适合客户现场讲解",
                    "尽量使用假数据和静态状态完成业务路径演示",
                    f"视觉风格建议：{' / '.join(spec['style_keywords'])}",
                ],
                "待补充：设计原则",
            ),
        ),
        make_section("页面结构", numbered_lines(spec["screens"], "待补充：页面结构")),
        make_section("模块布局", numbered_lines(spec["modules"], "待补充：模块布局")),
        make_section("交互路径", numbered_lines(spec["key_actions"], "待补充：交互路径")),
        make_section(
            "交付件",
            bullet_lines(spec["solution_artifacts"], "待补充：交付件"),
        ),
        make_section(
            "架构设计",
            bullet_lines(spec["architecture_layers"], "待补充：架构设计"),
        ),
        make_section(
            "演示状态说明",
            bullet_lines(
                [
                    "首页展示关键概览卡片和主操作入口",
                    "详情页展示 AI 洞察、生成结果和建议动作的静态样例",
                    "用切换状态、Tab、Drawer 或 Mock 数据模拟关键动作反馈",
                    "所有指标、列表和详情内容都可以先用假数据驱动",
                ],
                "待补充：演示状态说明",
            ),
        ),
        make_section(
            "推荐技术栈",
            bullet_lines(
                [
                    f"前端建议：{spec['tech_stack']}",
                    "样式建议：组件化卡片布局 + 简洁图表占位 + 演示态弹层",
                    "数据建议：本地 JSON / mock 数据文件驱动页面展示",
                ],
                "待补充：推荐技术栈",
            ),
        ),
        make_section(
            "建议目录结构",
            bullet_lines(
                [
                    "app/ 或 src/pages/：页面入口",
                    "components/：卡片、表格、Tab、Drawer、图表占位组件",
                    "data/：样例数据、页面假数据、切换状态配置",
                    "docs/：保留本 PRD 和方案设计文档",
                ],
                "待补充：建议目录结构",
            ),
        ),
        make_section(
            "快速开发建议",
            numbered_lines(spec["next_build_steps"], "待补充：快速开发建议"),
        ),
        make_section(
            "可直接复用的提示信息",
            bullet_lines(
                [
                    f"目标用户：{spec['primary_user']}",
                    f"核心任务：{spec['core_task']}",
                    f"原型形态：{spec['prototype_surface']}",
                    f"原型价值：{spec['prototype_value']}",
                ],
                "待补充：提示信息",
            ),
        ),
    ]
    return "\n".join(sections).strip() + "\n"


def generate_docs(payload: dict, output_dir: Path, prd_name: str, design_name: str) -> tuple[Path, Path]:
    spec = normalize_mvp_spec(payload)
    prd_path = output_dir / prd_name
    design_path = output_dir / design_name
    save_text(prd_path, render_prd(spec))
    save_text(design_path, render_solution_design(spec))
    return prd_path, design_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate lightweight MVP PRD and solution design documents from a workshop scenario")
    parser.add_argument("--input", required=True, help="Path to normalized workshop scenario JSON")
    parser.add_argument("--output-dir", required=True, help="Output directory for markdown documents")
    parser.add_argument("--prd-name", default="需求PRD.md", help="PRD file name")
    parser.add_argument("--design-name", default="方案设计.md", help="Solution design file name")
    args = parser.parse_args()

    payload = load_json(args.input)
    prd_path, design_path = generate_docs(payload, Path(args.output_dir), args.prd_name, args.design_name)
    print(str(prd_path))
    print(str(design_path))


if __name__ == "__main__":
    main()