const state = {
  pollTimer: null,
  currentJobId: null,
  defaultMode: "codex-cli",
  prototypeStatus: "not_requested",
  sampleIndex: 0,
};

const timelineSteps = [
  { key: "queued", label: "请求队列", hint: "等待开始" },
  { key: "codex-normalization", label: "场景整理", hint: "理解图片与业务描述" },
  { key: "artifact-generation", label: "方案与 PPT 生成", hint: "生成内容与演示文稿" },
  { key: "completed", label: "结果完成", hint: "可下载并访问结果" }
];

const samplePayloads = [
  {
    scene_name: "会员增长与保留运营工作台",
    industry: "跨境电商",
    scenario_summary: "围绕会员生命周期运营，构建从客户洞察、个性化内容生成、活动落地到复盘分析与流失预警的一体化 AI 增长闭环。",
    target_role: "会员运营负责人",
    current_pain_point: "会员分层、营销内容生产、活动落地和流失预警分散在多个系统与团队中，响应慢且协同成本高。",
    expected_value: "希望先做出一版可演示的会员增长工作台，快速验证客户洞察、内容生成和保留动作联动的价值。"
  },
  {
    scene_name: "售后服务诊断与派工工作台",
    industry: "消费电子 IoT",
    scenario_summary: "围绕设备售后服务场景，连接工单、故障描述、历史处理记录和备件信息，帮助一线人员更快完成诊断与派工。",
    target_role: "售后运营经理",
    current_pain_point: "客服和工程师需要在多个系统里查设备状态、维修记录和知识库，诊断效率低且经验依赖强。",
    expected_value: "先做出一版售后服务工作台，验证问题识别、维修建议和派工协同的效率提升。"
  },
  {
    scene_name: "门店促销活动复盘助手",
    industry: "零售连锁",
    scenario_summary: "围绕门店促销活动复盘，整合销售、客流、商品和区域反馈信息，快速定位效果差异和下一轮优化方向。",
    target_role: "零售运营负责人",
    current_pain_point: "活动结束后复盘周期长，门店反馈和销售数据分散，难以及时提炼出可复制的促销打法。",
    expected_value: "先生成一版促销复盘方案，帮助业务快速看清活动效果并沉淀下一轮动作建议。"
  },
  {
    scene_name: "企业知识问答与培训助手",
    industry: "专业服务",
    scenario_summary: "围绕内部知识沉淀与培训场景，连接制度文档、项目案例和常见问答，帮助员工快速获取答案和培训内容。",
    target_role: "培训与知识管理负责人",
    current_pain_point: "知识分散在文档、群聊和个人经验中，新员工培训周期长，重复性答疑占用大量专家时间。",
    expected_value: "先生成一版知识问答与培训方案，验证统一入口、问答推荐和培训内容整理的价值。"
  },
  {
    scene_name: "跨团队项目风险预警看板",
    industry: "企业软件",
    scenario_summary: "围绕跨团队项目推进场景，汇总需求变更、排期、缺陷和协作阻塞信息，提前识别高风险项目并给出跟进建议。",
    target_role: "PMO 负责人",
    current_pain_point: "项目风险往往在周会前才暴露，信息来自多个系统和群组，人工汇总成本高且预警滞后。",
    expected_value: "先落一版项目风险预警看板，用于展示风险识别、影响分析和推进建议的闭环。"
  }
];

const elements = {
  form: document.getElementById("job-form"),
  loadSampleButton: document.getElementById("load-sample-button"),
  resetButton: document.getElementById("reset-button"),
  fileInput: document.getElementById("files"),
  dropzone: document.getElementById("dropzone"),
  fileList: document.getElementById("file-list"),
  statusBadge: document.getElementById("status-badge"),
  stageLabel: document.getElementById("stage-label"),
  jobIdText: document.getElementById("job-id-text"),
  errorCard: document.getElementById("error-card"),
  timeline: document.getElementById("timeline"),
  pptState: document.getElementById("ppt-state"),
  pptActions: document.getElementById("ppt-actions"),
  prototypeState: document.getElementById("prototype-state"),
  prototypeActions: document.getElementById("prototype-actions"),
  prototypeGenerateButton: document.getElementById("prototype-generate-button")
};

async function loadMeta() {
  const response = await fetch("/api/meta");
  if (!response.ok) {
    return;
  }
  const payload = await response.json();
  if (payload.default_mode) {
    state.defaultMode = payload.default_mode;
  }
}

function loadSample() {
  const samplePayload = samplePayloads[state.sampleIndex];
  Object.entries(samplePayload).forEach(([key, value]) => {
    const field = document.getElementById(key);
    if (field) {
      field.value = value;
    }
  });
  state.sampleIndex = (state.sampleIndex + 1) % samplePayloads.length;
}

function resetArtifacts() {
  elements.pptState.textContent = "等待生成";
  elements.prototypeState.textContent = "等待生成";
  elements.pptActions.innerHTML = "";
  elements.prototypeActions.innerHTML = "";
  elements.prototypeGenerateButton.disabled = true;
}

function setStatusBadge(status, stageLabel) {
  const statusText = {
    queued: "准备中",
    running: "生成中",
    succeeded: "已完成",
    failed: "生成失败",
  };
  elements.statusBadge.textContent = statusText[status] || "未开始";
  elements.statusBadge.className = "badge";
  if (status === "running" || status === "queued") {
    elements.statusBadge.classList.add("is-running");
  } else if (status === "succeeded") {
    elements.statusBadge.classList.add("is-success");
  } else if (status === "failed") {
    elements.statusBadge.classList.add("is-failed");
  }
  elements.stageLabel.textContent = stageLabel || "等待提交";
}

function renderTimeline(stage, status) {
  const stageOrder = timelineSteps.map((item) => item.key);
  const activeIndex = stageOrder.indexOf(stage);
  elements.timeline.innerHTML = timelineSteps.map((item, index) => {
    let stateClass = "is-pending";
    let marker = "等待";
    if (status === "failed" && (activeIndex === -1 || index >= Math.max(activeIndex, 0))) {
      stateClass = index === Math.max(activeIndex, 0) ? "is-failed" : "is-pending";
      marker = index === Math.max(activeIndex, 0) ? "失败" : "等待";
    } else if (activeIndex === -1 && status === "succeeded" && item.key === "completed") {
      stateClass = "is-done";
      marker = "完成";
    } else if (activeIndex > index) {
      stateClass = "is-done";
      marker = "完成";
    } else if (activeIndex === index) {
      stateClass = status === "succeeded" && item.key === "completed" ? "is-done" : "is-active";
      marker = stateClass === "is-done" ? "完成" : "进行中";
    }

    return `
      <article class="timeline-item ${stateClass}">
        <div class="timeline-dot"></div>
        <div class="timeline-copy">
          <strong>${item.label}</strong>
          <span>${item.hint}</span>
        </div>
        <em>${marker}</em>
      </article>
    `;
  }).join("");
}

function showError(message) {
  if (!message) {
    elements.errorCard.classList.add("is-hidden");
    elements.errorCard.textContent = "";
    return;
  }
  elements.errorCard.classList.remove("is-hidden");
  elements.errorCard.textContent = message;
}

function actionLink(href, label, extra = "") {
  return `<a class="artifact-link" href="${href}" target="_blank" rel="noopener" ${extra}>${label}</a>`;
}

function artifactUrl(jobId, artifactName, download = false) {
  return `/api/jobs/${jobId}/artifacts/${artifactName}${download ? "?download=1" : ""}`;
}

function openPptUrl(jobId, artifactName) {
  const rawUrl = `${window.location.origin}${artifactUrl(jobId, artifactName, false)}`;
  if (window.navigator.userAgent.includes("Windows")) {
    return `ms-powerpoint:ofe|u|${rawUrl}`;
  }
  return artifactUrl(jobId, artifactName, false);
}

function renderOutputs(jobId, artifacts, stage, status) {
  const pptArtifact = artifacts.find((artifact) => artifact.name.endsWith(".pptx"));
  const prototypeArtifact = artifacts.find((artifact) => artifact.name.endsWith("mvp-prototype/index.html"));
  const prototypeStatus = state.prototypeStatus || "not_requested";

  if (pptArtifact) {
    const openHref = openPptUrl(jobId, pptArtifact.name);
    const downloadHref = artifactUrl(jobId, pptArtifact.name, true);
    elements.pptState.textContent = "已完成";
    elements.pptActions.innerHTML = [
      actionLink(openHref, "打开 PPT"),
      actionLink(downloadHref, "下载 PPT", "download")
    ].join("");
  } else if (stage === "artifact-generation" || stage === "prototype-generation") {
    elements.pptState.textContent = "生成中";
    elements.pptActions.innerHTML = "";
  } else {
    elements.pptState.textContent = status === "failed" ? "生成失败" : "等待生成";
    elements.pptActions.innerHTML = "";
  }

  if (prototypeArtifact) {
    const href = artifactUrl(jobId, prototypeArtifact.name, false);
    elements.prototypeState.textContent = "已完成";
    elements.prototypeActions.innerHTML = actionLink(href, "打开原型");
    elements.prototypeGenerateButton.disabled = true;
  } else if (prototypeStatus === "queued" || prototypeStatus === "running") {
    elements.prototypeState.textContent = "生成中";
    elements.prototypeActions.innerHTML = "";
    elements.prototypeGenerateButton.disabled = true;
  } else if (prototypeStatus === "failed") {
    elements.prototypeState.textContent = "生成失败";
    elements.prototypeActions.innerHTML = "";
    elements.prototypeGenerateButton.disabled = false;
  } else {
    elements.prototypeState.textContent = pptArtifact ? "可单独生成" : "等待生成";
    elements.prototypeActions.innerHTML = "";
    elements.prototypeGenerateButton.disabled = !pptArtifact;
  }
}

function renderSelectedFiles(files) {
  if (!files.length) {
    elements.fileList.innerHTML = "";
    return;
  }
  elements.fileList.innerHTML = files.map((file) => `
    <span class="file-chip">${file.name}</span>
  `).join("");
}

function setFiles(fileList) {
  elements.fileInput.files = fileList;
  renderSelectedFiles(Array.from(fileList));
}

function buildRequestPayload() {
  const groupName = document.getElementById("group_name").value.trim();
  const sceneName = document.getElementById("scene_name").value.trim();
  const industry = document.getElementById("industry").value.trim();
  const targetRole = document.getElementById("target_role").value.trim();
  const expectedValue = document.getElementById("expected_value").value.trim();

  return {
    workshop: {
      title: "AI Discovery Card Workshop",
      customer: sceneName,
      group_name: groupName,
      industry,
    },
    event_input: {
      scene_name: sceneName,
      customer_type: industry,
      scenario_summary: document.getElementById("scenario_summary").value.trim(),
      target_role: targetRole,
      current_pain_point: document.getElementById("current_pain_point").value.trim(),
      expected_value: expectedValue,
    },
    mvp_spec: {
      prototype_mode: "前端壳子优先",
      primary_user: targetRole,
      core_task: expectedValue,
      screens: [],
      modules: [],
      key_actions: [],
      sample_data: [],
      style_keywords: ["企业级", "卡片式布局"],
      out_of_scope: []
    },
    current_process: [],
    detected_cards: {},
    recognized_cards: [],
    card_photo_paths: [],
    product_mapping: [],
    options: {
      mode: state.defaultMode,
      timeout_seconds: 900
    }
  };
}

async function submitJob(event) {
  event.preventDefault();
  showError("");
  resetArtifacts();
  renderTimeline("", "");
  setStatusBadge("queued", "正在提交任务");
  elements.jobIdText.textContent = "任务编号：提交中...";

  const payload = buildRequestPayload();
  const formData = new FormData();
  formData.append("payload_json", JSON.stringify(payload));

  for (const file of elements.fileInput.files) {
    formData.append("files", file);
  }

  const response = await fetch("/api/jobs/form", {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    const text = await response.text();
    setStatusBadge("failed", "提交失败");
    showError(text);
    return;
  }

  const result = await response.json();
  state.currentJobId = result.job_id;
  elements.jobIdText.textContent = `任务编号：${result.job_id}`;
  pollJob(result.job_id, true);
}

async function pollJob(jobId, immediate = false) {
  if (state.pollTimer) {
    clearTimeout(state.pollTimer);
    state.pollTimer = null;
  }

  if (!immediate) {
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }

  const response = await fetch(`/api/jobs/${jobId}`);
  if (!response.ok) {
    showError("无法读取任务状态。");
    return;
  }

  const job = await response.json();
  state.prototypeStatus = job.prototype_status || "not_requested";
  setStatusBadge(job.status, job.stage_label);
  renderTimeline(job.stage, job.status);
  elements.jobIdText.textContent = `任务编号：${job.job_id}`;

  if (job.error) {
    showError(job.error);
  } else if (job.prototype_error) {
    showError(job.prototype_error);
  } else {
    showError("");
  }

  renderOutputs(job.job_id, Array.isArray(job.artifacts) ? job.artifacts : [], job.stage, job.status);

  if (job.status === "queued" || job.status === "running") {
    state.pollTimer = setTimeout(() => pollJob(jobId, true), 2500);
  } else if (job.prototype_status === "queued" || job.prototype_status === "running") {
    state.pollTimer = setTimeout(() => pollJob(jobId, true), 2500);
  }
}

async function generatePrototype() {
  if (!state.currentJobId) {
    return;
  }
  elements.prototypeGenerateButton.disabled = true;
  elements.prototypeState.textContent = "提交中";
  showError("");
  const response = await fetch(`/api/jobs/${state.currentJobId}/prototype`, {
    method: "POST"
  });
  if (!response.ok) {
    const text = await response.text();
    elements.prototypeGenerateButton.disabled = false;
    showError(text);
    return;
  }
  pollJob(state.currentJobId, true);
}

elements.form.addEventListener("submit", submitJob);
elements.loadSampleButton.addEventListener("click", loadSample);
elements.fileInput.addEventListener("change", () => {
  renderSelectedFiles(Array.from(elements.fileInput.files));
});

["dragenter", "dragover"].forEach((eventName) => {
  elements.dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropzone.classList.add("is-dragover");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  elements.dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    elements.dropzone.classList.remove("is-dragover");
  });
});

elements.dropzone.addEventListener("drop", (event) => {
  const files = Array.from(event.dataTransfer?.files || []).filter((file) => file.type.startsWith("image/"));
  if (!files.length) {
    return;
  }
  const transfer = new DataTransfer();
  files.forEach((file) => transfer.items.add(file));
  setFiles(transfer.files);
});

elements.resetButton.addEventListener("click", () => {
  elements.form.reset();
  state.currentJobId = null;
  state.prototypeStatus = "not_requested";
  setStatusBadge("未开始", "等待提交");
  renderTimeline("", "");
  elements.jobIdText.textContent = "任务编号：-";
  showError("");
  resetArtifacts();
  renderSelectedFiles([]);
});
elements.prototypeGenerateButton.addEventListener("click", generatePrototype);

renderTimeline("", "");
loadMeta();
