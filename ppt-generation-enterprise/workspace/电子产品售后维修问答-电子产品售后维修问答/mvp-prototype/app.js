const prototypeData = {
  "scenario": {
    "name": "电子产品售后维修问答",
    "goal": "为售后人员提供统一的维修知识检索、问题问答和处理协同入口",
    "value": "让售后人员从人工翻资料和反复请教专家，转向在一个工作台中完成检索、判断和处理动作。"
  },
  "outcomes": [
    "缩短售后人员查询资料和定位问题的时间",
    "提升常见维修问题的标准化处理效率",
    "降低对资深专家经验的过度依赖",
    "推动维修知识持续沉淀和复用"
  ],
  "next_actions": [
    "确认试点产品范围和高频故障问题清单",
    "整理维修手册、FAQ 和历史工单样本",
    "两周内完成问答工作台原型和首轮效果验证"
  ]
};

document.getElementById("simulate-button")?.addEventListener("click", () => {
  const outcomes = prototypeData.outcomes.length
    ? prototypeData.outcomes.join(" / ")
    : prototypeData.scenario.value || "AI 已刷新当前场景建议。";
  window.alert(`模拟完成\n\n场景：${prototypeData.scenario.name}\n目标：${prototypeData.scenario.goal}\n\n预期结果：${outcomes}`);
});
