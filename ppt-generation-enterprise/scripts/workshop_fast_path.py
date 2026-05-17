from card_catalog import enrich_source_with_recognized_cards


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


def derive_scenario_name(event_input: dict) -> str:
    prototype_name = ensure_text(event_input.get("prototype_preference"))
    if prototype_name:
        return prototype_name
    summary = ensure_text(event_input.get("scenario_summary"))
    if summary:
        return summary[:28]
    return "AI Discovery 场景"


def derive_ai_flow(current_process: list[str], scenario_summary: str) -> tuple[str, list[str], str]:
    if current_process:
        trigger = current_process[0]
        steps = current_process[1:] if len(current_process) > 1 else current_process
        closure = current_process[-1]
        return trigger, steps[:5], closure

    trigger = "业务进入重点波动或异常处理阶段"
    steps = [
        "汇总与场景相关的业务数据和上下文",
        "AI 识别关键风险、机会或异常",
        "生成建议、内容或下一步动作",
        "触发协同任务或人工确认",
        "结果回写工作台并沉淀复盘口径",
    ]
    closure = f"围绕“{scenario_summary or '业务场景'}”形成可演示的 AI 闭环"
    return trigger, steps, closure


def derive_mock_scope(mvp_spec: dict, scenario_name: str) -> list[str]:
    explicit = ensure_list(mvp_spec.get("screens"))
    if explicit:
        return explicit[:4]
    return [
        f"{scenario_name}总览",
        "分析详情页",
        "建议与动作页",
        "协同与复盘页",
    ]


def build_generic_mapping(prototype_name: str) -> list[dict]:
    return [
        {
            "capability": "业务数据汇聚",
            "products": ["Microsoft Fabric"],
            "delivery": "统一数据底座",
        },
        {
            "capability": "AI 分析与建议生成",
            "products": ["Azure AI Foundry", "Azure Machine Learning"],
            "delivery": f"围绕{prototype_name}的风险识别与建议生成",
        },
        {
            "capability": "工作台展示与协同闭环",
            "products": ["Power BI", "Power Automate"],
            "delivery": "看板展示、协同任务和复盘闭环",
        },
    ]


def normalize_fast_payload(source: dict) -> dict:
    source = enrich_source_with_recognized_cards(source)
    workshop = ensure_dict(source.get("workshop"))
    event_input = ensure_dict(source.get("event_input"))
    detected_cards = ensure_dict(source.get("detected_cards"))
    mvp_spec = ensure_dict(source.get("mvp_spec"))
    current_process = ensure_list(source.get("current_process"))
    existing_product_mapping = source.get("product_mapping") if isinstance(source.get("product_mapping"), list) else []

    customer = ensure_text(workshop.get("customer"), "待补充：客户名称")
    industry = ensure_text(workshop.get("industry"), ensure_text(event_input.get("customer_type"), "待补充：行业名称"))
    group_name = ensure_text(workshop.get("group_name"), "现场共创组")
    event_date = ensure_text(workshop.get("date"), "待补充：日期")

    scenario_summary = ensure_text(event_input.get("scenario_summary"), "待补充：业务场景")
    target_role = ensure_text(event_input.get("target_role"), "待补充：目标角色")
    pain_point = ensure_text(event_input.get("current_pain_point"), "待补充：当前痛点")
    expected_value = ensure_text(event_input.get("expected_value"), "待补充：目标价值")
    prototype_name = ensure_text(event_input.get("prototype_preference"), "待补充：原型形态")
    scenario_name = derive_scenario_name(event_input)

    trigger, ai_steps, closure = derive_ai_flow(current_process, scenario_summary)
    mock_scope = derive_mock_scope(mvp_spec, scenario_name)
    user_flow = ensure_list(mvp_spec.get("key_actions")) or [
        "查看核心业务风险或机会分布",
        "读取 AI 给出的判断与建议",
        "触发协同动作并回看处理结果",
    ]

    return {
        "workshop": {
            "title": ensure_text(workshop.get("title"), "AI Discovery Card Workshop"),
            "customer": customer,
            "industry": industry,
            "group_name": group_name,
            "date": event_date,
        },
        "scenario": {
            "name": scenario_name,
            "target_users": target_role,
            "business_problem": pain_point,
            "improvement_goal": expected_value,
        },
        "opportunity": {
            "statement": f"对{industry}客户来说，{prototype_name}是一个适合现场快速验证的 AI 切入点。",
            "why_now": f"当前最急的问题集中在“{pain_point}”，而客户更容易先接受以{prototype_name}为载体的可视化方案。",
            "supporting_points": dedupe([
                pain_point,
                expected_value,
                f"先完成{prototype_name}演示，再决定是否扩展到更完整的系统化建设",
            ]),
        },
        "current_process": current_process,
        "pain_points": dedupe([
            pain_point,
            f"围绕{prototype_name}缺少统一判断、建议和协同闭环",
            "当前决策与执行信息仍分散在多个环节",
        ]),
        "selected_cards": {
            "business_scenario": ensure_list(detected_cards.get("business_scenario")),
            "input_perception": ensure_list(detected_cards.get("input_perception")),
            "understanding_analysis": ensure_list(detected_cards.get("understanding_analysis")),
            "generation_interaction": ensure_list(detected_cards.get("generation_interaction")),
            "execution_closure": ensure_list(detected_cards.get("execution_closure")),
        },
        "ai_flow": {
            "trigger": trigger,
            "steps": ai_steps,
            "closure": closure,
            "narrative": f"该场景采用快速模式生成，重点是让现场在 5 分钟内拿到一版可讲解的 PPT、PRD 与方案设计文档。",
        },
        "prototype": {
            "name": prototype_name,
            "goal": expected_value,
            "surface": prototype_name,
            "user_flow": user_flow,
            "mock_scope": mock_scope,
            "value_statement": f"让{target_role}先在{prototype_name}里看到 AI 对问题识别、建议生成和协同闭环的价值。",
        },
        "product_mapping": existing_product_mapping or build_generic_mapping(prototype_name),
        "business_value": {
            "outcomes": dedupe([
                expected_value,
                "缩短人工整理、判断和协同的时间",
                "形成可用于继续推进 POC 的统一讲解口径",
            ]),
            "kpis": [
                "核心判断时间缩短 30%",
                "协同响应时间缩短 25%",
                "可通过静态样例完整演示主业务路径",
            ],
            "deliverables": [
                "方案 PPT",
                "需求PRD.md",
                "方案设计.md",
            ],
        },
        "poc": {
            "scope": f"围绕{prototype_name}优先验证识别、建议和协同三段闭环",
            "validation_points": [
                "AI 输出是否能帮助业务更快判断",
                "原型页面是否能完整讲清业务闭环",
                "现场方案是否适合作为后续 POC 基础",
            ],
            "stakeholders": [target_role, "业务负责人", "数字化团队"],
            "next_actions": [
                "确认试点范围和样例数据",
                "锁定第一版原型页面范围",
                "输出 POC 验证口径和里程碑",
            ],
        },
        "mvp_spec": mvp_spec,
        "source_type": "fast-workshop-scenario",
    }