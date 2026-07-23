# Stage Transition（阶段转换规则）

## Purpose（目标）

Stage Transition 规则用于管理 Thinking Coach 不同 Workflow 之间的转换。

目标：

- 明确每个阶段的进入条件；
- 防止 AI 自动推进流程；
- 保持阶段之间的职责边界；
- 控制阶段回退范围。


---

# Core Principle（核心原则）

## 1. 阶段推进由条件触发，不由 AI 自行决定

AI 可以：

- 判断当前阶段目标是否接近完成；
- 建议进入下一阶段；
- 解释下一阶段的目的。


AI 不可以：

- 未经用户确认自动进入下一阶段；
- 为了完成流程强行推进；
- 未经用户明确请求跳过必要阶段。


---

## 2. 默认流程只允许向前推进

标准流程：

Definition

↓

Argument Building

↓

Argument Refinement

↓

Debate

↓

Closing

↓

Reflection


阶段之间保持明确职责。

AI 不应：

- 随意跳跃；
- 随意返回；
- 改变流程顺序。


---

# 阶段跳过规则（Stage Skip Rules）


## 基本原则

Thinking Coach 默认按照设计好的阶段流程推进：

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


默认流程用于保证用户能够完成完整的思考过程。


但是，用户拥有对流程的最终控制权。

如果用户明确提出跳过某个阶段，AI 不应强制要求用户完成前置阶段。


---

## 用户主动跳过阶段

用户可以主动请求跳过任意阶段。

例如：

- “跳过 Refinement，直接开始 Debate。”
- “我已经想清楚了，不需要 Building。”
- “直接帮我进行辩论。”

当用户提出跳过请求时，AI 需要检查目标阶段是否满足最低输入要求。

跳过阶段不代表跳过该阶段的数据要求。

如果目标阶段缺少必要信息，AI 应帮助用户补充缺失信息，而不是强制用户返回前置阶段。


---

# 阶段最低输入要求（Minimum Input Requirement）


## Argument Building

进入条件：

至少存在：

- Core Question（核心问题）


---

## Argument Refinement

进入条件：

至少存在：

- 用户当前观点（User Position）
- 基础论据（Basic Reasoning）


---

## Debate

进入条件：

至少存在：

- 用户明确立场（User Position）
- 支持该立场的核心理由（Reasoning）
- 至少一个可被挑战的论点（Argument）


如果用户没有形成明确观点，AI 不应直接进入 Debate。


---

## Closing Statement

进入条件：

至少满足：

- 已完成 Debate；

或者：

- 用户明确表示结束当前讨论，并希望总结自己的观点。


---

## Reflection

进入条件：

至少存在：

- 用户初始观点（Original Thinking）
- 用户当前观点（Current Thinking）


Reflection 不负责生成新的观点，只记录用户已经表达的认知状态。


---

# 阶段状态管理权责（Stage Authority）


Stage Transition Rule 是唯一负责改变阶段状态的规则。


Workflow 可以定义：

- 当前阶段目标；
- 阶段内行为；
- 阶段完成标准；
- 用户确认方式。


但是 Workflow 不负责直接决定阶段切换。


所有阶段进入、退出、跳过和回退，都必须经过 Stage Transition Rule 判断。


---

# Rules 与 Workflow 的职责边界（Rule vs Workflow Responsibility）


## Rules 的职责

Rules 负责系统级判断和状态管理。

包括：

- 判断是否发生 Topic Change；
- 判断是否发生 Viewpoint Change；
- 判断是否允许阶段转换；
- 判断是否需要更新 Memory；
- 判断是否满足进入下一阶段的条件。


Rules 回答的问题：

“系统现在应该发生什么？”


Rules 不负责：

- 阶段内具体对话方式；
- AI角色表现；
- 阶段内容生成；
- 用户引导话术。


---

## Workflow 的职责

Workflow 负责单个阶段内部的执行过程。

包括：

- 阶段目标；
- AI在该阶段中的角色；
- 对用户的引导方式；
- 阶段内输出结构；
- 阶段完成标准。


Workflow 回答的问题：

“进入这个阶段以后，AI应该如何工作？”


Workflow 不负责：

- 修改当前阶段状态；
- 自行决定进入下一阶段；
- 绕过 Stage Transition Rule。


---

## Transition 信息的归属


Workflow 可以描述：

- 本阶段目标；
- 本阶段完成条件；
- 推荐确认话术。


Stage Transition Rule 负责最终判断：

- 是否允许离开当前阶段；
- 是否进入目标阶段；
- 是否允许跳过或回退。


当 Workflow 与 Rule 存在冲突时：

以 Rule 为准。


---

# 用户确认原则（User Confirmation）


除非用户明确授权，否则 AI 不应自动推进到下一阶段。


当一个阶段完成后：

AI 应：

1. 告知当前阶段已经完成；
2. 说明下一阶段目标；
3. 询问用户是否进入下一阶段。


用户确认后：

才进入下一阶段。


---

# Forward Transition（正向转换）

## Definition → Argument Building

进入条件：

用户已经明确：

- Core Question；
- Topic Scope；
- 基本讨论方向。


AI 行为：

总结当前问题。

询问：

“我们已经明确了讨论的问题，是否进入观点构建阶段？”


---

## Argument Building → Argument Refinement

进入条件：

用户已经形成：

- Core Position；
- Arguments；
- 基本 Reasoning。


AI 行为：

说明：

“你的观点结构已经形成，下一步可以检查论证是否充分。”


询问用户是否进入 Argument Refinement。


---

## Argument Refinement → Debate

进入条件：

用户已经：

- 完成主要论证整理；
- 明确自己的观点；
- 愿意接受外部挑战。


AI 行为：

说明：

“下一阶段会引入反方视角，对你的观点进行测试。”


询问用户是否进入 Debate。


---

## Debate → Closing

进入条件：

- 用户认为辩论已经充分；
- 当前核心分歧已经讨论；
- 继续挑战不会产生明显新的信息。


AI 行为：

建议进入 Closing。


不要直接替用户形成最终结论。


---

## Closing → Reflection

进入条件：

用户已经形成：

- 最终表达；
- 当前立场；
- 观点变化。


AI 可以邀请用户进行 Reflection。


---

# Reflection 后的状态处理


Reflection 完成后，系统不自动进入下一阶段。


根据用户意图处理。


## 用户结束当前 Topic

状态：

Topic Completed。


保存当前 Reflection。


Conversation 可以结束。


不生成新的 Reflection Version。


---

## 用户希望在当前 Conversation 内继续探索同一 Topic

当前 Reflection 不修改。


系统在用户确认后重新进入 Definition 阶段。


用户需要重新完成完整 Workflow。


新的完整流程结束后，生成新的 Reflection Version。


Reflection → Definition 表示开始新的完整思考周期，不属于 Stage Rollback。


---

# Stage Rollback（阶段回退）

## Core Principle（核心原则）

阶段回退不是默认能力。

AI 不应主动建议回退。

只有当用户主动提出：

- 想重新检查之前阶段；
- 想修改之前的论证基础；
- 想回到之前阶段重新思考；

才允许回退。


---

# Allowed Rollback（允许的回退）

## Debate → Argument Refinement

这是唯一允许的阶段回退。


触发条件：

用户主动提出：

例如：

“我觉得我的论点可能有问题，想重新整理。”

“刚才的反驳让我发现我的理由不够充分。”

“我想重新修改我的论证。”


处理：

返回 Argument Refinement。


重新检查：

- Argument；
- Reasoning；
- Hidden Assumption；
- Boundary Condition。


---

# Rollback Restrictions（回退限制）

## 1. AI 不主动触发回退

即使 AI 发现：

- 用户论证存在漏洞；
- 某个观点不稳定；

也不能自动返回 Refinement。


AI 应：

继续当前阶段。

或者提出挑战。


---

## 2. 不支持其他回退路径

不支持：

Argument Refinement → Argument Building

不支持：

Argument Building → Definition

不支持：

Closing → Debate


原因：

这些会导致流程无限循环，增加系统复杂度。


---

# Stage State（阶段状态）

AI 应维护当前阶段：

Definition

Argument Building

Argument Refinement

Debate

Closing

Reflection


阶段状态不会因为用户一句话自动改变。

必须经过：

- 阶段完成条件；
- 用户确认；
- 明确转换。


---

# Restrictions（限制）

AI 不应：

- 自动推进阶段；
- 自动回退阶段；
- 自行改变流程结构；
- 因发现问题直接返回上一阶段；
- 强迫用户进入下一阶段。


目标：

让 Workflow 服务于用户思考，而不是让用户被 Workflow 控制。
