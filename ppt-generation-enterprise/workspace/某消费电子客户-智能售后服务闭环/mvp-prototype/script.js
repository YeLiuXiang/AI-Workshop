const cases = [
  {
    id: "case-001",
    title: "空调控制器离线且频繁报修",
    customer: "华东核心经销商 / VIP 客户",
    channel: "电话报修",
    priority: "P1",
    priorityLabel: "高优先级",
    status: "设备离线 17 分钟",
    statusLevel: "critical",
    tags: ["联网异常", "高频工单", "保内设备"],
    metrics: {
      "设备在线率": "62%",
      "近 7 天报修": "4 次",
      "知识命中率": "91%",
      "建议首响": "3 分钟内"
    },
    history: [
      "08:42 App 上报 E102 通信中断，设备自动重连失败。",
      "08:47 客户电话报修，反馈设备黑屏且无法远程控制。",
      "08:51 上周同型号曾出现网关固件不兼容问题。"
    ],
    diagnosis: {
      confidence: "置信度 92%",
      type: "网关通信异常",
      rootCause: "固件版本与网关协议不兼容",
      summary: "AI 综合设备遥测、同型号历史工单与 FAQ，判断当前问题更可能由网关固件版本冲突引起，而非硬件损坏。"
    },
    knowledge: [
      "FAQ #17: E102 伴随黑屏时优先检查网关协议版本。",
      "案例 #A-224: 同型号在 4.2.1 固件下与旧网关存在兼容性缺陷。",
      "处理手册: 先远程刷新网关握手，再决定是否安排现场服务。"
    ],
    reply:
      "您好，系统已识别到设备当前存在通信异常。建议先保持设备通电，我们将优先执行一次远程网关握手刷新；如 10 分钟内未恢复，将自动升级二线支持并安排进一步处理。",
    suggestedActions: [
      "自动下发网关握手刷新指令",
      "若 10 分钟内未恢复，升级二线工单",
      "同步提示客服优先安抚客户并确认现场网络状态"
    ],
    closure: {
      title: "新增知识条目：网关 4.2.1 固件兼容性排查模板",
      summary: "本次处理完成后可沉淀为‘E102 通信异常’的标准诊断剧本，后续同类问题优先自动召回。",
      points: [
        "记录兼容性受影响的设备型号与网关版本",
        "保存远程刷新是否成功的结果字段",
        "补充客服标准回复模板与升级阈值"
      ]
    }
  },
  {
    id: "case-002",
    title: "扫地机电池衰减导致续航骤降",
    customer: "直营电商渠道用户",
    channel: "在线客服",
    priority: "P2",
    priorityLabel: "中优先级",
    status: "续航低于阈值",
    statusLevel: "warning",
    tags: ["电池健康", "可自助排查", "质保边界"],
    metrics: {
      "设备在线率": "99%",
      "近 7 天报修": "1 次",
      "知识命中率": "87%",
      "建议首响": "5 分钟内"
    },
    history: [
      "昨日续航从 86 分钟降至 41 分钟。",
      "最近两周已累计完成 91 次深度充放电。",
      "历史工单显示该批次电池在高温环境下衰减更快。"
    ],
    diagnosis: {
      confidence: "置信度 84%",
      type: "电池健康衰减",
      rootCause: "高温使用环境叠加充放电周期过密",
      summary: "AI 判断该案例属于典型的电池健康衰减问题，可先引导用户执行自助校准与健康检测，再决定是否进入换新流程。"
    },
    knowledge: [
      "FAQ #38: 续航骤降优先触发电池校准向导。",
      "案例 #B-118: 高温环境用户需提示清洁与冷却等待。",
      "服务政策: 满足质保阈值时可自动推荐换新方案。"
    ],
    reply:
      "您好，系统判断设备当前更像是电池健康衰减。建议先按页面指引完成一次电池校准和健康检测，我们会根据结果判断是否进入换新流程。",
    suggestedActions: [
      "推送电池校准步骤给用户",
      "生成健康检测结果回收任务",
      "若检测低于阈值，自动触发换新审核"
    ],
    closure: {
      title: "新增知识条目：续航骤降自助排查脚本",
      summary: "沉淀用户环境、充放电次数与检测结果的组合条件，提升自助解决比例。",
      points: [
        "标记高温使用场景作为高风险特征",
        "记录健康检测数值与是否进入换新",
        "补充用户教育类 FAQ 入口"
      ]
    }
  },
  {
    id: "case-003",
    title: "净水设备滤芯误报需要更换",
    customer: "华南服务商批量报修",
    channel: "服务商门户",
    priority: "P3",
    priorityLabel: "标准优先级",
    status: "规则告警待复核",
    statusLevel: "normal",
    tags: ["规则误报", "批量设备", "知识补全"],
    metrics: {
      "设备在线率": "96%",
      "近 7 天报修": "12 台",
      "知识命中率": "76%",
      "建议首响": "10 分钟内"
    },
    history: [
      "近三天同批次设备集中出现滤芯更换提醒。",
      "现场检测显示实际水质与滤芯寿命均在正常区间。",
      "上一次规则更新后，阈值修正记录缺失。"
    ],
    diagnosis: {
      confidence: "置信度 79%",
      type: "规则阈值误触发",
      rootCause: "寿命估算阈值更新不完整",
      summary: "AI 更倾向这是批量规则误报，而不是滤芯真实失效，建议转交运营支持核查阈值配置并暂缓换件。"
    },
    knowledge: [
      "FAQ #52: 滤芯提醒需先核对寿命估算阈值版本。",
      "案例 #C-022: 批量误报通常与规则更新不同步相关。",
      "操作手册: 服务商批量场景应优先升级配置排查工单。"
    ],
    reply:
      "您好，系统判断当前更可能是阈值配置导致的批量误报，建议暂缓直接更换滤芯，我们会先升级配置核查工单并给出统一处理结论。",
    suggestedActions: [
      "创建配置核查工单",
      "同步批量设备清单给运营支持",
      "暂停自动发送换芯通知"
    ],
    closure: {
      title: "新增知识条目：批量规则误报升级模板",
      summary: "形成面向服务商的批量误报排查模板，减少一线客服重复判断。",
      points: [
        "沉淀阈值版本比对字段",
        "记录是否属于批量误报的判定规则",
        "补充服务商统一通知模板"
      ]
    }
  }
];

const kpiCards = [
  { value: "30%", label: "预计首响时间下降" },
  { value: "40%", label: "预计问题定位时间下降" },
  { value: "20%", label: "复杂升级率目标下降" },
  { value: "1 个", label: "统一工作台完成主要操作" }
];

const state = {
  selectedCaseId: cases[0].id,
  filter: "全部",
  activeTab: "knowledge",
  executionLogs: {
    [cases[0].id]: ["AI 已完成设备状态、工单与 FAQ 联合分析"],
    [cases[1].id]: ["AI 已生成电池健康检测建议"],
    [cases[2].id]: ["AI 已识别批量规则误报趋势"],
  },
};

const elements = {
  kpiStrip: document.getElementById("kpi-strip"),
  filterRow: document.getElementById("filter-row"),
  caseList: document.getElementById("case-list"),
  workspaceTitle: document.getElementById("workspace-title"),
  priorityValue: document.getElementById("priority-value"),
  deviceName: document.getElementById("device-name"),
  deviceMeta: document.getElementById("device-meta"),
  deviceStatus: document.getElementById("device-status"),
  deviceStats: document.getElementById("device-stats"),
  historyCount: document.getElementById("history-count"),
  historyTimeline: document.getElementById("history-timeline"),
  diagnosisConfidence: document.getElementById("diagnosis-confidence"),
  diagnosisType: document.getElementById("diagnosis-type"),
  diagnosisRootCause: document.getElementById("diagnosis-root-cause"),
  diagnosisSummary: document.getElementById("diagnosis-summary"),
  tabContent: document.getElementById("tab-content"),
  replyPreview: document.getElementById("reply-preview"),
  executionStatus: document.getElementById("execution-status"),
  executionList: document.getElementById("execution-list"),
  closureTitle: document.getElementById("closure-title"),
  closureSummary: document.getElementById("closure-summary"),
  closurePoints: document.getElementById("closure-points"),
  nextCaseButton: document.getElementById("next-case-button"),
};

function getCurrentCase() {
  return cases.find((item) => item.id === state.selectedCaseId) ?? cases[0];
}

function renderKpis() {
  elements.kpiStrip.innerHTML = kpiCards
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
  const filters = ["全部", "P1", "P2", "P3"];
  elements.filterRow.innerHTML = filters
    .map(
      (filter) => `
        <button class="chip-button ${state.filter === filter ? "is-active" : ""}" data-filter="${filter}" type="button">
          ${filter}
        </button>`
    )
    .join("");
}

function renderCaseList() {
  const visibleCases = cases.filter((item) => state.filter === "全部" || item.priority === state.filter);

  elements.caseList.innerHTML = visibleCases
    .map(
      (item) => `
        <article class="case-item ${item.id === state.selectedCaseId ? "is-selected" : ""}" data-case-id="${item.id}">
          <h3>${item.title}</h3>
          <p>${item.customer}</p>
          <div class="case-meta">
            <span>${item.channel}</span>
            <span>${item.priorityLabel}</span>
          </div>
          <div class="case-tags">
            ${item.tags.map((tag) => `<span>${tag}</span>`).join("")}
          </div>
        </article>`
    )
    .join("");
}

function renderStats(caseData) {
  elements.deviceStats.innerHTML = Object.entries(caseData.metrics)
    .map(
      ([label, value]) => `
        <div class="stat-card">
          <p class="mini-label">${label}</p>
          <strong>${value}</strong>
        </div>`
    )
    .join("");
}

function renderHistory(caseData) {
  elements.historyCount.textContent = `${caseData.history.length} 条轨迹`;
  elements.historyTimeline.innerHTML = caseData.history.map((item) => `<li>${item}</li>`).join("");
}

function renderTab(caseData) {
  if (state.activeTab === "knowledge") {
    elements.tabContent.innerHTML = `<ul class="bullet-list">${caseData.knowledge.map((item) => `<li>${item}</li>`).join("")}</ul>`;
    return;
  }

  if (state.activeTab === "reply") {
    elements.tabContent.innerHTML = `<p>${caseData.reply}</p>`;
    return;
  }

  elements.tabContent.innerHTML = `<ul class="bullet-list">${caseData.suggestedActions.map((item) => `<li>${item}</li>`).join("")}</ul>`;
}

function renderExecution(caseData) {
  const logs = state.executionLogs[caseData.id] ?? [];
  elements.executionStatus.textContent = logs[logs.length - 1] ?? "等待动作触发";
  elements.executionList.innerHTML = logs.map((item) => `<li>${item}</li>`).join("");
}

function renderClosure(caseData) {
  elements.closureTitle.textContent = caseData.closure.title;
  elements.closureSummary.textContent = caseData.closure.summary;
  elements.closurePoints.innerHTML = caseData.closure.points.map((item) => `<li>${item}</li>`).join("");
}

function renderWorkspace() {
  const caseData = getCurrentCase();

  elements.workspaceTitle.textContent = caseData.title;
  elements.priorityValue.textContent = caseData.priority;
  elements.deviceName.textContent = caseData.title;
  elements.deviceMeta.textContent = `${caseData.customer} | ${caseData.channel}`;
  elements.deviceStatus.textContent = caseData.status;
  elements.deviceStatus.className = `status-pill ${
    caseData.statusLevel === "critical"
      ? "is-critical"
      : caseData.statusLevel === "warning"
        ? "is-warning"
        : ""
  }`;
  elements.diagnosisConfidence.textContent = caseData.diagnosis.confidence;
  elements.diagnosisType.textContent = caseData.diagnosis.type;
  elements.diagnosisRootCause.textContent = caseData.diagnosis.rootCause;
  elements.diagnosisSummary.textContent = caseData.diagnosis.summary;
  elements.replyPreview.textContent = caseData.reply;

  renderStats(caseData);
  renderHistory(caseData);
  renderTab(caseData);
  renderExecution(caseData);
  renderClosure(caseData);
}

function renderTabs() {
  document.querySelectorAll(".tab-button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.tab === state.activeTab);
  });
}

function rerender() {
  renderFilters();
  renderCaseList();
  renderWorkspace();
  renderTabs();
}

function appendExecutionLog(message) {
  const caseData = getCurrentCase();
  const logs = state.executionLogs[caseData.id] ?? [];
  logs.push(message);
  state.executionLogs[caseData.id] = logs.slice(-4);
  renderExecution(caseData);
}

document.addEventListener("click", (event) => {
  const filterButton = event.target.closest("[data-filter]");
  if (filterButton) {
    state.filter = filterButton.dataset.filter;
    const visibleCases = cases.filter((item) => state.filter === "全部" || item.priority === state.filter);
    if (!visibleCases.some((item) => item.id === state.selectedCaseId)) {
      state.selectedCaseId = visibleCases[0]?.id ?? cases[0].id;
    }
    rerender();
    return;
  }

  const caseCard = event.target.closest("[data-case-id]");
  if (caseCard) {
    state.selectedCaseId = caseCard.dataset.caseId;
    rerender();
    return;
  }

  const tabButton = event.target.closest("[data-tab]");
  if (tabButton) {
    state.activeTab = tabButton.dataset.tab;
    renderTabs();
    renderTab(getCurrentCase());
    return;
  }

  const actionButton = event.target.closest("[data-action]");
  if (actionButton) {
    const actionMap = {
      "send-reply": "已生成客服回复并进入待发送状态",
      escalate: "已升级二线工单并附带 AI 诊断摘要",
      "create-task": "已创建上门排障任务并回填服务编排队列",
    };

    appendExecutionLog(actionMap[actionButton.dataset.action]);
  }
});

elements.nextCaseButton.addEventListener("click", () => {
  const index = cases.findIndex((item) => item.id === state.selectedCaseId);
  const nextCase = cases[(index + 1) % cases.length];
  state.selectedCaseId = nextCase.id;
  rerender();
});

renderKpis();
rerender();