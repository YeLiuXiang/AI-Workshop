const segments = [
  {
    id: "eu-high-value",
    market: "欧洲站",
    audience: "高价值复购客群",
    title: "欧洲站高价值客群增长机会",
    summary: "高价值复购用户最近 14 天访问频次上升，但复购转化开始放缓，适合用会员权益和套装组合拉动下一轮转化。",
    tags: ["高客单", "复购放缓", "会员权益"],
    score: "增长评分 87",
    riskLevel: "中风险",
    riskNote: "最近 7 天复购率环比下降 8%",
    flow: "客群分层 -> 文案生成 -> 页面建议 -> 复盘回流 -> 精准留存",
    stats: {
      "近 14 天访问": "32k",
      "复购转化率": "18.4%",
      "高客单占比": "41%",
      "预计 uplift": "+12%"
    },
    signals: [
      "德国与法国站的会员客群打开率保持稳定，但加购率下降。",
      "高价值用户更偏好限时权益和组合包，而非单品折扣。",
      "最近两轮活动的页面首屏加载后停留时间较长。"
    ],
    insight: {
      persona: "高价值复购客群",
      opportunity: "以会员专享组合包带动下一次复购",
      retentionRisk: "若仍使用泛促销模板，复购节奏可能继续下降",
      summary: "AI 判断这个客群不是立即流失，而是处于价值释放不足阶段。优先优化权益表达、主视觉节奏和 landing 页首屏信息密度。",
      tags: ["套装优先", "权益表达", "欧盟仓现货", "高毛利配件"]
    },
    content: {
      theme: "会员专享升级周",
      copy: "围绕高价值复购用户推出配件组合包和会员加赠权益，用更少选择成本换更高下单意愿。",
      headline: "为你的下一次升级，提前准备好完整组合",
      subhead: "针对已购主设备用户，推荐高关联配件与会员限定福利，降低决策门槛。",
      landingFocus: "首屏展示会员专属权益 + 最常一起购买的组合推荐",
      landingSummary: "页面重点突出价值密度和权益可得性，减少泛促销噪音。",
      landingSections: [
        "权益总览与倒计时",
        "组合推荐卡片",
        "用户评价与复购理由",
        "库存与履约承诺"
      ]
    },
    analysis: {
      metrics: {
        "CTR": "6.8%",
        "加购率": "22%",
        "转化率": "4.9%",
        "ROI": "2.7x"
      },
      learnings: [
        "会员权益文案比直接折扣文案带来更高点击率。",
        "组合包页面在移动端的转化优于纯商品列表页。",
        "德语站更偏好明确库存和配送承诺。"
      ],
      note: "下一轮建议把页面首屏继续压缩到一个主权益 + 两个组合推荐，减少内容分散。"
    },
    retention: {
      customers: [
        { name: "EU-1029", value: "年贡献 €1,480", risk: "7 天未复购", action: "发放会员组合券" },
        { name: "EU-2871", value: "年贡献 €1,160", risk: "近 3 次仅浏览未加购", action: "触发站内提醒" },
        { name: "EU-4420", value: "年贡献 €930", risk: "配件品类兴趣下降", action: "推送组合内容" }
      ],
      actions: [
        "对高价值复购客群发放会员限定组合券",
        "对浏览未加购用户创建 CRM 跟进任务",
        "对权益敏感客群加入复购旅程"
      ]
    },
    poc: {
      focus: "先验证会员权益表达是否能显著提升复购转化。",
      note: "试点范围限定在欧洲站已购主设备的会员客群。"
    }
  },
  {
    id: "sea-new-users",
    market: "东南亚站",
    audience: "新客首购客群",
    title: "东南亚站新客首购转化提升",
    summary: "新客流量充足，但首购转化不稳定，活动页缺少足够明确的入门理由和本地化信任信息。",
    tags: ["新客冷启", "本地化", "首购激励"],
    score: "增长评分 79",
    riskLevel: "低风险",
    riskNote: "新客活跃在上升，但转化波动较大",
    flow: "新客识别 -> 内容生成 -> 页面本地化 -> 数据复盘 -> 再营销触达",
    stats: {
      "近 14 天新客": "58k",
      "首购转化率": "2.6%",
      "跳出率": "41%",
      "预计 uplift": "+15%"
    },
    signals: [
      "泰国与印尼站的新客访问高峰集中在晚间移动端。",
      "包邮与本地退换承诺对新客停留时间影响明显。",
      "英文主视觉在本地化站点表现弱于双语版本。"
    ],
    insight: {
      persona: "移动端新客",
      opportunity: "用双语入门礼包和信任承诺拉动首购",
      retentionRisk: "若首购体验弱，新客会快速流向价格更低的平台",
      summary: "AI 判断当前机会在于强化首屏的本地化信任元素，而不是继续堆叠折扣信息。",
      tags: ["双语页面", "包邮承诺", "移动端优先", "入门礼包"]
    },
    content: {
      theme: "新客入门礼遇周",
      copy: "用更轻量的首购礼包和清晰的本地化权益，让新客更快完成第一次下单。",
      headline: "第一次购买，也能感受到被认真对待",
      subhead: "突出本地配送、包邮政策和热门入门组合，降低首次下单顾虑。",
      landingFocus: "首屏展示本地信任承诺 + 三个入门款推荐",
      landingSummary: "页面内容更偏轻量转化，强调清晰与安心。",
      landingSections: [
        "本地物流与退换承诺",
        "入门爆款推荐",
        "双语 FAQ",
        "首购礼包入口"
      ]
    },
    analysis: {
      metrics: {
        "CTR": "7.4%",
        "加购率": "16%",
        "转化率": "3.1%",
        "ROI": "2.1x"
      },
      learnings: [
        "双语页面较纯英文页面多带来 11% 的停留时长。",
        "新客更关注物流承诺而不是复杂促销机制。",
        "首购礼包在晚间移动端表现最佳。"
      ],
      note: "下一轮建议分国家进一步拆分主视觉和 FAQ 口径，减少统一模板带来的表达损耗。"
    },
    retention: {
      customers: [
        { name: "SEA-731", value: "首购潜力高", risk: "3 次访问未下单", action: "加入首购提醒" },
        { name: "SEA-128", value: "移动端高活跃", risk: "停留长但未加购", action: "发放入门礼包" },
        { name: "SEA-556", value: "浏览 FAQ 2 次", risk: "信任犹豫", action: "推送本地物流承诺" }
      ],
      actions: [
        "给犹豫新客触发首购礼包",
        "给高停留未加购用户创建再营销提醒",
        "将高意向新客加入转化旅程"
      ]
    },
    poc: {
      focus: "验证双语信任表达对首购转化的拉动效果。",
      note: "试点范围限定在泰国站和印尼站移动端新客。"
    }
  },
  {
    id: "na-at-risk",
    market: "北美站",
    audience: "流失预警客群",
    title: "北美站高风险流失客群保留",
    summary: "近期高风险客群在邮件打开和站内回访上持续走低，需要把预警、内容和 CRM 跟进整合起来做定向干预。",
    tags: ["流失预警", "CRM 跟进", "高价值保留"],
    score: "增长评分 74",
    riskLevel: "高风险",
    riskNote: "近 30 天活跃度下降 22%",
    flow: "风险识别 -> 保留内容生成 -> 干预旅程 -> 执行跟进 -> 效果复盘",
    stats: {
      "高风险用户": "4.2k",
      "邮件打开率": "14%",
      "回访率": "9.8%",
      "预计 uplift": "+9%"
    },
    signals: [
      "近 30 天高客单客群的邮件打开率持续下降。",
      "站内复访用户更愿意点击个性化保留权益而非统一折扣。",
      "CRM 团队当前缺少优先级排序清单。"
    ],
    insight: {
      persona: "高价值流失预警客群",
      opportunity: "用更精细的保留权益和优先级清单挽回高价值用户",
      retentionRisk: "若仍按统一触达节奏执行，关键用户可能在下个周期流失",
      summary: "AI 判断这一客群需要先排序再干预，优先给高价值且近期信号下滑明显的用户更强权益和人工跟进。",
      tags: ["优先级排序", "人工跟进", "个性化权益", "高价值回流"]
    },
    content: {
      theme: "高价值用户保留计划",
      copy: "以个性化权益包、限时关怀和 CRM 优先跟进，提升高价值用户的回流概率。",
      headline: "把最重要的客户，拉回到你的下一轮增长里",
      subhead: "系统优先识别高价值风险用户，输出分层权益、触达话术和跟进任务。",
      landingFocus: "以保留权益和用户价值提醒为页面主结构",
      landingSummary: "页面更偏任务式操作，便于营销和 CRM 共同使用。",
      landingSections: [
        "高风险清单与优先级",
        "保留权益建议",
        "触达话术模板",
        "跟进任务状态"
      ]
    },
    analysis: {
      metrics: {
        "CTR": "4.1%",
        "回访率": "11.4%",
        "留存率": "63%",
        "ROI": "3.0x"
      },
      learnings: [
        "高价值流失客群更需要差异化权益而不是统一满减。",
        "人工 CRM 跟进对高价值用户回流效果更强。",
        "风险排序清单能显著提升团队执行效率。"
      ],
      note: "下一轮建议把风险分层直接写入 CRM 任务看板，减少跨系统复制。"
    },
    retention: {
      customers: [
        { name: "NA-902", value: "年贡献 $2,340", risk: "28 天无回访", action: "专属权益 + 人工电话" },
        { name: "NA-411", value: "年贡献 $1,980", risk: "打开率连续下降", action: "重启旅程 + 页面提醒" },
        { name: "NA-220", value: "年贡献 $1,540", risk: "高频浏览但无复购", action: "推送个性化礼包" }
      ],
      actions: [
        "为高价值用户生成专属权益方案",
        "为 CRM 团队创建优先级跟进任务",
        "将高风险用户加入保留旅程并标记回访状态"
      ]
    },
    poc: {
      focus: "验证风险排序 + 个性化权益 + CRM 跟进的组合效果。",
      note: "试点范围限定在北美站高价值流失预警客群。"
    }
  }
];

const topKpis = [
  { value: "40%", label: "活动准备周期目标缩短" },
  { value: "50%", label: "内容与页面生产效率提升" },
  { value: "60%", label: "复盘出具时间目标缩短" },
  { value: "80%", label: "高风险识别准确率目标" }
];

const state = {
  selectedSegmentId: segments[0].id,
  marketFilter: "全部",
  activeScreen: "insight",
  executionLogs: {
    [segments[0].id]: ["AI 已完成客群洞察与活动切入点识别"],
    [segments[1].id]: ["AI 已生成首购礼包与本地化页面方向"],
    [segments[2].id]: ["AI 已生成高风险用户优先级与保留任务草案"]
  }
};

const elements = {
  kpiStrip: document.getElementById("kpi-strip"),
  marketFilterRow: document.getElementById("market-filter-row"),
  segmentList: document.getElementById("segment-list"),
  recommendedActions: document.getElementById("recommended-actions"),
  pocFocus: document.getElementById("poc-focus"),
  pocNote: document.getElementById("poc-note"),
  heroFlow: document.getElementById("hero-flow"),
  heroBrief: document.getElementById("hero-brief"),
  workspaceTitle: document.getElementById("workspace-title"),
  workspaceSubtitle: document.getElementById("workspace-subtitle"),
  riskLevel: document.getElementById("risk-level"),
  riskNote: document.getElementById("risk-note"),
  segmentScore: document.getElementById("segment-score"),
  signalCount: document.getElementById("signal-count"),
  signalList: document.getElementById("signal-list"),
  personaBadge: document.getElementById("persona-badge"),
  growthOpportunity: document.getElementById("growth-opportunity"),
  retentionRisk: document.getElementById("retention-risk"),
  insightSummary: document.getElementById("insight-summary"),
  insightTags: document.getElementById("insight-tags"),
  insightStats: document.getElementById("insight-stats"),
  campaignTheme: document.getElementById("campaign-theme"),
  campaignCopy: document.getElementById("campaign-copy"),
  headlineCopy: document.getElementById("headline-copy"),
  subheadCopy: document.getElementById("subhead-copy"),
  landingFocus: document.getElementById("landing-focus"),
  landingSummary: document.getElementById("landing-summary"),
  landingSections: document.getElementById("landing-sections"),
  analysisMetrics: document.getElementById("analysis-metrics"),
  analysisLearnings: document.getElementById("analysis-learnings"),
  optimizationNote: document.getElementById("optimization-note"),
  retentionCount: document.getElementById("retention-count"),
  retentionList: document.getElementById("retention-list"),
  executionStatus: document.getElementById("execution-status"),
  executionList: document.getElementById("execution-list"),
  nextSegmentButton: document.getElementById("next-segment-button"),
  triggerRunButton: document.getElementById("trigger-run-button")
};

function getCurrentSegment() {
  return segments.find((segment) => segment.id === state.selectedSegmentId) ?? segments[0];
}

function getVisibleSegments() {
  return segments.filter((segment) => state.marketFilter === "全部" || segment.market === state.marketFilter);
}

function renderKpis() {
  elements.kpiStrip.innerHTML = topKpis
    .map(
      (item) => `
        <article class="kpi-card">
          <strong>${item.value}</strong>
          <p>${item.label}</p>
        </article>`
    )
    .join("");
}

function renderFilters() {
  const filters = ["全部", ...new Set(segments.map((segment) => segment.market))];
  elements.marketFilterRow.innerHTML = filters
    .map(
      (filter) => `
        <button class="chip-button ${state.marketFilter === filter ? "is-active" : ""}" data-filter="${filter}" type="button">
          ${filter}
        </button>`
    )
    .join("");
}

function renderSegmentList() {
  const visibleSegments = getVisibleSegments();

  elements.segmentList.innerHTML = visibleSegments
    .map(
      (segment) => `
        <article class="segment-card ${segment.id === state.selectedSegmentId ? "is-active" : ""}" data-segment-id="${segment.id}">
          <h3>${segment.audience}</h3>
          <p>${segment.summary}</p>
          <div class="segment-meta">
            <span>${segment.market}</span>
            <span>${segment.riskLevel}</span>
          </div>
          <div class="case-chip-row">
            ${segment.tags.map((tag) => `<span class="case-chip">${tag}</span>`).join("")}
          </div>
        </article>`
    )
    .join("");
}

function renderInsight(segment) {
  elements.segmentScore.textContent = segment.score;
  elements.signalCount.textContent = `${segment.signals.length} 条样例信号`;
  elements.signalList.innerHTML = segment.signals.map((item) => `<li>${item}</li>`).join("");
  elements.personaBadge.textContent = segment.insight.persona;
  elements.growthOpportunity.textContent = segment.insight.opportunity;
  elements.retentionRisk.textContent = segment.insight.retentionRisk;
  elements.insightSummary.textContent = segment.insight.summary;
  elements.insightTags.innerHTML = segment.insight.tags.map((tag) => `<span>${tag}</span>`).join("");
  elements.insightStats.innerHTML = Object.entries(segment.stats)
    .map(
      ([label, value]) => `
        <article class="stat-card">
          <p class="mini-label">${label}</p>
          <strong>${value}</strong>
        </article>`
    )
    .join("");
}

function renderContent(segment) {
  elements.campaignTheme.textContent = segment.content.theme;
  elements.campaignCopy.textContent = segment.content.copy;
  elements.headlineCopy.textContent = segment.content.headline;
  elements.subheadCopy.textContent = segment.content.subhead;
  elements.landingFocus.textContent = segment.content.landingFocus;
  elements.landingSummary.textContent = segment.content.landingSummary;
  elements.landingSections.innerHTML = segment.content.landingSections
    .map(
      (section) => `
        <article class="preview-section">
          <span>模块建议</span>
          <strong>${section}</strong>
        </article>`
    )
    .join("");
}

function renderAnalysis(segment) {
  elements.analysisMetrics.innerHTML = Object.entries(segment.analysis.metrics)
    .map(
      ([label, value]) => `
        <article class="metric-card">
          <p class="mini-label">${label}</p>
          <strong>${value}</strong>
        </article>`
    )
    .join("");
  elements.analysisLearnings.innerHTML = segment.analysis.learnings.map((item) => `<li>${item}</li>`).join("");
  elements.optimizationNote.textContent = segment.analysis.note;
}

function renderRetention(segment) {
  elements.retentionCount.textContent = `${segment.retention.customers.length} 位高风险样例`;
  elements.retentionList.innerHTML = segment.retention.customers
    .map(
      (customer) => `
        <article class="customer-card">
          <strong>${customer.name}</strong>
          <div class="customer-meta">
            <span>${customer.value}</span>
            <span>${customer.risk}</span>
          </div>
          <p>推荐动作：${customer.action}</p>
        </article>`
    )
    .join("");
  elements.recommendedActions.innerHTML = segment.retention.actions.map((item) => `<li>${item}</li>`).join("");
}

function renderExecution(segment) {
  const logs = state.executionLogs[segment.id] ?? [];
  elements.executionStatus.textContent = logs[logs.length - 1] ?? "等待动作触发";
  elements.executionList.innerHTML = logs.map((item) => `<li>${item}</li>`).join("");
}

function renderWorkspace() {
  const segment = getCurrentSegment();

  elements.heroFlow.textContent = segment.flow;
  elements.heroBrief.textContent = `${segment.market} / ${segment.audience} / 当前默认从“客户洞察”开始讲解，再过渡到内容生成、复盘和保留动作。`;
  elements.workspaceTitle.textContent = segment.title;
  elements.workspaceSubtitle.textContent = `${segment.market} / ${segment.audience} / ${segment.summary}`;
  elements.riskLevel.textContent = segment.riskLevel;
  elements.riskNote.textContent = segment.riskNote;
  elements.pocFocus.textContent = segment.poc.focus;
  elements.pocNote.textContent = segment.poc.note;

  renderInsight(segment);
  renderContent(segment);
  renderAnalysis(segment);
  renderRetention(segment);
  renderExecution(segment);
}

function renderActiveScreen() {
  document.querySelectorAll(".screen-button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.screen === state.activeScreen);
  });

  document.querySelectorAll("[data-screen-panel]").forEach((panel) => {
    panel.classList.toggle("is-active", panel.dataset.screenPanel === state.activeScreen);
  });
}

function rerender() {
  renderFilters();
  renderSegmentList();
  renderWorkspace();
  renderActiveScreen();
}

function appendExecutionLog(message) {
  const segment = getCurrentSegment();
  const logs = state.executionLogs[segment.id] ?? [];
  logs.push(message);
  state.executionLogs[segment.id] = logs.slice(-5);
  renderExecution(segment);
}

document.addEventListener("click", (event) => {
  const filterButton = event.target.closest("[data-filter]");
  if (filterButton) {
    state.marketFilter = filterButton.dataset.filter;
    const visibleSegments = getVisibleSegments();
    if (!visibleSegments.some((segment) => segment.id === state.selectedSegmentId)) {
      state.selectedSegmentId = visibleSegments[0]?.id ?? segments[0].id;
    }
    rerender();
    return;
  }

  const segmentCard = event.target.closest("[data-segment-id]");
  if (segmentCard) {
    state.selectedSegmentId = segmentCard.dataset.segmentId;
    state.activeScreen = "insight";
    rerender();
    return;
  }

  const screenButton = event.target.closest("[data-screen]");
  if (screenButton) {
    state.activeScreen = screenButton.dataset.screen;
    renderActiveScreen();
    return;
  }

  const actionButton = event.target.closest("[data-action]");
  if (actionButton) {
    const actionMap = {
      "trigger-offer": "已生成专属权益包并发送给目标客群",
      "create-task": "已创建 CRM 跟进任务并写入优先级排序",
      "launch-journey": "已将目标客群加入保留旅程并记录回访节点"
    };
    appendExecutionLog(actionMap[actionButton.dataset.action]);
  }
});

elements.nextSegmentButton.addEventListener("click", () => {
  const visibleSegments = getVisibleSegments();
  const currentIndex = visibleSegments.findIndex((segment) => segment.id === state.selectedSegmentId);
  const nextSegment = visibleSegments[(currentIndex + 1) % visibleSegments.length] ?? segments[0];
  state.selectedSegmentId = nextSegment.id;
  state.activeScreen = "insight";
  rerender();
});

elements.triggerRunButton.addEventListener("click", () => {
  const runMessages = {
    insight: "AI 已刷新客群洞察与增长机会判断",
    content: "AI 已生成新一版活动文案、页面和素材建议",
    analysis: "AI 已输出最新活动复盘和下一轮优化建议",
    retention: "AI 已刷新高风险清单并生成干预动作"
  };

  appendExecutionLog(runMessages[state.activeScreen]);
});

renderKpis();
rerender();