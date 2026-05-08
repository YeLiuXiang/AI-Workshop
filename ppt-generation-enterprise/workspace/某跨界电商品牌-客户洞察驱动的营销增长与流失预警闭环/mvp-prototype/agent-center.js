const agents = [
  {
    id: "insight-agent",
    name: "客户洞察 Agent",
    domain: "洞察",
    owner: "营销负责人",
    stage: "客群识别阶段",
    summary: "聚合客户画像、活动历史、站点行为和渠道反馈，形成客群细分与增长机会判断。",
    value: "让团队先知道该打谁、为什么打、机会在哪。",
    trigger: "活动立项或目标客群切换时触发",
    positioning: "这个 Agent 负责把原本分散在 CRM、活动报表和行为数据里的信号拉到一处，输出可讲可用的客群洞察，而不是直接替代策略决策。",
    inputs: ["客户画像标签", "历史活动结果", "站点行为数据", "渠道反馈摘要"],
    outputs: ["高价值客群清单", "潜在流失客群识别", "活动切入机会点", "优先级排序建议"],
    config: [
      { label: "推理模式", value: "洞察归因 + 客群分层" },
      { label: "主数据源", value: "Customer Insights / Fabric" },
      { label: "更新频率", value: "按活动周期或每日刷新" },
      { label: "展示口径", value: "客群、风险、价值、机会四象限" }
    ],
    tools: ["客户标签查询", "活动数据聚合", "行为趋势分析", "站点画像读取"],
    guardrails: ["不直接改写原始客户标签", "高风险判断需附可解释依据", "敏感客群仅展示聚合口径"],
    handoffs: [
      "接收业务目标和站点范围",
      "输出目标客群与优先级给活动策略 Agent",
      "将流失风险清单同步给流失预警 Agent"
    ],
    outOfScope: ["不直接发送营销触达", "不替代人工业务定价", "不写入 CRM 主数据"],
    note: "这是整个场景的前置 Agent，核心不是多智能，而是先把增长决策的上下文收全。"
  },
  {
    id: "strategy-agent",
    name: "活动策略 Agent",
    domain: "增长",
    owner: "增长运营负责人",
    stage: "活动策划阶段",
    summary: "基于客群洞察和历史活动表现，为不同国家站点输出活动策略、优先级和实验方向。",
    value: "把“要做什么活动”从经验拍板变成有上下文支撑的策略建议。",
    trigger: "客群确定后、内容生成前触发",
    positioning: "这个 Agent 更像策略副驾，不直接产出最终营销素材，而是定义主题、节奏、权益、页面重心和试验方向。",
    inputs: ["目标客群包", "增长目标", "历史活动 uplift", "库存与履约约束"],
    outputs: ["活动主题建议", "渠道组合建议", "权益设计建议", "A/B 测试方向"],
    config: [
      { label: "策略视角", value: "增长目标优先" },
      { label: "约束纳入", value: "库存、毛利、履约承诺" },
      { label: "结果形式", value: "活动方案卡 + 优先级建议" },
      { label: "适用节奏", value: "周度 / 大促前 / 试点活动" }
    ],
    tools: ["历史活动分析", "商品组合建议", "权益模板库", "站点策略对照表"],
    guardrails: ["不能绕过库存约束", "策略建议需对应明确目标客群", "不得输出不可兑现的权益方案"],
    handoffs: [
      "读取客户洞察 Agent 的客群分层结果",
      "把主题、权益和页面重点交给营销内容 Agent",
      "把实验设计同步给活动复盘 Agent"
    ],
    outOfScope: ["不直接生成成品文案", "不执行实际发券", "不决定最终预算投放"],
    note: "它决定活动该怎么打，但不代替内容 Agent 去写每一条文案。"
  },
  {
    id: "content-agent",
    name: "营销内容 Agent",
    domain: "内容",
    owner: "内容运营负责人",
    stage: "内容生产阶段",
    summary: "根据活动策略与目标客群，生成多语言文案、卖点结构、触达话术和页面首屏表达。",
    value: "缩短内容从 brief 到可演示版本的时间。",
    trigger: "活动主题和权益方案确定后触发",
    positioning: "这个 Agent 是内容工位的主力，负责文案结构和表达，不假设自己拥有最终业务拍板权。",
    inputs: ["活动主题", "客群洞察摘要", "品牌表达规范", "权益与商品信息"],
    outputs: ["首屏标题", "主文案与副文案", "触达话术包", "多语言页面块建议"],
    config: [
      { label: "内容模式", value: "多语言营销生成" },
      { label: "输出格式", value: "标题 / 副标题 / CTA / 话术包" },
      { label: "品牌约束", value: "品牌语气、禁用词、权益边界" },
      { label: "本地化级别", value: "站点级语言适配" }
    ],
    tools: ["Prompt 模板库", "品牌术语表", "多语言重写", "文案审校规则"],
    guardrails: ["不得夸大权益", "需避免违规促销表达", "敏感词和夸张承诺必须拦截"],
    handoffs: [
      "接收活动策略 Agent 的主题与权益定义",
      "将页面结构和首屏表达传给页面编排 Agent",
      "将触达文案同步给流失预警 Agent"
    ],
    outOfScope: ["不生成最终视觉设计稿", "不直接发布页面", "不执行群发消息"],
    note: "这是最容易被理解的 Agent，但在方案里需要强调它受品牌和业务护栏约束。"
  },
  {
    id: "page-agent",
    name: "页面编排 Agent",
    domain: "内容",
    owner: "数字化产品负责人",
    stage: "页面搭建阶段",
    summary: "把活动文案、模块优先级和本地化元素拼装成一个 landing 页配置建议。",
    value: "把“页面怎么摆”从口头沟通变成结构化配置。",
    trigger: "营销内容 Agent 输出页面素材建议后触发",
    positioning: "这个 Agent 更像页面装配师，目标是输出页面模块配置和排版建议，不承担最终开发发布。",
    inputs: ["页面首屏文案", "模块优先级", "本地化约束", "信任元素要求"],
    outputs: ["页面模块树", "首屏布局建议", "CTA 区块配置", "FAQ 与信任区建议"],
    config: [
      { label: "页面模式", value: "营销落地页配置" },
      { label: "组件来源", value: "模块库 / 组件模板" },
      { label: "布局策略", value: "首屏优先 + 模块化排列" },
      { label: "输出载体", value: "页面配置 JSON / 原型建议" }
    ],
    tools: ["页面模块模板库", "组件映射表", "首屏配置建议", "本地化布局规则"],
    guardrails: ["不输出无法实现的自定义模块", "必须标注哪些内容需要人工确认", "不能跳过品牌和法务块位"],
    handoffs: [
      "接收营销内容 Agent 的首屏与模块建议",
      "把页面结构交给前端壳子或设计团队",
      "将页面版本信息同步给活动复盘 Agent"
    ],
    outOfScope: ["不直接上线页面", "不替代设计系统", "不接真实 CMS 发布"],
    note: "如果需要展示“能力配置页”感，这个 Agent 的存在最容易让客户看到系统化编排价值。"
  },
  {
    id: "analysis-agent",
    name: "活动复盘 Agent",
    domain: "分析",
    owner: "数据分析负责人",
    stage: "活动复盘阶段",
    summary: "对活动效果做简化归因、关键指标对比和下一轮优化建议输出。",
    value: "让复盘从人工拉报表变成结构化、可回流的分析结论。",
    trigger: "活动上线后按天或按周期触发",
    positioning: "这个 Agent 的任务不是替代完整 BI，而是把活动相关结论提炼成增长团队可直接继续使用的复盘资产。",
    inputs: ["曝光点击转化数据", "客群表现分层", "页面版本信息", "实验分流结果"],
    outputs: ["关键指标摘要", "表现异常提示", "下一轮优化建议", "复盘摘要卡"],
    config: [
      { label: "分析模式", value: "增长复盘摘要" },
      { label: "口径维度", value: "客群 / 站点 / 页面版本" },
      { label: "节奏", value: "每日监控 + 周度复盘" },
      { label: "输出形式", value: "指标卡 + 学习结论" }
    ],
    tools: ["指标聚合", "异常对比", "实验结果解读", "复盘摘要模板"],
    guardrails: ["必须标注口径时间窗", "不能把相关性直接写成因果", "异常结论需附数据依据"],
    handoffs: [
      "接收页面版本与活动策略定义",
      "把优化建议回流给活动策略 Agent",
      "把流失信号同步给流失预警 Agent"
    ],
    outOfScope: ["不替代完整数仓建模", "不直接修改投放预算", "不对外生成财务口径结论"],
    note: "在客户汇报里，这个 Agent 能把“闭环”说完整。"
  },
  {
    id: "retention-agent",
    name: "流失预警 Agent",
    domain: "保留",
    owner: "CRM 运营负责人",
    stage: "保留干预阶段",
    summary: "识别高风险客群，生成优先级清单、保留权益建议和跟进动作草案。",
    value: "让客户保留不再等到复盘之后才开始。",
    trigger: "高风险行为信号出现或活动后流失概率提升时触发",
    positioning: "这个 Agent 是当前业务场景里最接近动作闭环的一环，但仍然主要负责建议和排序，不直接替代人工 CRM 触达。",
    inputs: ["流失风险分数", "高价值客户标签", "历史互动记录", "可用权益池"],
    outputs: ["高风险名单", "保留动作建议", "CRM 跟进任务草案", "回访优先级排序"],
    config: [
      { label: "预警模式", value: "风险识别 + 优先级排序" },
      { label: "动作模板", value: "权益包 / 旅程 / CRM 任务" },
      { label: "刷新节奏", value: "实时信号 + 每日批次" },
      { label: "输出视图", value: "高风险清单 + 动作面板" }
    ],
    tools: ["流失评分读取", "权益包模板库", "CRM 任务草案", "回访排序规则"],
    guardrails: ["高价值客户动作需人工确认", "不能自动执行大规模触达", "要避免重复骚扰同一客群"],
    handoffs: [
      "接收客户洞察与复盘 Agent 的风险信号",
      "将任务草案同步给 CRM 执行团队",
      "把执行反馈回流给活动复盘 Agent"
    ],
    outOfScope: ["不直接发送短信或邮件", "不改写会员权益主规则", "不替代人工客服处理投诉"],
    note: "这个 Agent 最适合放在展示页里作为“客户保留闭环”的落点。"
  }
];

const topSignals = [
  { value: "6", label: "候选 Agent 数量" },
  { value: "5", label: "覆盖业务域" },
  { value: "6", label: "推荐协同环节" },
  { value: "0", label: "真实执行依赖" }
];

const state = {
  selectedAgentId: agents[0].id,
  activeFilter: "全部",
  activeTab: "capability"
};

const elements = {
  heroChain: document.getElementById("hero-chain"),
  agentCount: document.getElementById("agent-count"),
  domainCount: document.getElementById("domain-count"),
  signalStrip: document.getElementById("signal-strip"),
  filterRow: document.getElementById("filter-row"),
  agentCardList: document.getElementById("agent-card-list"),
  agentName: document.getElementById("agent-name"),
  agentSummary: document.getElementById("agent-summary"),
  agentOwner: document.getElementById("agent-owner"),
  agentStage: document.getElementById("agent-stage"),
  agentDomain: document.getElementById("agent-domain"),
  agentValue: document.getElementById("agent-value"),
  agentTrigger: document.getElementById("agent-trigger"),
  agentPositioning: document.getElementById("agent-positioning"),
  agentInputs: document.getElementById("agent-inputs"),
  agentOutputs: document.getElementById("agent-outputs"),
  configList: document.getElementById("config-list"),
  toolList: document.getElementById("tool-list"),
  guardrailList: document.getElementById("guardrail-list"),
  handoffList: document.getElementById("handoff-list"),
  outOfScopeList: document.getElementById("out-of-scope-list"),
  collabNote: document.getElementById("collab-note"),
  chainGrid: document.getElementById("chain-grid"),
  nextAgentButton: document.getElementById("next-agent-button")
};

function getVisibleAgents() {
  return agents.filter((agent) => state.activeFilter === "全部" || agent.domain === state.activeFilter);
}

function getCurrentAgent() {
  return agents.find((agent) => agent.id === state.selectedAgentId) ?? agents[0];
}

function renderSignals() {
  elements.signalStrip.innerHTML = topSignals
    .map(
      (item) => `
        <article class="signal-card">
          <strong>${item.value}</strong>
          <p>${item.label}</p>
        </article>`
    )
    .join("");

  elements.agentCount.textContent = String(agents.length);
  elements.domainCount.textContent = String(new Set(agents.map((agent) => agent.domain)).size);
  elements.heroChain.textContent = agents.map((agent) => agent.name.replace(" Agent", "")).join(" -> ");
}

function renderFilters() {
  const filters = ["全部", ...new Set(agents.map((agent) => agent.domain))];
  elements.filterRow.innerHTML = filters
    .map(
      (filter) => `
        <button class="filter-button ${state.activeFilter === filter ? "is-active" : ""}" data-filter="${filter}" type="button">
          ${filter}
        </button>`
    )
    .join("");
}

function renderAgentCards() {
  const visibleAgents = getVisibleAgents();

  elements.agentCardList.innerHTML = visibleAgents
    .map(
      (agent) => `
        <article class="agent-card ${agent.id === state.selectedAgentId ? "is-active" : ""}" data-agent-id="${agent.id}">
          <div class="agent-card-head">
            <div>
              <h3>${agent.name}</h3>
              <p>${agent.summary}</p>
            </div>
            <span class="domain-chip">${agent.domain}</span>
          </div>
          <div class="agent-meta">
            <span class="agent-chip">${agent.owner}</span>
            <span class="agent-chip">${agent.stage}</span>
          </div>
        </article>`
    )
    .join("");
}

function renderDetail() {
  const agent = getCurrentAgent();
  elements.agentName.textContent = agent.name;
  elements.agentSummary.textContent = agent.summary;
  elements.agentOwner.textContent = agent.owner;
  elements.agentStage.textContent = agent.stage;
  elements.agentDomain.textContent = agent.domain;
  elements.agentValue.textContent = agent.value;
  elements.agentTrigger.textContent = agent.trigger;
  elements.agentPositioning.textContent = agent.positioning;

  elements.agentInputs.innerHTML = agent.inputs.map((item) => `<li>${item}</li>`).join("");
  elements.agentOutputs.innerHTML = agent.outputs.map((item) => `<li>${item}</li>`).join("");
  elements.configList.innerHTML = agent.config
    .map(
      (item) => `
        <article class="config-item">
          <strong>${item.label}</strong>
          <p>${item.value}</p>
        </article>`
    )
    .join("");
  elements.toolList.innerHTML = agent.tools.map((item) => `<li>${item}</li>`).join("");
  elements.guardrailList.innerHTML = agent.guardrails.map((item) => `<li>${item}</li>`).join("");
  elements.handoffList.innerHTML = agent.handoffs
    .map(
      (item, index) => `
        <article class="flow-step">
          <span class="step-index">${index + 1}</span>
          <p>${item}</p>
        </article>`
    )
    .join("");
  elements.outOfScopeList.innerHTML = agent.outOfScope.map((item) => `<li>${item}</li>`).join("");
  elements.collabNote.textContent = agent.note;
}

function renderTabs() {
  document.querySelectorAll(".tab-button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.tab === state.activeTab);
  });

  document.querySelectorAll("[data-tab-panel]").forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.tabPanel === state.activeTab);
  });
}

function renderChain() {
  elements.chainGrid.innerHTML = agents
    .map(
      (agent, index) => `
        <article class="chain-card ${agent.id === state.selectedAgentId ? "is-active" : ""}" data-agent-id="${agent.id}">
          <p class="mini-label">Step ${index + 1}</p>
          <strong>${agent.name}</strong>
          <span class="domain-chip">${agent.domain}</span>
          <p class="chain-caption">${agent.summary}</p>
        </article>`
    )
    .join("");
}

function rerender() {
  renderFilters();
  renderAgentCards();
  renderDetail();
  renderTabs();
  renderChain();
}

document.addEventListener("click", (event) => {
  const filterButton = event.target.closest("[data-filter]");
  if (filterButton) {
    state.activeFilter = filterButton.dataset.filter;
    state.activeTab = "capability";
    const visibleAgents = getVisibleAgents();
    if (!visibleAgents.some((agent) => agent.id === state.selectedAgentId)) {
      state.selectedAgentId = visibleAgents[0]?.id ?? agents[0].id;
    }
    rerender();
    return;
  }

  const agentCard = event.target.closest("[data-agent-id]");
  if (agentCard) {
    state.selectedAgentId = agentCard.dataset.agentId;
    state.activeTab = "capability";
    rerender();
    return;
  }

  const tabButton = event.target.closest("[data-tab]");
  if (tabButton) {
    state.activeTab = tabButton.dataset.tab;
    renderTabs();
  }
});

elements.nextAgentButton.addEventListener("click", () => {
  const visibleAgents = getVisibleAgents();
  const currentIndex = visibleAgents.findIndex((agent) => agent.id === state.selectedAgentId);
  const nextAgent = visibleAgents[(currentIndex + 1) % visibleAgents.length] ?? agents[0];
  state.selectedAgentId = nextAgent.id;
  state.activeTab = "capability";
  rerender();
});

renderSignals();
rerender();