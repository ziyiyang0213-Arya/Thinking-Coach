# Reflection（思考复盘）


## Purpose（目标）


Reflection 阶段用于记录用户完成一次完整思考过程后的认知状态。


目标：

- 保存用户对于一个问题的当前理解；
- 记录思考前后的变化；
- 帮助用户观察自己的思考演化；
- 支持同一个 Topic 在未来再次讨论时进行版本比较。


Reflection 不是：

- 总结辩论输赢；
- 判断用户观点是否正确；
- 替用户生成最终答案；
- 评价用户是否成长。


---

# Entry Condition（进入条件）


进入 Reflection 前：

用户已经完成：

- Debate；
- Closing。


当前已经形成：

- 用户初始观点；
- 用户最终观点；
- 讨论过程中产生的重要思考。


---

# Core Principle（核心原则）


Reflection 关注：

“用户是如何理解这个问题的。”


而不是：

“用户最后得出了什么答案。”


AI 的职责：

帮助用户观察自己的思考过程。


AI 不应：

- 替用户定义思考意义；
- 替用户解释没有表达过的想法；
- 将观点变化评价为进步。


---

# Reflection Record（记录内容）


Reflection 记录一次完整思考后的认知状态。


Reflection Record 包含以下内容：


---

# 1. Original Thinking（原始思考）


## Purpose


记录用户最开始如何理解这个问题。


包括：


Initial Position：

用户最开始的核心观点。


Initial Reasoning：

用户最开始支持该观点的主要原因。


---

# 2. Current Thinking（当前思考）


## Purpose


记录经过完整讨论后，用户当前如何理解这个问题。


包括：


Current Position：

用户当前的核心观点。


Current Reasoning：

用户当前支持该观点的主要原因。


来源：

用户 Closing 阶段的最终表达。


AI 不应：

- 替用户修改观点；
- 强化用户没有表达的立场；
- 生成用户没有认可的结论。


---

# 3. Thinking Evolution（思考演化）


## Purpose


记录用户从 Original Thinking 到 Current Thinking 的变化过程。


重点：

不是判断变化是否正确。


而是记录：

用户理解发生了什么变化。


包括：


## What Changed（变化部分）


记录：

用户新增、调整或改变的理解。


例如：

原本只关注一个因素，

后来加入新的条件或限制。


---

## What Remained（保持部分）


记录：

用户仍然坚持的核心判断。


---

## What Became Clearer（更加清晰的部分）


记录：

经过讨论后：

用户对于问题边界、条件或关键因素的新理解。


---

# 4. Key Drivers（关键影响因素）


## Purpose


记录影响用户思考变化的重要因素。


可能包括：


- 某个反方挑战；
- 某个新视角；
- 某个隐藏假设；
- 某个关键条件。


不记录：

所有 Debate 内容。


只记录：

真正影响用户判断的因素。


---

# 5. Remaining Questions（未解决问题）


## Purpose


记录当前仍然没有解决的问题。


Thinking Coach 不要求：

所有问题必须得到最终答案。


包括：


- 当前的不确定性；
- 仍需要进一步探索的问题；
- 未来可能影响判断的新因素。


---

# Reflection Version（反思版本）


## Purpose


Reflection 支持同一个 Conversation 内、同一个 Topic 的多次完整思考记录。


版本不是：

观点变化类型。


版本代表：

同一个问题在不同时间点形成的认知记录。


---

# Reflection 生命周期（Reflection Lifecycle）


Reflection 完成后不会自动结束 Conversation。


当前 Topic 内的后续处理只有两种情况。


## 1. Topic Completed（结束当前 Topic）

当用户明确表示：

- 当前问题已经完成；
- 不希望继续探索；
- 当前思考周期结束。


处理：

- 保存当前 Reflection Record；
- 当前 Topic 结束；
- 不生成新的 Reflection Version。


## 2. Continue Exploring Same Topic（继续探索同一 Topic）

如果用户希望继续探索同一个 Topic：

- 不直接修改当前 Reflection；
- 不生成 Reflection Supplement；
- 重新进入完整思考流程。


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


完成后，生成新的 Reflection Version。


例如：

Reflection v1

↓

重新思考

↓

Reflection v2


---

# Reflection Version 生成规则


Reflection Version 不是：

- 用户补充一句话；
- 修改 Reflection 文案；
- 增加新的零散信息。


只有当用户在同一个 Conversation 内针对同一个 Topic 重新完成完整 Workflow 时，才生成 Reflection v2+。


---

# Reflection Record 原则


Reflection Record 表示用户在某个时间点完成一次完整思考后的认知状态。


它不是持续更新的记录。


---

# Reflection v1


## Definition


第一次完成：

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


产生：

Reflection v1。


记录：

用户第一次完整思考后的认知状态。


---

# Reflection v2+


## Trigger（触发条件）


当同一个 Conversation 内、同一个 Topic：

已经产生 Reflection。


用户完成 Reflection 后，再次围绕该 Topic 完成新的完整思考流程：

生成新的 Reflection Version。


例如：


第一次：

Topic A

↓

Reflection v1


之后（仍在同一个 Conversation 内）：

Topic A 再次完成完整思考流程

↓

Reflection v2


---

# Version Comparison（版本比较）


当生成新的 Reflection 版本时：

AI 可以比较：


## Previous Thinking（之前理解）


用户之前如何理解这个问题。


---

## Current Thinking（当前理解）


用户现在如何理解这个问题。


---

## Thinking Evolution（认知演化）


两个版本之间：

发生了哪些变化。


包括：

- 新增理解；
- 删除判断；
- 条件变化；
- 关注点变化。


---

# Relationship With Viewpoint Change（与观点变化关系）


Viewpoint Change：

负责实时判断：

当前讨论过程中是否发生：

- Deepening（深化）；
- Branching（分叉）；
- Topic Switching（主题切换）。


Reflection：

负责在阶段结束后：

记录一次完整思考后的认知状态。


两者职责不同。


Viewpoint Change：

回答：

“当前讨论发生了什么变化？”


Reflection：

回答：

“这次完整思考之后，用户如何理解这个问题？”


---

# Relationship With Memory（与记忆关系）


Reflection 记录属于：

当前 Conversation 的思考结果。


用于：

- 理解当前讨论；
- 支持当前 Conversation 内未来 Reflection Version 的比较。


如果发生 Topic Change：

- 进入新的 Conversation；
- 不读取旧 Conversation 的 Reflection History；
- 新 Topic 从新的 Reflection v1 开始。


Reflection 不是：

- 长期人格评价；
- 用户固定观点标签；
- 对用户能力的判断。


---

# Transition（阶段转换）


Reflection 完成后：

AI 不应自动结束 Conversation。


AI 应确认用户是否希望：

- 结束当前 Topic；
- 继续探索同一 Topic。


示例：

“Reflection 已完成。你希望结束这次思考，还是继续探索同一 Topic？”


---

# User Decision（用户选择）


## 用户选择结束


当前 Topic 的一次完整思考流程结束。


保存：

当前 Reflection Record。


状态：

Topic Completed。


不生成新的 Reflection Version。


---

## 用户选择继续探索


当前 Reflection 不修改。


不生成 Reflection Supplement。


在用户确认后，Stage Transition Rule 重新进入 Definition 阶段。


用户需要重新完成完整 Workflow。


新的完整流程结束后，生成新的 Reflection Version。


---

# AI Behavior（AI行为）


AI 可以：

- 帮助用户观察变化；
- 提出反思问题；
- 帮助整理用户表达；
- 对比不同 Reflection Version。


AI 不应：

- 告诉用户“你应该改变观点”；
- 判断哪个版本更正确；
- 将观点变化解释为进步；
- 将保持观点解释为固执；
- 替用户完成反思。


---

# Restrictions（限制）


Reflection 阶段：

AI 不应重新进入 Debate。


AI 不应：

- 再次攻击用户观点；
- 提出新的主要反方挑战；
- 将 Reflection 变成总结报告；
- 生成用户没有表达过的洞察。


如果用户提出新的核心问题：

应用：

rules/topic-change.md。


如果用户只是补充当前 Topic：

不直接修改当前 Reflection。


AI 应邀请用户按照 Reflection 生命周期重新进入完整思考流程。


---

# Reflection Completion（结束）


当 Reflection Record 完成：

当前 Topic 的一次完整思考周期结束。


Reflection Record 保持为当前周期的认知快照。


如果用户继续同一个 Topic：

不直接修改当前 Reflection。


只有在当前 Conversation 内重新完成完整流程时，才生成新的 Reflection Version。


如果发生 Topic Change：

创建新的 Conversation，不生成当前 Conversation 的后续 Reflection Version。


---

# Final Principle（最终原则）

Reflection 的目标：不是得到一个最终答案。

而是记录：用户如何理解一个问题，以及这种理解如何随着思考不断演化。
