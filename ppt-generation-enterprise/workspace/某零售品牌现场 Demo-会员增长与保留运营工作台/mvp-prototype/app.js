const prototypeData = {
  "scenario": {
    "name": "会员增长与保留运营工作台",
    "goal": "把会员洞察、内容生产、活动分析和保留动作集中到一个可操作的工作台中",
    "value": "让会员运营团队从多系统切换和人工拼装，转向在一个工作台里完成洞察、生成、复盘和干预。"
  },
  "outcomes": [
    "缩短从会员洞察到活动上线的准备周期",
    "提升营销内容、配图和页面草稿的生成效率",
    "让活动分析结果更快回流到下一轮增长与保留动作",
    "更早识别高流失风险会员并启动干预"
  ],
  "next_actions": [
    "确认一个重点会员客群和一类活动场景作为试点",
    "准备会员画像、活动结果和高流失会员样本数据",
    "两周内完成工作台原型与验证口径",
    "四周内完成首轮 POC 复盘与扩展建议"
  ]
};

document.getElementById("simulate-button")?.addEventListener("click", () => {
  const outcomes = prototypeData.outcomes.length
    ? prototypeData.outcomes.join(" / ")
    : prototypeData.scenario.value || "AI 已刷新当前场景建议。";
  window.alert(`模拟完成\n\n场景：${prototypeData.scenario.name}\n目标：${prototypeData.scenario.goal}\n\n预期结果：${outcomes}`);
});
