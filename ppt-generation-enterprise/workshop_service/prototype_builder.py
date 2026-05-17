from __future__ import annotations

import json
import re
from pathlib import Path


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


def shorten_text(value: str, limit: int = 64) -> str:
    text = ensure_text(value)
    if len(text) <= limit:
        return text
    return f"{text[: limit - 1].rstrip()}…"


def extract_metric_value(metric: str, fallback: str) -> tuple[str, str]:
    text = ensure_text(metric)
    if not text:
        return fallback, "待确认业务指标"

    match = re.search(r"(\d+\s*[%xX倍]|T\+\d+|\d+\s*(周|天|小时|分钟|人|项|次))", text)
    if match:
        value = match.group(1).replace(" ", "")
        label = text.replace(match.group(1), "").strip(" ：:，,。")
        return value, label or text
    return fallback, text


def infer_variant(payload: dict) -> str:
    workshop = ensure_dict(payload.get("workshop"))
    scenario = ensure_dict(payload.get("scenario"))
    prototype = ensure_dict(payload.get("prototype"))
    source = " ".join(
        [
            ensure_text(workshop.get("industry")),
            ensure_text(scenario.get("name")),
            ensure_text(scenario.get("business_problem")),
            ensure_text(prototype.get("name")),
            ensure_text(prototype.get("goal")),
        ]
    )

    growth_keywords = ("会员", "营销", "增长", "流失", "客群", "复购", "电商")
    service_keywords = ("售后", "报修", "工单", "客服", "维修", "派工", "服务")
    knowledge_keywords = ("知识", "问答", "培训", "学习", "文档", "助手")

    if any(keyword in source for keyword in growth_keywords):
        return "growth"
    if any(keyword in source for keyword in service_keywords):
        return "service"
    if any(keyword in source for keyword in knowledge_keywords):
        return "knowledge"
    return "ops"


VARIANT_CONFIG = {
    "growth": {
        "hero_label": "GROWTH AND RETENTION OPS ROOM",
        "nav_label": "场景原型包",
        "sidebar_title": "客群与运营样例",
        "sidebar_badge": "3 组样例",
        "queue_label": "重点经营对象",
        "workspace_kicker": "统一增长工作台",
        "status_label": "保留风险",
        "run_button": "模拟一次 AI 生成",
        "cycle_button": "切换下一组样例",
        "tab_titles": ["客户洞察", "方案编排", "内容生成", "闭环动作"],
        "action_buttons": ["触发专属优惠", "生成活动落地页", "创建 CRM 跟进任务"],
        "metric_defaults": ["38%", "2.4x", "T+1天", "82%"],
        "tag_defaults": ["会员运营", "内容生成", "复盘分析", "流失预警"],
        "theme": "growth",
    },
    "service": {
        "hero_label": "AI AFTER-SALES SERVICE LOOP",
        "nav_label": "场景原型包",
        "sidebar_title": "报修与服务样例",
        "sidebar_badge": "3 条工单",
        "queue_label": "待处理工单",
        "workspace_kicker": "统一服务工作台",
        "status_label": "当前优先级",
        "run_button": "模拟一次 AI 诊断",
        "cycle_button": "切换下一条工单",
        "tab_titles": ["服务上下文", "问题诊断", "回复与动作", "闭环沉淀"],
        "action_buttons": ["发送回复建议", "升级二线专家", "创建上门排障任务"],
        "metric_defaults": ["12分钟", "65%", "T+4小时", "91%"],
        "tag_defaults": ["工单诊断", "知识召回", "派工联动", "闭环回写"],
        "theme": "service",
    },
    "knowledge": {
        "hero_label": "KNOWLEDGE AND ENABLEMENT WORKBENCH",
        "nav_label": "场景原型包",
        "sidebar_title": "问题与知识样例",
        "sidebar_badge": "3 组样例",
        "queue_label": "待响应问题",
        "workspace_kicker": "统一知识工作台",
        "status_label": "响应优先级",
        "run_button": "模拟一次 Copilot 生成",
        "cycle_button": "切换下一组问题",
        "tab_titles": ["问题理解", "知识编排", "答案生成", "运营沉淀"],
        "action_buttons": ["生成标准答案", "创建培训任务", "回写知识库"],
        "metric_defaults": ["76%", "3.1x", "T+1小时", "88%"],
        "tag_defaults": ["知识问答", "内容整理", "培训支持", "回写闭环"],
        "theme": "knowledge",
    },
    "ops": {
        "hero_label": "COPILOT WORKSHOP OPERATIONS ROOM",
        "nav_label": "场景原型包",
        "sidebar_title": "业务样例",
        "sidebar_badge": "3 组任务",
        "queue_label": "重点任务",
        "workspace_kicker": "统一业务工作台",
        "status_label": "当前状态",
        "run_button": "模拟一次 Copilot 编排",
        "cycle_button": "切换下一组任务",
        "tab_titles": ["场景概览", "方案编排", "内容生成", "闭环动作"],
        "action_buttons": ["生成方案建议", "创建协同任务", "回写结果记录"],
        "metric_defaults": ["45%", "2.0x", "T+2天", "80%"],
        "tag_defaults": ["场景理解", "方案生成", "原型演示", "闭环验证"],
        "theme": "ops",
    },
}


def build_growth_items(payload: dict) -> list[dict]:
    scenario = ensure_dict(payload.get("scenario"))
    business_value = ensure_dict(payload.get("business_value"))
    pain_points = ensure_list(payload.get("pain_points"))
    outcomes = ensure_list(business_value.get("outcomes"))
    steps = ensure_list(ensure_dict(payload.get("ai_flow")).get("steps"))

    titles = ["高价值会员客群", "沉默复购会员", "高流失风险会员"]
    tones = ["增长机会高", "复购潜力待激活", "需要即时保留动作"]
    statuses = ["机会窗口", "重点跟进", "高风险"]

    items = []
    for index, title in enumerate(titles):
        items.append(
            {
                "name": title,
                "badge": statuses[index],
                "owner": "会员运营负责人",
                "headline": outcomes[index % max(len(outcomes), 1)] if outcomes else "验证增长与保留动作联动价值",
                "summary": pain_points[index % max(len(pain_points), 1)] if pain_points else scenario.get("business_problem", "待补充"),
                "focus": tones[index],
                "signals": [
                    steps[index % max(len(steps), 1)] if steps else "系统汇总会员画像与活动结果",
                    outcomes[(index + 1) % max(len(outcomes), 1)] if outcomes else "形成可执行的经营建议",
                    pain_points[(index + 1) % max(len(pain_points), 1)] if pain_points else "识别主要业务摩擦点",
                ],
                "journey": [
                    "查看客群洞察与生命周期信号",
                    "生成营销内容与活动页面草稿",
                    "查看结果并触发下一轮干预动作",
                ],
                "recommendations": [
                    "优先生成一版活动主题与文案草稿",
                    "联动高流失会员清单生成专属动作",
                    "把复盘结果回流到下一轮客群策略",
                ],
                "generated_asset": {
                    "title": f"{title} 经营动作草案",
                    "body": outcomes[index % max(len(outcomes), 1)] if outcomes else "生成客群经营建议与演示页面。",
                },
            }
        )
    return items


def build_service_items(payload: dict) -> list[dict]:
    scenario = ensure_dict(payload.get("scenario"))
    pain_points = ensure_list(payload.get("pain_points"))
    steps = ensure_list(ensure_dict(payload.get("ai_flow")).get("steps"))

    titles = ["新报修待诊断", "重复报修高风险", "专家升级工单"]
    badges = ["待处理", "需加急", "升级中"]

    items = []
    for index, title in enumerate(titles):
        items.append(
            {
                "name": title,
                "badge": badges[index],
                "owner": "售后服务主管",
                "headline": shorten_text(scenario.get("improvement_goal", "提升诊断效率与服务闭环速度"), 38),
                "summary": pain_points[index % max(len(pain_points), 1)] if pain_points else scenario.get("business_problem", "待补充"),
                "focus": "优先压缩诊断与派工耗时",
                "signals": [
                    steps[index % max(len(steps), 1)] if steps else "系统读取工单、设备状态与知识记录",
                    "召回历史处理经验与 FAQ",
                    "给出客服回复与下一步动作建议",
                ],
                "journey": [
                    "查看设备状态与客户上下文",
                    "完成 AI 诊断与知识召回",
                    "发送回复并升级复杂工单",
                ],
                "recommendations": [
                    "优先给一线客服返回可解释诊断依据",
                    "把疑难问题自动转给专家队列",
                    "同步沉淀新知识回写规则",
                ],
                "generated_asset": {
                    "title": f"{title} 服务动作建议",
                    "body": "生成面向客服的一键回复、升级动作和知识回写建议。",
                },
            }
        )
    return items


def build_knowledge_items(payload: dict) -> list[dict]:
    scenario = ensure_dict(payload.get("scenario"))
    pain_points = ensure_list(payload.get("pain_points"))

    titles = ["高频问答整理", "新员工培训支持", "跨部门知识协同"]
    badges = ["高频", "新需求", "协同中"]
    items = []
    for index, title in enumerate(titles):
        items.append(
            {
                "name": title,
                "badge": badges[index],
                "owner": "知识运营负责人",
                "headline": shorten_text(scenario.get("improvement_goal", "把知识理解、答案生成和回写沉淀拉到一个工作台中"), 38),
                "summary": pain_points[index % max(len(pain_points), 1)] if pain_points else scenario.get("business_problem", "待补充"),
                "focus": "统一答案口径与知识沉淀",
                "signals": [
                    "读取历史知识、文档片段与常见问题",
                    "生成带依据的答案与训练材料",
                    "把反馈结果回写到知识库",
                ],
                "journey": [
                    "定位问题与目标角色",
                    "召回资料并编排答案结构",
                    "输出答案、培训材料和回写建议",
                ],
                "recommendations": [
                    "优先整理高频问题的标准答案",
                    "把培训提纲和演示案例同步生成",
                    "记录被采纳答案用于后续优化",
                ],
                "generated_asset": {
                    "title": f"{title} Copilot 草案",
                    "body": "生成标准答案、培训提纲与后续知识运营动作建议。",
                },
            }
        )
    return items


def build_ops_items(payload: dict) -> list[dict]:
    scenario = ensure_dict(payload.get("scenario"))
    steps = ensure_list(ensure_dict(payload.get("ai_flow")).get("steps"))
    pain_points = ensure_list(payload.get("pain_points"))
    titles = ["机会整理", "方案编排", "验证闭环"]
    badges = ["待整理", "编排中", "待验证"]
    items = []
    for index, title in enumerate(titles):
        items.append(
            {
                "name": title,
                "badge": badges[index],
                "owner": ensure_text(scenario.get("target_users"), "业务负责人"),
                "headline": shorten_text(scenario.get("improvement_goal", "验证当前业务场景的可落地方案"), 38),
                "summary": pain_points[index % max(len(pain_points), 1)] if pain_points else scenario.get("business_problem", "待补充"),
                "focus": "先对齐场景、流程和验证口径",
                "signals": [
                    steps[index % max(len(steps), 1)] if steps else "整理当前业务输入",
                    "形成更清晰的方案结构与验证范围",
                    "输出工作台原型和后续动作建议",
                ],
                "journey": [
                    "梳理业务输入",
                    "组织方案与关键模块",
                    "生成可演示产物并校验",
                ],
                "recommendations": [
                    "先聚焦一条最有价值的业务闭环",
                    "定义 POC 验证点与样例数据",
                    "输出 PPT 和可访问原型进行现场演示",
                ],
                "generated_asset": {
                    "title": f"{title} 输出建议",
                    "body": "生成与当前场景绑定的方案大纲、原型结构和验证动作。",
                },
            }
        )
    return items


def build_work_items(payload: dict, variant: str) -> list[dict]:
    if variant == "growth":
        return build_growth_items(payload)
    if variant == "service":
        return build_service_items(payload)
    if variant == "knowledge":
        return build_knowledge_items(payload)
    return build_ops_items(payload)


def build_kpis(payload: dict, config: dict) -> list[dict]:
    kpis = ensure_list(ensure_dict(payload.get("business_value")).get("kpis"))
    defaults = config["metric_defaults"]
    cards = []
    for index in range(4):
        metric = kpis[index] if index < len(kpis) else ""
        value, label = extract_metric_value(metric, defaults[index])
        cards.append(
            {
                "value": value,
                "label": label,
                "detail": "演示态业务指标",
            }
        )
    return cards


def build_tags(payload: dict, config: dict) -> list[str]:
    mvp_spec = ensure_dict(payload.get("mvp_spec"))
    tags = ensure_list(mvp_spec.get("style_keywords")) + ensure_list(ensure_dict(payload.get("prototype")).get("mock_scope"))
    if not tags:
        tags = config["tag_defaults"]
    return tags[:6]


def build_capability_cards(payload: dict) -> list[dict]:
    mapping = payload.get("product_mapping")
    if isinstance(mapping, list) and mapping:
        cards = []
        for item in mapping[:4]:
            item_dict = ensure_dict(item)
            cards.append(
                {
                    "title": ensure_text(item_dict.get("capability"), "能力模块"),
                    "body": ensure_text(item_dict.get("delivery"), "待补充交付内容"),
                    "products": ensure_list(item_dict.get("products"))[:3],
                }
            )
        return cards

    modules = ensure_list(ensure_dict(payload.get("mvp_spec")).get("modules"))
    return [
        {
            "title": module,
            "body": "用于承接当前场景的关键业务动作与展示内容。",
            "products": [],
        }
        for module in modules[:4]
    ]


def build_screen_cards(payload: dict) -> list[dict]:
    screens = ensure_list(ensure_dict(payload.get("mvp_spec")).get("screens"))
    key_actions = ensure_list(ensure_dict(payload.get("mvp_spec")).get("key_actions"))
    cards = []
    for index, screen in enumerate(screens[:4]):
        cards.append(
            {
                "title": screen,
                "body": key_actions[index % max(len(key_actions), 1)] if key_actions else "用于演示当前业务页面结构与关键交互。",
            }
        )
    return cards


def build_prototype_data(payload: dict) -> dict:
    workshop = ensure_dict(payload.get("workshop"))
    scenario = ensure_dict(payload.get("scenario"))
    opportunity = ensure_dict(payload.get("opportunity"))
    prototype = ensure_dict(payload.get("prototype"))
    business_value = ensure_dict(payload.get("business_value"))
    poc = ensure_dict(payload.get("poc"))
    mvp_spec = ensure_dict(payload.get("mvp_spec"))
    ai_flow = ensure_dict(payload.get("ai_flow"))

    variant = infer_variant(payload)
    config = VARIANT_CONFIG[variant]
    work_items = build_work_items(payload, variant)
    primary_item = work_items[0]

    flow_steps = ensure_list(ai_flow.get("steps"))
    selected_cards = ensure_dict(payload.get("selected_cards"))
    card_tags = (
        ensure_list(selected_cards.get("business_scenario"))
        + ensure_list(selected_cards.get("understanding_analysis"))
        + ensure_list(selected_cards.get("generation_interaction"))
    )

    return {
        "variant": variant,
        "theme": config["theme"],
        "context": {
            "customer": ensure_text(workshop.get("customer"), "现场客户"),
            "industry": ensure_text(workshop.get("industry"), "业务场景"),
            "group_name": ensure_text(workshop.get("group_name"), "第 1 组"),
            "scenario_name": ensure_text(scenario.get("name"), "业务场景"),
            "target_user": ensure_text(scenario.get("target_users"), ensure_text(mvp_spec.get("primary_user"), "业务负责人")),
            "prototype_name": ensure_text(prototype.get("name"), ensure_text(scenario.get("name"), "业务工作台")),
            "hero_label": config["hero_label"],
            "nav_label": config["nav_label"],
            "workspace_kicker": config["workspace_kicker"],
            "queue_label": config["queue_label"],
            "status_label": config["status_label"],
            "sidebar_title": config["sidebar_title"],
            "sidebar_badge": config["sidebar_badge"],
            "run_button": config["run_button"],
            "cycle_button": config["cycle_button"],
        },
        "hero": {
            "goal": ensure_text(prototype.get("goal"), ensure_text(scenario.get("improvement_goal"), "待补充")),
            "brief": ensure_text(prototype.get("value_statement"), ensure_text(opportunity.get("statement"), "待补充")),
            "problem": ensure_text(scenario.get("business_problem"), "待补充"),
            "flow": " -> ".join(flow_steps[:4]) if flow_steps else "等待整理业务流程输入",
            "tags": build_tags(payload, config),
        },
        "tabs": config["tab_titles"],
        "kpis": build_kpis(payload, config),
        "work_items": work_items,
        "active_item_name": primary_item["name"],
        "capability_cards": build_capability_cards(payload),
        "screen_cards": build_screen_cards(payload),
        "overview": {
            "signals": flow_steps[:5] or ["等待补充业务流程"],
            "pain_points": ensure_list(payload.get("pain_points"))[:4],
            "outcomes": ensure_list(business_value.get("outcomes"))[:4],
            "validation_points": ensure_list(poc.get("validation_points"))[:4],
            "next_actions": ensure_list(poc.get("next_actions"))[:4],
            "stakeholders": ensure_list(poc.get("stakeholders"))[:4],
            "selected_cards": card_tags[:8],
            "modules": ensure_list(mvp_spec.get("modules"))[:6],
            "actions": ensure_list(mvp_spec.get("key_actions"))[:6],
            "sample_data": ensure_list(mvp_spec.get("sample_data"))[:6],
            "scope": ensure_text(poc.get("scope"), "待补充"),
            "why_now": ensure_text(opportunity.get("why_now"), ""),
            "deliverables": ensure_list(business_value.get("deliverables"))[:3],
        },
        "actions": config["action_buttons"],
    }


def render_index_html(data: dict) -> str:
    payload_json = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    theme = data.get("theme", "ops")
    context = data["context"]
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{context["prototype_name"]}</title>
    <link rel="stylesheet" href="./styles.css" />
    <script id="prototype-data" type="application/json">{payload_json}</script>
    <script defer src="./script.js"></script>
  </head>
  <body data-theme="{theme}">
    <div class="page-shell">
      <nav class="page-nav">
        <div class="nav-context">
          <span class="nav-label">{context["nav_label"]}</span>
          <strong>{context["customer"]} / {context["scenario_name"]}</strong>
        </div>
        <div class="nav-badges">
          <span>{context["industry"]}</span>
          <span>{context["group_name"]}</span>
        </div>
      </nav>

      <header class="hero-panel">
        <div class="hero-copy-block">
          <p class="eyebrow">{data["context"]["hero_label"]}</p>
          <h1 id="hero-title"></h1>
          <p class="hero-copy" id="hero-brief"></p>
          <div class="hero-tags" id="hero-tags"></div>
        </div>

        <div class="hero-signal-panel">
          <p class="eyebrow">当前演示链路</p>
          <strong id="hero-flow"></strong>
          <p class="hero-brief" id="hero-problem"></p>
          <div class="hero-actions">
            <button id="cycle-item-button" class="primary-button" type="button">{context["cycle_button"]}</button>
            <button id="simulate-run-button" class="secondary-button" type="button">{context["run_button"]}</button>
          </div>
        </div>
      </header>

      <section class="kpi-strip" id="kpi-strip"></section>

      <main class="dashboard-layout">
        <aside class="panel sidebar-panel">
          <div class="panel-heading">
            <div>
              <p class="panel-kicker">{context["queue_label"]}</p>
              <h2>{context["sidebar_title"]}</h2>
            </div>
            <span class="badge">{context["sidebar_badge"]}</span>
          </div>

          <div class="chip-row" id="card-chip-row"></div>
          <div class="work-item-list" id="work-item-list"></div>

          <section class="sidebar-block">
            <div class="subheading-row">
              <h3>Copilot 推荐动作</h3>
              <span class="badge badge-soft">演示态</span>
            </div>
            <ul class="bullet-list" id="recommended-actions"></ul>
          </section>

          <section class="sidebar-block accent-block">
            <p class="mini-label">POC 验证范围</p>
            <strong id="poc-focus"></strong>
            <p id="poc-note"></p>
          </section>
        </aside>

        <section class="panel workspace-panel">
          <div class="workspace-header">
            <div>
              <p class="panel-kicker">{context["workspace_kicker"]}</p>
              <h2 id="workspace-title"></h2>
              <p class="workspace-subtitle" id="workspace-subtitle"></p>
            </div>
            <div class="headline-card">
              <p class="mini-label">{context["status_label"]}</p>
              <strong id="status-title"></strong>
              <span id="status-note"></span>
            </div>
          </div>

          <nav class="screen-nav" id="screen-nav">
            <button class="screen-button is-active" data-screen="overview" type="button">{data["tabs"][0]}</button>
            <button class="screen-button" data-screen="design" type="button">{data["tabs"][1]}</button>
            <button class="screen-button" data-screen="generate" type="button">{data["tabs"][2]}</button>
            <button class="screen-button" data-screen="closure" type="button">{data["tabs"][3]}</button>
          </nav>

          <section class="screen-stage">
            <article class="screen-panel is-active" data-screen-panel="overview">
              <div class="screen-grid two-up-grid">
                <section class="subpanel">
                  <div class="subheading-row">
                    <h3>业务信号概览</h3>
                    <span class="badge" id="active-owner"></span>
                  </div>
                  <div class="stat-grid" id="overview-stats"></div>
                  <div class="timeline-card">
                    <div class="subheading-row">
                      <h4>当前关键流程</h4>
                      <span id="signal-count"></span>
                    </div>
                    <ul class="timeline-list" id="signal-list"></ul>
                  </div>
                </section>

                <section class="subpanel">
                  <div class="subheading-row">
                    <h3>当前重点问题</h3>
                    <span class="badge badge-warm" id="focus-badge"></span>
                  </div>
                  <div class="highlight-block">
                    <div>
                      <p class="mini-label">本轮目标</p>
                      <strong id="goal-title"></strong>
                    </div>
                    <div>
                      <p class="mini-label">关键角色</p>
                      <strong id="target-user"></strong>
                    </div>
                  </div>
                  <p class="summary-text" id="problem-summary"></p>
                  <div class="tag-cloud" id="stakeholder-tags"></div>
                </section>
              </div>
            </article>

            <article class="screen-panel" data-screen-panel="design">
              <div class="screen-grid two-up-grid">
                <section class="subpanel">
                  <div class="subheading-row">
                    <h3>方案路径与业务编排</h3>
                    <span class="badge">方案结构</span>
                  </div>
                  <div class="journey-stack" id="journey-stack"></div>
                </section>

                <section class="subpanel">
                  <div class="subheading-row">
                    <h3>能力与产品承接</h3>
                    <span class="badge badge-soft">MVP 范围</span>
                  </div>
                  <div class="capability-grid" id="capability-grid"></div>
                </section>
              </div>
            </article>

            <article class="screen-panel" data-screen-panel="generate">
              <div class="screen-grid two-up-grid">
                <section class="subpanel">
                  <div class="subheading-row">
                    <h3>当前生成结果</h3>
                    <span class="badge">工作台输出</span>
                  </div>
                  <div class="content-card">
                    <p class="mini-label">主输出</p>
                    <strong id="generated-title"></strong>
                    <p id="generated-body"></p>
                  </div>
                  <div class="action-stack" id="action-stack"></div>
                </section>

                <section class="subpanel">
                  <div class="subheading-row">
                    <h3>原型页面结构</h3>
                    <span class="badge badge-soft">可演示</span>
                  </div>
                  <div class="preview-grid" id="screen-card-grid"></div>
                  <div class="mock-data-card">
                    <p class="mini-label">样例数据</p>
                    <div class="chip-row" id="sample-data-row"></div>
                  </div>
                </section>
              </div>
            </article>

            <article class="screen-panel" data-screen-panel="closure">
              <div class="screen-grid two-up-grid">
                <section class="subpanel">
                  <div class="subheading-row">
                    <h3>验证点与业务结果</h3>
                    <span class="badge badge-warm">POC</span>
                  </div>
                  <div class="closure-columns">
                    <div>
                      <p class="mini-label">预期结果</p>
                      <ul class="bullet-list" id="outcome-list"></ul>
                    </div>
                    <div>
                      <p class="mini-label">验证重点</p>
                      <ul class="bullet-list" id="validation-list"></ul>
                    </div>
                  </div>
                </section>

                <section class="subpanel">
                  <div class="subheading-row">
                    <h3>下一步动作与运行日志</h3>
                    <span class="badge">实时 mock</span>
                  </div>
                  <ul class="bullet-list" id="next-action-list"></ul>
                  <div class="execution-card">
                    <p class="mini-label">运行日志</p>
                    <strong id="execution-status"></strong>
                    <ul class="execution-list" id="execution-list"></ul>
                  </div>
                </section>
              </div>
            </article>
          </section>
        </section>
      </main>
    </div>
  </body>
</html>
"""


def render_styles_css() -> str:
    return """:root {
  --bg: #f3eee8;
  --surface: rgba(255, 250, 246, 0.9);
  --surface-strong: #fffaf4;
  --text: #2f2722;
  --muted: #786a61;
  --line: rgba(89, 68, 52, 0.12);
  --line-strong: rgba(89, 68, 52, 0.18);
  --shadow: 0 22px 60px rgba(86, 58, 39, 0.12);
  --radius-xl: 32px;
  --radius-lg: 24px;
  --radius-md: 18px;
  --radius-sm: 12px;
  --brand: #915132;
  --brand-2: #d37d45;
  --brand-soft: rgba(211, 125, 69, 0.14);
  --brand-strong: rgba(145, 81, 50, 0.16);
  --brand-active-border: #c79d82;
  --badge-warm-bg: #f2ddd0;
  --badge-warm-text: #7a4524;
}

body[data-theme="growth"] {
  --brand: #8e5134;
  --brand-2: #cf7a43;
  --brand-soft: rgba(207, 122, 67, 0.16);
  --brand-strong: rgba(142, 81, 52, 0.14);
  --brand-active-border: #c9a087;
  --badge-warm-bg: #f3dfd2;
  --badge-warm-text: #7f4626;
}

body[data-theme="service"] {
  --brand: #365a72;
  --brand-2: #5f9ecb;
  --brand-soft: rgba(95, 158, 203, 0.18);
  --brand-strong: rgba(54, 90, 114, 0.15);
  --brand-active-border: #89aac0;
  --badge-warm-bg: #dbe9f2;
  --badge-warm-text: #35576d;
}

body[data-theme="knowledge"] {
  --brand: #4e4f8f;
  --brand-2: #7d7cf3;
  --brand-soft: rgba(125, 124, 243, 0.18);
  --brand-strong: rgba(78, 79, 143, 0.15);
  --brand-active-border: #a7a7db;
  --badge-warm-bg: #e4e3fb;
  --badge-warm-text: #4f4e8d;
}

body[data-theme="ops"] {
  --brand: #48515f;
  --brand-2: #8090aa;
  --brand-soft: rgba(128, 144, 170, 0.18);
  --brand-strong: rgba(72, 81, 95, 0.14);
  --brand-active-border: #aab3c0;
  --badge-warm-bg: #e3e7ed;
  --badge-warm-text: #4b5563;
}

* { box-sizing: border-box; }
html, body { margin: 0; min-height: 100%; }

body {
  font-family: "Segoe UI Variable", "Aptos", "Microsoft YaHei UI", sans-serif;
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(255,255,255,0.95), rgba(255,255,255,0) 36%),
    radial-gradient(circle at 100% 0%, var(--brand-soft), transparent 30%),
    linear-gradient(180deg, var(--bg) 0%, #efe7df 100%);
}

.page-shell {
  max-width: 1440px;
  margin: 0 auto;
  padding: 24px;
}

.page-nav,
.hero-panel,
.panel,
.subpanel,
.headline-card,
.execution-card,
.content-card,
.mock-data-card,
.accent-block {
  background: var(--surface);
  border: 1px solid rgba(255, 255, 255, 0.72);
  box-shadow: var(--shadow);
  backdrop-filter: blur(12px);
}

.page-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 18px;
  border-radius: 22px;
  margin-bottom: 18px;
}

.nav-context,
.nav-badges,
.hero-tags,
.chip-row,
.tag-cloud,
.action-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.nav-label,
.eyebrow,
.panel-kicker,
.mini-label {
  margin: 0;
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--muted);
}

.nav-context strong,
h1,
h2,
h3,
h4,
.badge,
.work-item-card strong,
.content-card strong {
  font-family: "Bahnschrift", "Aptos Display", "Microsoft YaHei UI", sans-serif;
}

.nav-context strong {
  display: block;
  margin-top: 4px;
  font-size: 16px;
}

.nav-badges span,
.hero-tags span,
.badge,
.chip-row span,
.tag-cloud span {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(30, 29, 27, 0.05);
  color: var(--muted);
  font-size: 12px;
}

.hero-panel {
  display: grid;
  grid-template-columns: 1.2fr 0.9fr;
  gap: 18px;
  padding: 30px;
  border-radius: var(--radius-xl);
  margin-bottom: 18px;
}

.hero-copy-block,
.hero-signal-panel {
  min-height: 248px;
  border-radius: 28px;
}

.hero-copy-block {
  padding: 6px 6px 6px 0;
}

.hero-signal-panel {
  display: grid;
  gap: 14px;
  align-content: start;
  padding: 24px;
  background:
    radial-gradient(circle at top right, rgba(255,255,255,0.36), transparent 22%),
    linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fff8f2;
}

h1 {
  margin: 10px 0 0;
  font-size: clamp(34px, 4.8vw, 58px);
  line-height: 1.04;
  max-width: 10ch;
}

h2 {
  margin: 4px 0 0;
  font-size: 28px;
}

h3 {
  margin: 0;
  font-size: 18px;
}

h4 {
  margin: 0;
  font-size: 15px;
}

.hero-copy,
.hero-brief,
.workspace-subtitle,
.summary-text,
.content-card p,
.accent-block p,
.execution-card li,
.timeline-list li,
.bullet-list li {
  color: var(--muted);
  line-height: 1.7;
}

.hero-copy {
  margin: 18px 0 20px;
  max-width: 64ch;
}

.hero-signal-panel .eyebrow,
.hero-signal-panel .hero-brief,
.hero-signal-panel .mini-label {
  color: rgba(255, 248, 242, 0.78);
}

.hero-signal-panel strong {
  font-size: 28px;
  line-height: 1.4;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.primary-button,
.secondary-button,
.screen-button,
.action-button,
.work-item-card {
  font: inherit;
}

.primary-button,
.secondary-button,
.action-button {
  min-height: 46px;
  border-radius: 999px;
  padding: 0 18px;
  border: 0;
  cursor: pointer;
}

.primary-button {
  background: rgba(255, 255, 255, 0.14);
  color: #fff8f2;
}

.secondary-button {
  background: rgba(255, 255, 255, 0.92);
  color: var(--brand);
}

.kpi-strip {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.kpi-card {
  padding: 18px 20px;
  border-radius: 22px;
  background: var(--surface);
  border: 1px solid rgba(255, 255, 255, 0.74);
  box-shadow: var(--shadow);
}

.kpi-card strong {
  display: block;
  margin-top: 8px;
  font-size: 28px;
  color: var(--brand);
}

.kpi-card p {
  margin: 8px 0 0;
  color: var(--muted);
}

.dashboard-layout {
  display: grid;
  grid-template-columns: 360px minmax(0, 1fr);
  gap: 18px;
}

.panel,
.subpanel,
.headline-card,
.execution-card,
.content-card,
.mock-data-card,
.accent-block {
  border-radius: var(--radius-lg);
}

.panel {
  padding: 22px;
}

.sidebar-panel {
  display: grid;
  gap: 16px;
  align-content: start;
}

.panel-heading,
.workspace-header,
.subheading-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.work-item-list {
  display: grid;
  gap: 12px;
}

.work-item-card {
  width: 100%;
  text-align: left;
  padding: 16px;
  border-radius: 20px;
  border: 1px solid var(--line);
  background: var(--surface-strong);
  cursor: pointer;
}

.work-item-card.is-active {
  border-color: var(--brand-active-border);
  box-shadow: inset 0 0 0 1px var(--brand-strong);
  background: linear-gradient(180deg, #fffaf5 0%, var(--brand-soft) 100%);
}

.work-item-card strong {
  display: block;
  margin: 8px 0 6px;
  font-size: 18px;
}

.work-item-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.55;
}

.status-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.status-pill,
.badge,
.badge-soft,
.badge-warm {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 32px;
  padding: 0 12px;
  border-radius: 999px;
  font-size: 12px;
}

.badge {
  background: rgba(30, 29, 27, 0.06);
  color: var(--muted);
}

.badge-soft {
  background: var(--brand-soft);
  color: var(--brand);
}

.badge-warm {
  background: var(--badge-warm-bg);
  color: var(--badge-warm-text);
}

.sidebar-block,
.subpanel,
.headline-card,
.content-card,
.mock-data-card,
.execution-card {
  padding: 18px;
}

.accent-block {
  padding: 20px;
  background:
    radial-gradient(circle at top right, rgba(255,255,255,0.26), transparent 26%),
    linear-gradient(145deg, var(--brand), var(--brand-2));
}

.accent-block strong,
.accent-block p,
.accent-block .mini-label {
  color: #fff8f2;
}

.workspace-panel {
  min-width: 0;
}

.headline-card {
  min-width: 220px;
  background: linear-gradient(180deg, #fffaf6 0%, var(--brand-soft) 100%);
}

.headline-card strong {
  display: block;
  margin-top: 8px;
  font-size: 26px;
  color: var(--brand);
}

.screen-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 18px 0 14px;
}

.screen-button {
  min-height: 40px;
  padding: 0 16px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.6);
  color: var(--muted);
  cursor: pointer;
}

.screen-button.is-active {
  color: #fffaf6;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  border-color: transparent;
}

.screen-panel { display: none; }
.screen-panel.is-active { display: block; }

.screen-grid {
  display: grid;
  gap: 16px;
}

.two-up-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.stat-grid,
.preview-grid,
.capability-grid,
.closure-columns {
  display: grid;
  gap: 12px;
}

.stat-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-bottom: 14px;
}

.preview-grid,
.capability-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.closure-columns {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  margin-top: 8px;
}

.stat-card,
.preview-card,
.capability-card,
.journey-step {
  padding: 16px;
  border-radius: 18px;
  background: var(--surface-strong);
  border: 1px solid var(--line);
}

.stat-card strong,
.preview-card strong,
.capability-card strong {
  display: block;
  margin-top: 8px;
  font-size: 20px;
}

.journey-stack {
  display: grid;
  gap: 12px;
}

.journey-step {
  position: relative;
  padding-left: 54px;
}

.journey-step::before {
  content: attr(data-step);
  position: absolute;
  left: 16px;
  top: 16px;
  width: 26px;
  height: 26px;
  border-radius: 999px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fffaf6;
  font-size: 12px;
  font-weight: 700;
}

.timeline-card,
.highlight-block,
.content-card,
.mock-data-card,
.execution-card {
  margin-top: 12px;
}

.timeline-list,
.bullet-list,
.execution-list {
  margin: 12px 0 0;
  padding-left: 18px;
}

.highlight-block {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  padding: 14px;
  border-radius: 20px;
  background: linear-gradient(180deg, #fffaf6 0%, var(--brand-soft) 100%);
  border: 1px solid var(--line);
}

.content-card strong {
  font-size: 24px;
  color: var(--text);
}

.content-card p {
  margin: 10px 0 0;
}

.action-stack {
  margin-top: 14px;
}

.action-button {
  border: 1px solid var(--line-strong);
  background: rgba(255, 255, 255, 0.68);
  color: var(--text);
}

.action-button.primary-action {
  background: linear-gradient(135deg, var(--brand), var(--brand-2));
  color: #fffaf6;
  border-color: transparent;
}

.execution-card strong {
  display: block;
  margin-top: 8px;
  font-size: 20px;
}

.products-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.products-row span {
  padding: 6px 10px;
  border-radius: 999px;
  background: var(--brand-soft);
  color: var(--brand);
  font-size: 12px;
}

@media (max-width: 1180px) {
  .dashboard-layout,
  .hero-panel,
  .two-up-grid,
  .closure-columns {
    grid-template-columns: 1fr;
  }

  .kpi-strip {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .page-shell { padding: 14px; }
  .page-nav,
  .hero-panel,
  .panel { padding: 16px; }
  .page-nav,
  .panel-heading,
  .workspace-header,
  .subheading-row,
  .hero-actions { flex-direction: column; }
  .kpi-strip,
  .stat-grid,
  .preview-grid,
  .capability-grid { grid-template-columns: 1fr; }
  .headline-card { min-width: 0; width: 100%; }
  h1 { font-size: 38px; max-width: none; }
}
"""


def render_script_js() -> str:
    return """const prototypeData = JSON.parse(document.getElementById("prototype-data").textContent);

const state = {
  activeItemIndex: Math.max(
    prototypeData.work_items.findIndex((item) => item.name === prototypeData.active_item_name),
    0
  ),
  activeScreen: "overview",
  runCount: 0,
  logs: ["原型已加载，等待演示动作。"],
};

const elementMap = {
  heroTitle: document.getElementById("hero-title"),
  heroBrief: document.getElementById("hero-brief"),
  heroFlow: document.getElementById("hero-flow"),
  heroProblem: document.getElementById("hero-problem"),
  heroTags: document.getElementById("hero-tags"),
  kpiStrip: document.getElementById("kpi-strip"),
  cardChipRow: document.getElementById("card-chip-row"),
  workItemList: document.getElementById("work-item-list"),
  recommendedActions: document.getElementById("recommended-actions"),
  pocFocus: document.getElementById("poc-focus"),
  pocNote: document.getElementById("poc-note"),
  workspaceTitle: document.getElementById("workspace-title"),
  workspaceSubtitle: document.getElementById("workspace-subtitle"),
  statusTitle: document.getElementById("status-title"),
  statusNote: document.getElementById("status-note"),
  activeOwner: document.getElementById("active-owner"),
  overviewStats: document.getElementById("overview-stats"),
  signalCount: document.getElementById("signal-count"),
  signalList: document.getElementById("signal-list"),
  focusBadge: document.getElementById("focus-badge"),
  goalTitle: document.getElementById("goal-title"),
  targetUser: document.getElementById("target-user"),
  problemSummary: document.getElementById("problem-summary"),
  stakeholderTags: document.getElementById("stakeholder-tags"),
  journeyStack: document.getElementById("journey-stack"),
  capabilityGrid: document.getElementById("capability-grid"),
  generatedTitle: document.getElementById("generated-title"),
  generatedBody: document.getElementById("generated-body"),
  actionStack: document.getElementById("action-stack"),
  screenCardGrid: document.getElementById("screen-card-grid"),
  sampleDataRow: document.getElementById("sample-data-row"),
  outcomeList: document.getElementById("outcome-list"),
  validationList: document.getElementById("validation-list"),
  nextActionList: document.getElementById("next-action-list"),
  executionStatus: document.getElementById("execution-status"),
  executionList: document.getElementById("execution-list"),
};

function createListItems(items) {
  return items.map((item) => `<li>${item}</li>`).join("");
}

function renderHero() {
  elementMap.heroTitle.textContent = prototypeData.context.prototype_name;
  elementMap.heroBrief.textContent = prototypeData.hero.brief;
  elementMap.heroFlow.textContent = prototypeData.hero.flow;
  elementMap.heroProblem.textContent = prototypeData.hero.problem;
  elementMap.heroTags.innerHTML = prototypeData.hero.tags.map((tag) => `<span>${tag}</span>`).join("");
}

function renderKpis() {
  elementMap.kpiStrip.innerHTML = prototypeData.kpis
    .map(
      (metric) => `
        <article class="kpi-card">
          <p class="mini-label">${metric.detail}</p>
          <strong>${metric.value}</strong>
          <p>${metric.label}</p>
        </article>
      `
    )
    .join("");
}

function renderWorkItems() {
  elementMap.workItemList.innerHTML = prototypeData.work_items
    .map((item, index) => {
      const activeClass = index === state.activeItemIndex ? "is-active" : "";
      return `
        <button class="work-item-card ${activeClass}" data-item-index="${index}" type="button">
          <div class="status-row">
            <span class="mini-label">${item.owner}</span>
            <span class="badge badge-soft">${item.badge}</span>
          </div>
          <strong>${item.name}</strong>
          <p>${item.summary}</p>
        </button>
      `;
    })
    .join("");
}

function renderStaticPanels(activeItem) {
  elementMap.cardChipRow.innerHTML = prototypeData.overview.selected_cards
    .map((card) => `<span>${card}</span>`)
    .join("");
  elementMap.recommendedActions.innerHTML = createListItems(activeItem.recommendations);
  elementMap.pocFocus.textContent = prototypeData.overview.scope || "待补充";
  elementMap.pocNote.textContent = prototypeData.overview.why_now || "当前演示页用于展示当前方案如何落到可访问工作台。";
  elementMap.outcomeList.innerHTML = createListItems(prototypeData.overview.outcomes);
  elementMap.validationList.innerHTML = createListItems(prototypeData.overview.validation_points);
  elementMap.nextActionList.innerHTML = createListItems(prototypeData.overview.next_actions);
  elementMap.sampleDataRow.innerHTML = prototypeData.overview.sample_data
    .map((item) => `<span>${item}</span>`)
    .join("");

  elementMap.capabilityGrid.innerHTML = prototypeData.capability_cards
    .map(
      (card) => `
        <article class="capability-card">
          <p class="mini-label">能力模块</p>
          <strong>${card.title}</strong>
          <p>${card.body}</p>
          ${
            card.products && card.products.length
              ? `<div class="products-row">${card.products.map((product) => `<span>${product}</span>`).join("")}</div>`
              : ""
          }
        </article>
      `
    )
    .join("");

  elementMap.screenCardGrid.innerHTML = prototypeData.screen_cards
    .map(
      (card) => `
        <article class="preview-card">
          <p class="mini-label">页面</p>
          <strong>${card.title}</strong>
          <p>${card.body}</p>
        </article>
      `
    )
    .join("");
}

function renderActiveItem() {
  const item = prototypeData.work_items[state.activeItemIndex];

  elementMap.workspaceTitle.textContent = item.name;
  elementMap.workspaceSubtitle.textContent = item.headline;
  elementMap.statusTitle.textContent = item.badge;
  elementMap.statusNote.textContent = item.focus;
  elementMap.activeOwner.textContent = item.owner;
  elementMap.focusBadge.textContent = item.focus;
  elementMap.goalTitle.textContent = prototypeData.hero.goal;
  elementMap.targetUser.textContent = prototypeData.context.target_user;
  elementMap.problemSummary.textContent = item.summary;
  elementMap.generatedTitle.textContent = item.generated_asset.title;
  elementMap.generatedBody.textContent = item.generated_asset.body;

  elementMap.stakeholderTags.innerHTML = prototypeData.overview.stakeholders
    .map((role) => `<span>${role}</span>`)
    .join("");

  const statCards = [
    { label: "场景名称", value: prototypeData.context.scenario_name },
    { label: "目标角色", value: prototypeData.context.target_user },
    { label: "核心任务", value: item.journey[0] || "待补充" },
    { label: "演示重点", value: item.focus },
  ];
  elementMap.overviewStats.innerHTML = statCards
    .map(
      (card) => `
        <article class="stat-card">
          <p class="mini-label">${card.label}</p>
          <strong>${card.value}</strong>
        </article>
      `
    )
    .join("");

  elementMap.signalList.innerHTML = createListItems(item.signals);
  elementMap.signalCount.textContent = `${item.signals.length} 条`;

  elementMap.journeyStack.innerHTML = item.journey
    .map(
      (step, index) => `
        <article class="journey-step" data-step="${String(index + 1).padStart(2, "0")}">
          <strong>${prototypeData.tabs[index] || "步骤"}</strong>
          <p>${step}</p>
        </article>
      `
    )
    .join("");

  elementMap.actionStack.innerHTML = prototypeData.actions
    .map((label, index) => {
      const primaryClass = index === 0 ? "primary-action" : "";
      return `<button class="action-button ${primaryClass}" data-action-label="${label}" type="button">${label}</button>`;
    })
    .join("");

  renderStaticPanels(item);
  renderExecution();
  renderWorkItems();
}

function renderExecution() {
  const item = prototypeData.work_items[state.activeItemIndex];
  elementMap.executionStatus.textContent = state.runCount
    ? `已模拟 ${state.runCount} 次运行`
    : `${item.badge}，等待演示动作`;
  elementMap.executionList.innerHTML = state.logs
    .slice()
    .reverse()
    .map((entry) => `<li>${entry}</li>`)
    .join("");
}

function setActiveScreen(screen) {
  state.activeScreen = screen;
  document.querySelectorAll(".screen-button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.screen === screen);
  });
  document.querySelectorAll(".screen-panel").forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.screenPanel === screen);
  });
}

function addLog(message) {
  const timestamp = new Date().toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
  state.logs.push(`${timestamp} · ${message}`);
  renderExecution();
}

function simulateRun() {
  state.runCount += 1;
  const item = prototypeData.work_items[state.activeItemIndex];
  const variantMessage = {
    growth: "Copilot 已刷新客群洞察、内容草稿与保留动作建议。",
    service: "Copilot 已更新诊断依据、客服回复与后续处理动作。",
    knowledge: "Copilot 已整理参考知识、答案结构与回写建议。",
    ops: "Copilot 已刷新方案结构、页面草稿与验证动作。",
  }[prototypeData.variant];
  addLog(`${item.name}：${variantMessage}`);
  elementMap.generatedBody.textContent = `${item.generated_asset.body} 当前已完成第 ${state.runCount} 次演示刷新。`;
}

document.getElementById("cycle-item-button")?.addEventListener("click", () => {
  state.activeItemIndex = (state.activeItemIndex + 1) % prototypeData.work_items.length;
  addLog(`已切换到样例：${prototypeData.work_items[state.activeItemIndex].name}`);
  renderActiveItem();
});

document.getElementById("simulate-run-button")?.addEventListener("click", simulateRun);

document.getElementById("work-item-list")?.addEventListener("click", (event) => {
  const target = event.target.closest("[data-item-index]");
  if (!target) return;
  state.activeItemIndex = Number(target.dataset.itemIndex);
  addLog(`已切换到样例：${prototypeData.work_items[state.activeItemIndex].name}`);
  renderActiveItem();
});

document.getElementById("screen-nav")?.addEventListener("click", (event) => {
  const target = event.target.closest("[data-screen]");
  if (!target) return;
  setActiveScreen(target.dataset.screen);
});

document.getElementById("action-stack")?.addEventListener("click", (event) => {
  const target = event.target.closest("[data-action-label]");
  if (!target) return;
  addLog(`已触发动作：${target.dataset.actionLabel}`);
});

renderHero();
renderKpis();
renderActiveItem();
setActiveScreen("overview");
"""


def write_prototype(payload: dict, case_dir: Path) -> Path:
    prototype_dir = case_dir / "mvp-prototype"
    prototype_dir.mkdir(parents=True, exist_ok=True)
    data = build_prototype_data(payload)
    (prototype_dir / "index.html").write_text(render_index_html(data), encoding="utf-8")
    (prototype_dir / "styles.css").write_text(render_styles_css(), encoding="utf-8")
    (prototype_dir / "script.js").write_text(render_script_js(), encoding="utf-8")
    (prototype_dir / "scenario.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return prototype_dir
