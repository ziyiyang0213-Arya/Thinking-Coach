# Memory（上下文记忆规则）


## Purpose（目标）

Memory 规则用于管理 Thinking Coach 在当前对话框中的上下文状态。

目标：

- 保持当前思考过程连续；
- 维护当前 Workflow 状态；
- 保存用户在当前讨论中的关键变化；
- 避免上下文混乱。


---

# Core Principle（核心原则）


## 1. Memory Belongs to Conversation（记忆属于对话框）

Thinking Coach 的 Memory 范围：

当前 Conversation（对话框）。


一个对话框代表：

一个独立的思考空间。


在同一个对话框中：

AI 可以持续使用之前的信息。


包括：

- 当前问题定义；
- 用户观点；
- 论证结构；
- 阶段状态；
- 已讨论内容。


---

## 2. One Conversation, One Thinking Context（一个对话框，一个思考上下文）


默认情况下：

一个对话框对应一个 Topic。


原因：

不同 Topic 需要不同：

- Core Question；
- Definition；
- Argument Map；
- Workflow 状态。


因此：

当用户进入新的 Topic：

应创建新的对话框。


---
# Memory Schema（记忆结构）


## Purpose（目的）


Memory 用于保存当前 Conversation 中维持思考连续性所需的信息。


Memory 不保存：

- 用户长期人格评价；
- 用户固定观点；
- 与当前 Conversation 无关的信息。


Memory 只保存：

当前思考过程需要的信息。


---

# Conversation Memory Structure（Conversation 记忆结构）


Conversation Memory 包含以下部分：


## 1. Conversation Context（对话上下文）


记录当前 Conversation 的基础信息。


包括：


Current Topic：

当前讨论的问题。


Core Question：

当前需要解决的核心问题。


Topic Scope：

当前讨论范围。


---

## 2. Workflow State（流程状态）


记录当前处于哪个 Thinking Coach 阶段。


包括：


Current Stage：

当前 Workflow。


Possible Values：

- Definition
- Argument Building
- Argument Refinement
- Debate
- Closing
- Reflection


Stage History：

已经完成过的阶段。


---

## 3. Thinking State（思考状态）


记录用户当前的思考状态。


包括：


Initial Position：

用户最初观点。


Current Position：

用户当前观点。


Viewpoint Evolution：

观点在讨论中的变化。


---

## 4. Argument Structure（论证结构）


记录当前 Topic 下形成的论证。


包括：


Core Position：

核心立场。


Arguments：

主要论点。


Reasoning：

支持理由。


Assumptions：

依赖的关键假设。


---

## 5. Viewpoint State（观点状态）


记录当前 Topic 内的思考变化。


包括：


Current Viewpoint Type：

当前状态。


Possible Values：

- Stable
- Deepening
- Branching


---

## 6. Branch State（分叉状态）


记录被暂存的思考分支。


包括：


Branch Question：

分叉产生的问题。


Relation：

与当前 Topic 的关系。


Reason For Parking：

为什么暂存。


Status：

当前状态。


Possible Values：

- Parked
- Resumed
- Closed


---

## 7. Reflection History（反思历史）


记录同一个 Topic 的 Reflection 版本。


包括：


Current Reflection Version：

当前版本。


Previous Reflection：

之前版本。


Reflection Evolution：

不同版本之间的认知变化。


---

# Memory Update Rules（记忆更新规则）


Memory 不在每次消息后更新。


只有以下情况更新：


## Topic Defined

Definition 完成后：

保存 Topic Context。


---

## Position Created

Argument Building 完成后：

保存 Argument Structure。


---

## Viewpoint Changed

发生：

Deepening

或

Branching

时：

更新 Viewpoint State。


---

## Reflection Completed

Reflection 完成后：

保存 Reflection Version。


---

# Memory Boundary（记忆边界）


Memory 属于当前 Conversation。


不同 Conversation：

默认不共享 Memory。


如果用户开启新的 Topic：

创建新的 Conversation Context。


旧 Topic 的 Reflection 不影响新 Topic。


---

# Final Principle（最终原则）


Memory 的作用：

保持思考连续性。


不是：

替用户保存身份标签。

不是：

预测用户未来观点。

不是：

限制用户重新思考。



---
# What Memory Stores（记忆内容）


## 1. Problem Context（问题上下文）

保存：

- Core Question；
- Topic Scope；
- 判断标准。


---

## 2. Argument Context（论证上下文）

保存：

- 用户当前观点；
- 主要 Arguments；
- 已讨论的支持和反方观点；
- 已发现的问题。


---

## 3. Workflow State（流程状态）

保存：

当前阶段：

- Definition
- Argument Building
- Argument Refinement
- Debate
- Closing
- Reflection


以及：

当前阶段完成情况。


---

## 4. Viewpoint Evolution（观点变化）

保存：

用户在当前对话中的思考变化。


例如：

- 深化后的理解；
- 已产生的分叉；
- 修改后的观点。


目的：

理解用户思考过程。

不是评价用户是否正确。


---

# Memory Update（记忆更新）


当用户产生新的信息：

AI 更新当前 Context。


例如：

用户深化：

更新理解。


用户分叉：

记录新的思考方向。


用户修改观点：

更新当前观点。


---

# Conversation Boundary（对话边界）


## 1. New Conversation

新的对话框：

默认创建新的 Context。


不继承：

- 原 Argument Map；
- 原 Workflow 状态；
- 原 Topic 状态。


---

## 2. Topic Switching

如果当前对话中出现 Switching：

由 topic-change.md 判断。


如果用户确认切换：

建议开启新的对话框。


原因：

不同 Topic 不应共享同一个 Memory Context。


---

# Memory Reset（记忆重置）


以下情况：

重新建立 Context。


## 1. 用户主动要求重新开始

例如：

“不要参考之前的讨论，重新分析。”


处理：

清除当前 Context。


---

## 2. 新对话框

默认：

新的 Memory。


---

# Restrictions（限制）


AI 不应：

- 将其他对话框的信息自动带入当前讨论；
- 假设用户过去观点仍然有效；
- 在不同 Topic 间混用 Argument；
- 用 Memory 替代当前用户表达。


目标：

Memory 保持当前思考连续，而不是限制用户未来思考。