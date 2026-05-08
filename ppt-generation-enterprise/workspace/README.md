# workspace 目录说明

这个目录里目前混放了两类产物：

1. 标准 workshop 交付目录
   形态是 `Workspace/<客户名称-场景名称>/`。
   这是 `scripts/generate_workshop_package.py` 当前推荐的输出方式，也是现在应该继续沿用的主路径。

2. 历史平铺式 JSON / PPT 产物
   例如 `composed-*.json`、`*-plan.json`、`presentation-plan.json`、`replacement-map.json`、`scenario-*.json`。
   这些通常来自更早的脚本调试、单步命令验证、案例沉淀或旧的平铺输出方式，不属于当前推荐的客户交付目录结构。

## 这些根级 JSON 分别是什么

- `composed-*.json`
  稀疏 workshop 输入经过资产匹配后的标准化场景数据。
- `*-plan.json` 或 `presentation-plan.json`
  供 PPT 生成器消费的演示文稿中间计划文件。
- `replacement-map.json`
  用于模板替换或下游 PPTX 写入的槽位映射结果。
- `scenario-*.json`
  某些手工案例或脚本验证用的标准化场景输入。

## 当前建议

- 新案例统一输出到 `Workspace/<客户名称-场景名称>/`。
- 根目录平铺的历史样例暂时保留，用于回归比对和脚本验证。
- 如果后续继续整理，建议新增两个子目录：
  - `_legacy-flat-outputs/`：存放旧的平铺式 JSON / PPT
  - `_regression-samples/`：存放需要长期保留的基准案例

## Windows 大小写说明

当前文档里同时出现 `workspace/` 和 `Workspace/`。在 Windows 下这通常指向同一个目录，但文档和命令建议统一写成 `Workspace/`，避免误解。