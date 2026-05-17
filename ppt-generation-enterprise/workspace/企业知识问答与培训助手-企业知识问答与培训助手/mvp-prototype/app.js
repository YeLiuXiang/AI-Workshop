const prototypeData = {
  "scenario": {
    "name": "企业知识问答与培训助手",
    "goal": "把知识检索、智能问答、培训内容整理和知识回写整合到一个统一工作台中",
    "value": "让培训与知识管理负责人先在一个统一工作台里看到 AI 对知识问答、培训整理和组织沉淀的直接价值。"
  },
  "outcomes": [
    "缩短员工获取知识和培训内容的时间",
    "降低专家重复答疑投入，提升知识复用率",
    "把答疑记录和培训材料持续沉淀为可运营的企业知识资产"
  ],
  "next_actions": [
    "确认首批接入的制度文档、项目案例和 FAQ 范围",
    "选择一个高频培训主题和一类典型答疑问题作为试点",
    "输出工作台原型范围、样例数据和 POC 验证口径"
  ]
};

document.getElementById("simulate-button")?.addEventListener("click", () => {
  const outcomes = prototypeData.outcomes.length
    ? prototypeData.outcomes.join(" / ")
    : prototypeData.scenario.value || "AI 已刷新当前场景建议。";
  window.alert(`模拟完成\n\n场景：${prototypeData.scenario.name}\n目标：${prototypeData.scenario.goal}\n\n预期结果：${outcomes}`);
});
