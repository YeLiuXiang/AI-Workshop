# 输入参考 Demo

这份文档基于当前项目的实际用法重新整理，目标不是替代 [WORKSHOP-INPUT-PLAYBOOK.md](F:/VsCodeProject/AI-Workshop/ppt-generation-enterprise/WORKSHOP-INPUT-PLAYBOOK.md) 或 [live-input-field-guide.md](F:/VsCodeProject/AI-Workshop/ppt-generation-enterprise/examples/live-input-field-guide.md)，而是提供一份更适合直接复制、改字、落地的输入案例集合。

## 当前推荐怎么用

当前项目建议把输入分成两类：

1. 稀疏现场输入
   适合 workshop 现场快速整理卡片结果，走 asset-first 路线。
   推荐从 `examples/live-input-capture-template.json` 或下面的稀疏案例开始。

2. 标准化场景输入
   适合客户文案已经收敛，希望尽量保留措辞，不希望被 reference case 自动改写。
   推荐直接使用完整 `scenario` 结构输入。

## 推荐命令

### 稀疏输入

```powershell
python scripts/generate_workshop_package.py `
  --input examples/live-sparse-consumer-electronics.json `
  --workspace-root Workspace
```

### 标准化输入

```powershell
python scripts/generate_workshop_package.py `
  --input Workspace/某消费电子客户-智能售后服务闭环/场景输入.json `
  --workspace-root Workspace
```

## 选型建议

- 现场卡片刚整理完：优先用“稀疏输入”
- 客户口径已经确定：优先用“标准化输入”
- 希望顺带生成前端壳子 PRD：补 `mvp_spec`
- 希望后续 wording 更稳定：不要只依赖 `live-sparse-*.json`，尽快转成标准化输入

---

## Demo 1：消费电子 IoT / 智能售后服务工作台

适合场景：设备状态、历史工单、FAQ 分散，客服定位慢，复杂问题频繁升级。

```json
{
  "workshop": {
    "title": "AI Discovery Card Workshop",
    "customer": "某消费电子客户",
    "industry": "消费电子 IoT",
    "group_name": "第 1 组",
    "date": "2026-05-22"
  },
  "event_input": {
    "customer_type": "消费电子 IoT",
    "scenario_summary": "希望针对售后服务场景，设计一个能结合设备状态、历史工单和知识库的 AI 服务流程。",
    "target_role": "售后负责人",
    "current_pain_point": "客服定位问题慢，复杂问题需要频繁升级专家。",
    "expected_value": "希望提升首响效率，并形成主动服务闭环。",
    "prototype_preference": "智能售后服务工作台"
  },
  "detected_cards": {
    "business_scenario": ["智能体类卡片"],
    "input_perception": ["语音识别", "OCR"],
    "understanding_analysis": ["异常检测", "用户意图识别"],
    "generation_interaction": ["自动回答", "自然对话", "文本生成"],
    "execution_closure": ["流程优化", "自动履行", "人机交互"]
  },
  "card_photo_paths": ["AI WorkFlow.png"]
}
```

---

## Demo 2：消费电子 IoT / 全球设备运营指挥台

适合场景：多区域设备在线率、故障率、固件风险不在一个统一决策视图中。

```json
{
  "workshop": {
    "title": "AI Discovery Card Workshop",
    "customer": "某出海智能硬件客户",
    "industry": "消费电子 IoT",
    "group_name": "第 5 组",
    "date": "2026-05-22"
  },
  "event_input": {
    "customer_type": "消费电子 IoT",
    "scenario_summary": "希望针对全球设备运营场景，设计一个能结合在线率、故障率和固件指标的 AI 运营闭环。",
    "target_role": "全球运营负责人",
    "current_pain_point": "各区域指标口径不统一，区域异常和固件风险发现不及时。",
    "expected_value": "希望建立统一的全球运营监控和动作协同机制。",
    "prototype_preference": "全球设备运营指挥台"
  },
  "detected_cards": {
    "business_scenario": ["数据和预测分析中偏业务目标的卡片"],
    "input_perception": ["环境感知"],
    "understanding_analysis": ["数据分析", "异常检测", "风险预测"],
    "generation_interaction": ["文本生成"],
    "execution_closure": ["流程优化", "自动履行", "决策制定"]
  },
  "card_photo_paths": ["AI WorkFlow.png"]
}
```

---

## Demo 3：消费电子 IoT / 安全治理中枢

适合场景：认证日志、证书状态、审计事件分散，安全负责人缺少统一的风险研判与响应入口。

```json
{
  "workshop": {
    "title": "AI Discovery Card Workshop",
    "customer": "某全球化 IoT 品牌",
    "industry": "消费电子 IoT",
    "group_name": "第 6 组",
    "date": "2026-05-22"
  },
  "event_input": {
    "customer_type": "消费电子 IoT",
    "scenario_summary": "希望针对设备接入安全场景，设计一个能结合认证日志、证书状态和审计事件的 AI 风险治理流程。",
    "target_role": "安全负责人",
    "current_pain_point": "认证失败和越权风险分散在不同区域，安全事件响应效率低。",
    "expected_value": "希望建立统一的风险识别、研判和自动化响应闭环。",
    "prototype_preference": "IoT 安全治理中枢"
  },
  "detected_cards": {
    "business_scenario": ["数据和预测分析中偏业务目标的卡片"],
    "input_perception": ["环境感知"],
    "understanding_analysis": ["异常检测", "风险预测", "数据分析"],
    "generation_interaction": ["文本生成"],
    "execution_closure": ["流程优化", "自动履行", "安全运营"]
  },
  "card_photo_paths": ["AI WorkFlow.png"]
}
```

---

## Demo 4：跨界电商 / 营销增长与客户保留工作台

适合场景：营销负责人希望把客户画像、活动数据和内容生产串起来，同时补上流失预警与干预。

```json
{
  "workshop": {
    "title": "AI Discovery Card Workshop",
    "customer": "某跨界电商品牌",
    "industry": "跨界电商",
    "group_name": "第 2 组",
    "date": "2026-05-22"
  },
  "event_input": {
    "customer_type": "跨界电商",
    "scenario_summary": "希望针对跨境营销场景，设计一个能结合客户画像、活动数据和内容生产的 AI 流程。",
    "target_role": "营销负责人",
    "current_pain_point": "内容生产和活动复盘周期长，流失预警不及时。",
    "expected_value": "希望更快完成个性化营销和高风险客户干预。",
    "prototype_preference": "营销增长与客户保留工作台"
  },
  "detected_cards": {
    "business_scenario": ["内容生成中偏营销、网页、内容生产的卡片"],
    "input_perception": ["表单理解"],
    "understanding_analysis": ["客户洞察", "数据分析", "风险预测"],
    "generation_interaction": ["文本生成", "网页生成", "营销内容生成"],
    "execution_closure": ["流程优化", "自动履行", "决策制定"]
  },
  "card_photo_paths": ["AI WorkFlow.png"]
}
```

---

## Demo 5：跨界电商 / 库存与履约控制塔

适合场景：客户已经明确希望连同前端壳子一起出，所以建议直接补齐 `mvp_spec`。

```json
{
  "workshop": {
    "title": "AI Discovery Card Workshop",
    "customer": "跨境电商客户",
    "industry": "跨境电商",
    "group_name": "现场共创组",
    "date": "2026-05-08"
  },
  "event_input": {
    "customer_type": "跨界电商",
    "scenario_summary": "希望针对跨区域订单、库存和履约异常协同场景，设计一个能联动补货、调拨和仓配建议的 AI 控制塔流程。",
    "target_role": "供应链负责人",
    "current_pain_point": "跨区域订单、库存和履约异常缺少统一判断与联动，补货调拨仍依赖人工拼表。",
    "expected_value": "希望先验证 AI 对缺货、积压和履约风险识别及协同建议的价值。",
    "prototype_preference": "库存与履约控制塔"
  },
  "mvp_spec": {
    "prototype_mode": "前端壳子优先",
    "primary_user": "供应链负责人",
    "core_task": "在一个控制塔界面里完成库存履约风险判断、建议查看和协同任务触发。",
    "screens": [
      "全局风险总览",
      "区域库存与订单分析页",
      "补货调拨建议页",
      "协同任务与复盘页"
    ],
    "modules": [
      "区域风险地图",
      "缺货与积压预警卡片",
      "履约异常解释区",
      "补货调拨建议列表",
      "协同任务面板"
    ],
    "key_actions": [
      "切换区域查看库存与订单风险",
      "查看 AI 给出的补货调拨建议",
      "触发区域协同任务",
      "回看执行结果与复盘口径"
    ],
    "sample_data": [
      "区域库存样例",
      "订单波动样例",
      "退货原因样例",
      "履约异常样例"
    ],
    "style_keywords": ["企业级", "控制塔", "运营看板"],
    "tech_stack_preference": "Next.js + Tailwind CSS",
    "out_of_scope": [
      "不接真实 ERP 或 WMS 接口",
      "不直接执行自动补货下单",
      "不实现正式权限体系"
    ]
  },
  "current_process": [
    "订单和库存持续变化",
    "汇总库存、订单、退货和仓配数据",
    "AI 判断缺货、积压和履约风险",
    "生成补货、调拨和仓配建议",
    "触发区域协同和运营任务",
    "结果回写控制塔与复盘口径"
  ],
  "detected_cards": {
    "business_scenario": ["数据和预测分析中偏业务目标的卡片"],
    "input_perception": ["表单理解"],
    "understanding_analysis": ["数据分析", "风险预测", "异常检测"],
    "generation_interaction": ["文本生成"],
    "execution_closure": ["流程优化", "自动履行", "决策制定"]
  },
  "card_photo_paths": []
}
```

---

## Demo 6：标准化输入 / 智能售后服务闭环

适合场景：客户文案已经定稿，希望保留业务问题、AI Flow、价值表述和原型口径，不想让资产匹配再做较大改写。

```json
{
  "workshop": {
    "title": "AI Discovery Card Workshop",
    "customer": "某消费电子客户",
    "industry": "消费电子 IoT",
    "group_name": "第 1 组",
    "date": "2026-05-08"
  },
  "scenario": {
    "name": "智能售后服务闭环",
    "target_users": "售后负责人",
    "business_problem": "设备状态、历史工单和知识资料彼此割裂，导致客服定位慢、复杂问题升级频繁、经验难以复用。",
    "improvement_goal": "以设备状态驱动的方式提升问题识别效率、回复质量和服务闭环能力。"
  },
  "opportunity": {
    "statement": "把传统售后从人工查资料、人工找专家升级为设备状态驱动的智能服务闭环，是消费电子 IoT 企业提升服务体验与运营效率的直接切口。",
    "why_now": "企业通常已经沉淀了设备状态数据、历史工单和 FAQ，但这些资产分散在不同系统中，正适合通过 AI 工作台快速验证串联价值。",
    "supporting_points": [
      "服务体验正在成为消费电子品牌差异化的重要抓手",
      "设备在线状态与历史工单已具备作为诊断上下文的基础",
      "AI 可以把识别、回复、升级与知识沉淀串成闭环",
      "先建设智能售后服务工作台，适合低风险验证直接业务价值"
    ]
  },
  "current_process": [
    "客户报修后，客服需要人工确认设备型号、状态和问题描述",
    "客服切换多个系统查看历史工单、FAQ 和维修资料",
    "问题判断依赖个人经验，回复质量与处理速度波动较大",
    "复杂问题频繁升级专家或二线支持，服务链路变长",
    "处理结果虽然回写工单系统，但经验难以沉淀复用"
  ],
  "pain_points": [
    "设备状态、历史工单和知识资料彼此割裂，诊断定位慢",
    "客服定位问题慢，复杂问题升级频繁，首响效率受影响",
    "人工查资料和找专家的模式导致服务成本高且稳定性差",
    "处理经验无法持续沉淀为可复用的知识资产"
  ],
  "selected_cards": {
    "business_scenario": ["智能体类卡片"],
    "input_perception": ["OCR"],
    "understanding_analysis": ["用户意图识别", "异常检测"],
    "generation_interaction": ["自动回答", "自然对话", "文本生成"],
    "execution_closure": ["流程优化", "自动履行", "人机交互"]
  },
  "ai_flow": {
    "trigger": "用户报修或客服接单",
    "steps": [
      "系统读取设备状态、历史工单与 FAQ 等知识资料",
      "AI 判断问题类型、风险等级和处理优先级",
      "AI 生成客户回复与排障建议，支持一线客服快速响应",
      "复杂问题自动升级工单或转交专家继续处理",
      "处理结果回写知识库与服务系统，持续沉淀经验"
    ],
    "closure": "形成从问题识别、服务响应、工单升级到知识沉淀的智能售后服务闭环",
    "narrative": "这个场景聚焦客服与售后协同最典型的高频链路，用一个工作台把数据读取、问题识别、回复生成与服务动作联动起来，便于快速验证 AI 的直接业务价值。"
  },
  "prototype": {
    "name": "智能售后服务工作台",
    "goal": "为客服和售后人员提供一个结合设备状态、历史工单、FAQ 与工单动作的统一服务入口",
    "surface": "智能售后服务工作台",
    "user_flow": [
      "接收报修请求后自动汇总设备上下文与历史服务记录",
      "展示 AI 判断的问题类型、优先级与推荐处置路径",
      "一键生成回复建议、排障动作和升级工单"
    ],
    "mock_scope": [
      "设备状态与客户上下文面板",
      "AI 诊断与知识召回面板",
      "回复建议与工单动作面板"
    ],
    "value_statement": "让客服从人工翻资料、人工找专家，转向在一个工作台里完成识别、回复、排障和动作触发。"
  },
  "source_type": "normalized-workshop-scenario"
}
```

---

## 最后怎么选

- 想要最快出一版 PPT：用 Demo 1 到 Demo 5 这种稀疏输入
- 想要文案更可控、更贴近客户原话：用 Demo 6 这种标准化输入
- 想顺带产出前端壳子 PRD：至少补上 `mvp_spec.primary_user`、`mvp_spec.core_task`、`mvp_spec.screens`、`mvp_spec.modules`、`mvp_spec.key_actions`
- 想降低后续目录混乱：新输入尽量放在 `examples/` 或直接放到 `Workspace/<客户-场景>/场景输入.json`，不要再往 `workspace/` 根层平铺新的临时 JSON