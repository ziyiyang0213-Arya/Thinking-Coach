# Thinking Coach Testing Strategy

## Purpose（目标）

Testing 用于验证 Thinking Coach 是否按照设计的 Skill、Workflow 和 Rules 执行。

测试重点不是判断用户观点是否正确，而是验证：

- AI 是否遵守阶段职责；
- Workflow 是否正确流转；
- Rules 是否正确触发；
- AI 是否保持用户最终控制权。


---

# Testing Principle（测试原则）

Thinking Coach 使用 Scenario Based Testing（场景测试）。

每个测试案例模拟一次真实用户讨论过程。

测试关注：

“AI 是否按照设计行为运行。”

而不是：

“AI 是否产生某个固定答案。”


---

# Test Types（测试类型）

## 1. Workflow Test

验证单个 Workflow 是否符合设计。

检查：

- 阶段目标是否达成；
- AI角色是否正确；
- 输出是否符合要求；
- 是否越界进入其他阶段。

Examples：

- Definition 是否帮助用户明确问题；
- Debate 是否保持反方角色；
- Reflection 是否记录认知变化。


---

## 2. Rule Test

验证跨阶段 Rules 是否正确工作。

包括：

- Topic Change；
- Viewpoint Change；
- Stage Transition；
- Memory Update。

检查：

- 是否按照优先级判断；
- 是否触发正确规则；
- 是否避免错误切换。


---

## 3. Transition Test

验证阶段流转逻辑。

检查：

- 正常流程是否可完成；

Definition

↓

Argument Building

↓

Argument Refinement

↓

Debate

↓

Closing Statement

↓

Reflection


同时验证：

- 用户主动跳过；
- 用户请求回退；
- 用户结束阶段；

是否满足对应条件。


---

## 4. Full Session Test

验证完整 Thinking Coach 流程。

一个完整测试案例应包含：

User Topic

↓

Definition

↓

Argument Building

↓

Argument Refinement

↓

Debate

↓

Closing Statement

↓

Reflection


检查：

- 阶段是否正确进入；
- Memory 是否正确保存；
- Reflection 是否正确生成。


---

# Test Case Structure（测试案例结构）

每个测试案例包含：

## Scenario

描述：

- 用户输入；
- 当前 Topic；
- 当前阶段。


## Expected Behavior

描述：

AI 应该：

- 做什么；
- 如何回应；
- 是否进入下一阶段。


## Failure Conditions

描述：

什么情况代表失败。

例如：

- AI替用户形成观点；
- AI提前进入下一阶段；
- Debate变成协助用户补充论据；
- Reflection生成用户未表达的结论。


---

# Future Test Cases（后续测试案例）

后续可根据需要增加：

```
tests/

├── README.md
├── definition-test.md
├── building-test.md
├── refinement-test.md
├── debate-test.md
├── closing-test.md
├── reflection-test.md
└── full-session-test.md
```

当前版本仅定义测试规范。

具体测试案例将在 Workflow 实现阶段逐步补充。
