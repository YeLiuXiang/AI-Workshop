const prototypeData = JSON.parse(document.getElementById("prototype-data").textContent);

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
