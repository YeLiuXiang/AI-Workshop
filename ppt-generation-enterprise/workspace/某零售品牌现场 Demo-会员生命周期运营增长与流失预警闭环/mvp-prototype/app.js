const prototypeData = {
  "scenario": {
    "name": "会员生命周期运营增长与流失预警闭环",
    "goal": "把会员洞察、营销内容生成、活动落地、效果复盘和流失干预集中到一个可操作的工作台中",
    "value": "让会员运营团队从多系统切换和人工拼装，转向在一个工作台里完成洞察、生成、复盘和保留联动。"
  },
  "outcomes": [
    "缩短会员运营从洞察到活动上线的准备周期",
    "提升营销内容、配图和活动页面的生产效率",
    "让活动复盘结果更快回流到下一轮会员增长动作",
    "更早识别高流失风险会员并启动保留干预"
  ],
  "next_actions": [
    "确认一个重点会员客群和一类典型活动作为试点",
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
