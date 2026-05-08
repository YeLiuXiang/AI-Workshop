# Workshop Input Playbook

这份文档只解决一件事：现场怎么整理输入，才能稳定命中已有资产并生成 PPT 与轻量原型规格包。

现在默认交付已经从“只生成 PPT”扩展为“PPT + 轻量原型规格包”。也就是说，同一份客户输入会默认生成：

- 方案 PPT
- `需求PRD.md`
- `方案设计.md`

## 文档怎么用

现在文档结构收成 3 份就够了：

1. `README.md`
   看整体流程、脚本入口、产物关系。
2. `SKILL.md`
   看生成规则、约束、默认叙事顺序。
3. `WORKSHOP-INPUT-PLAYBOOK.md`
   看现场输入怎么写，以及直接可用的示例。

如果只是现场采集输入，优先看这份文档，不需要先读完整个 `README.md`。

## 5 分钟现场模式

如果你的目标是在现场 5 分钟内直接出一版可讲解的 PPT、`需求PRD.md` 和 `方案设计.md`，优先使用快速模式，不要先走 asset-first 补全。

推荐命令：

```powershell
python scripts/generate_workshop_package.py `
  --input examples/live-fast-template.json `
  --workspace-root Workspace `
  --fast
```

这个模式只保留最短路径：

- 现场输入
- 直接标准化成场景 JSON
- 生成 PPT
- 生成 `需求PRD.md`
- 生成 `方案设计.md`

默认不会再生成 `替换映射.json`，也不会去匹配 reference case，目的就是现场稳定出结果，而不是追求最复杂的自动补全。

## 标准输出目录规则

从现在开始，workshop 方案的默认输出根目录统一为 `Workspace/`。

每次输入一个客户场景并生成 PPT 时，都应该在 `Workspace/` 下创建一个中文子目录：

- 子目录命名：`客户名称-场景名称`
- PPT 文件命名：`客户名称-场景名称方案.pptx`

推荐直接使用这个统一入口命令：

```powershell
python scripts/generate_workshop_package.py `
  --input examples/live-input-capture-template.json `
  --workspace-root Workspace
```

默认会把结果落到类似下面的目录中：

```text
Workspace/
  客户名称-场景名称/
    原始输入.json
    组合场景.json
    演示文稿方案.json
    替换映射.json
    需求PRD.md
    方案设计.md
    客户名称-场景名称方案.pptx
```

如果输入本身已经是标准化场景 JSON，则目录里会保存 `场景输入.json`，不会再额外生成 `组合场景.json`。

## 最小输入原则

现场输入不要试图描述完整方案，只要说清三件事：

1. 这是哪一类客户
2. 当前最急的业务问题是什么
3. 客户更容易接受什么原型形态

只要这三件事足够清楚，系统就能用已有 reference case 补全大部分内容。

如果客户明确希望“除了 PPT，还要有一个可快速搭出来的原型壳子”，再额外补少量 `mvp_spec` 字段即可，不需要在现场写完整技术方案。

## 最小输入字段

最少收这 6 个字段：

- `customer_type`
- `scenario_summary`
- `target_role`
- `current_pain_point`
- `expected_value`
- `prototype_preference`

如果要顺带生成更可用的原型文档，建议再补这 5 个字段：

- `mvp_spec.primary_user`
- `mvp_spec.core_task`
- `mvp_spec.screens`
- `mvp_spec.modules`
- `mvp_spec.key_actions`

如果是 5 分钟现场模式，再额外补这 1 个字段最有帮助：

- `current_process`

也就是把现场卡片链路直接整理成 5 到 6 行步骤，系统就可以直接拿这条链路去生成 `目标 AI Flow` 和 PRD/方案设计文档。

建议写法：

- `customer_type`：只写一个 lane，比如 `消费电子 IoT` 或 `跨界电商`
- `scenario_summary`：一句话，只描述一个流程或场景
- `target_role`：只写一个主要角色
- `current_pain_point`：只写一个最急的问题
- `expected_value`：只写客户最想先看到的业务结果
- `prototype_preference`：写短标签，比如 `工作台`、`控制塔`、`助手`、`中枢`

## 推荐填写模板

```json
{
  "workshop": {
    "title": "AI Discovery Card Workshop",
    "customer": "待补充：客户名称",
    "industry": "待补充：行业名称",
    "group_name": "待补充：小组名称",
    "date": "2026-05-22"
  },
  "event_input": {
    "customer_type": "待补充：消费电子 IoT / 跨界电商",
    "scenario_summary": "待补充：一句话描述客户希望优化的业务流程或场景",
    "target_role": "待补充：谁来使用这个原型或流程",
    "current_pain_point": "待补充：当前最急的一个问题",
    "expected_value": "待补充：客户最想看到的业务结果",
    "prototype_preference": "待补充：客户更接受的原型形态"
  },
  "mvp_spec": {
    "prototype_mode": "待补充：前端壳子优先 / 可扩展到简单交互",
    "primary_user": "待补充：原型主要使用者",
    "core_task": "待补充：用户在原型里最核心的一件事",
    "screens": [],
    "modules": [],
    "key_actions": [],
    "sample_data": [],
    "style_keywords": [],
    "tech_stack_preference": "待补充：如 Next.js + Tailwind CSS",
    "out_of_scope": []
  },
  "current_process": [],
  "detected_cards": {
    "business_scenario": [],
    "input_perception": [],
    "understanding_analysis": [],
    "generation_interaction": [],
    "execution_closure": []
  },
  "card_photo_paths": []
}
```

## 现场卡片流程怎么记

不需要真的画图，OCR 后只要能整理成这种文字链路就够了：

`触发事件 -> 读取什么数据/资料 -> AI 做什么判断 -> 生成什么建议/内容 -> 触发什么动作 -> 结果回写到哪里`

这里要区分两层：

- 上面这条“文字流程链路”可以按业务动作自由描述
- 下面 `detected_cards` 里的卡片名，必须只使用 SOP 里五个使用区下“适合放入的卡片类型”中的名称，不要自造卡名

例如：

`用户报修 -> 读取设备状态和历史工单 -> AI 识别故障类型 -> 生成排障建议 -> 创建工单或升级专家 -> 处理结果回写知识库`

## `detected_cards` 允许使用的卡片类型

`business_scenario`

- `智能体类卡片`
- `数据和预测分析中偏业务目标的卡片`
- `内容生成中偏营销、网页、内容生产的卡片`

`input_perception`

- `视觉感知`
- `语音识别`
- `图像识别`
- `OCR`
- `表单理解`
- `环境感知`

`understanding_analysis`

- `文本理解`
- `情绪分析`
- `用户意图识别`
- `数据分析`
- `风险预测`
- `异常检测`
- `客户洞察`

`generation_interaction`

- `自动回答`
- `自然对话`
- `文本生成`
- `图像生成`
- `语音合成`
- `翻译`
- `网页生成`
- `营销内容生成`

`execution_closure`

- `智能体`
- `流程优化`
- `自动履行`
- `路径规划`
- `人机交互`
- `生产力`
- `安全运营`
- `决策制定`

## 示例 1：消费电子 IoT / 智能售后服务

### 现场卡片流程文字版

`用户报修或客服接单 -> 读取设备状态、历史工单、FAQ -> AI 判断问题类型和优先级 -> 生成回复与排障建议 -> 复杂问题升级工单 -> 处理结果回写知识库`

### 场景描述文案

客户希望把传统售后从“人工查资料、人工找专家”升级为“设备状态驱动的智能服务闭环”。现场最典型的问题不是没有数据，而是设备状态、历史工单和知识资料彼此割裂，导致客服定位慢、复杂问题升级频繁、经验难以复用。这个场景适合先做一个智能售后服务工作台，用来验证 AI 对问题识别、回复生成和服务动作联动的直接价值。

### 输入示例

```json
{
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
    "understanding_analysis": ["用户意图识别", "异常检测"],
    "generation_interaction": ["自动回答", "自然对话", "文本生成"],
    "execution_closure": ["流程优化", "自动履行", "人机交互"]
  }
}
```

## 示例 2：消费电子 IoT / 全球设备运营

### 现场卡片流程文字版

`区域设备持续上报指标 -> 汇总在线率、故障率、固件版本和能耗 -> AI 识别异常区域或异常批次 -> 生成运营解释和优先级 -> 触发扩容、限流、OTA 或人工复核 -> 结果回写运营规则`

### 场景描述文案

客户已经具备全球设备接入和基础报表能力，但区域之间指标口径不统一，异常发现和动作协同仍然依赖人工。真正要验证的不是单一看板，而是一个能让总部和区域团队共同使用的全球运营指挥台。这个场景的核心价值在于，把连接、故障、固件和能耗这些技术指标，转成可判断、可协同、可执行的运营动作。

### 输入示例

```json
{
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
  }
}
```

## 示例 3：跨界电商 / 营销增长与流失预警

### 现场卡片流程文字版

`准备新一轮营销活动 -> 读取客户画像、活动数据、渠道反馈 -> AI 识别高价值客群和流失风险 -> 生成文案、页面建议和活动策略 -> 触发营销动作和 retention 跟进 -> 活动结果回写并复盘`

### 场景描述文案

客户不是缺营销动作，而是缺一个把客户洞察、内容生产和增长执行真正串起来的 AI 工作流。当前常见问题是内容生产周期长、活动复盘慢、流失预警不及时。这个场景适合先做营销增长与客户保留工作台，快速验证 AI 在客群识别、内容生成和 retention 动作推荐上的业务价值。

### 输入示例

```json
{
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
  }
}
```

## 示例 4：跨界电商 / 库存与履约控制塔

### 现场卡片流程文字版

`订单和库存持续变化 -> 汇总库存、订单、退货和仓配数据 -> AI 判断缺货、积压和履约风险 -> 生成补货、调拨和仓配建议 -> 触发区域协同和运营任务 -> 结果回写控制塔与复盘口径`

### 场景描述文案

客户面对的核心问题不是单点库存优化，而是跨区域订单、库存和履约异常之间缺少统一判断和联动。当前运营经常同时面对缺货和积压，补货调拨决策依赖人工拼表。这个场景适合先做库存与履约控制塔，验证 AI 对风险识别、协同建议和动作优先级的价值，再逐步扩展到更完整的供应链优化。

### 输入示例

```json
{
  "event_input": {
    "customer_type": "跨界电商",
    "scenario_summary": "希望针对跨区域订单履约和库存协同场景，设计一个能结合订单、库存和退货数据的 AI 运营流程。",
    "target_role": "供应链负责人",
    "current_pain_point": "不同区域经常同时出现缺货和积压，履约异常发现不及时。",
    "expected_value": "希望更快完成补货调拨判断，并提升履约稳定性。",
    "prototype_preference": "库存与履约控制塔"
  },
  "detected_cards": {
    "business_scenario": ["数据和预测分析中偏业务目标的卡片"],
    "input_perception": ["表单理解"],
    "understanding_analysis": ["数据分析", "风险预测"],
    "generation_interaction": ["文本生成"],
    "execution_closure": ["流程优化", "自动履行", "决策制定"]
  }
}
```

## 现场使用建议

现场主持人按这个顺序收集信息就够了：

1. 先判断客户属于 `消费电子 IoT` 还是 `跨界电商`
2. 用一句话写 `scenario_summary`
3. 只锁一个 `target_role`
4. 只写一个 `current_pain_point`
5. 只写一个 `expected_value`
6. 补一个 `prototype_preference`
7. 最后再补卡片分类和卡片流程文字版

如果现场时间很短，先把 1 到 6 写完，再补卡片信息，不要一开始就整理复杂流程图。