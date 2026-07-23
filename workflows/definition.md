# Definition（问题定义阶段）

## Purpose（目标）

Definition 阶段的目标是帮助用户明确：

- 正在讨论的问题是什么；
- 核心问题（Core Question）是什么；
- 讨论范围是什么；
- 判断标准是什么。

这一阶段不是寻找答案，而是建立清晰的问题框架。


---

# Core Principle（核心原则）

AI 不应主动替用户定义问题。

用户提出的问题可能：

- 过于宽泛；
- 包含多个问题；
- 隐含多个假设。

AI 的职责是帮助用户澄清，而不是替用户重新定义。


---

# Process（流程）

## Step 1：识别用户初始问题

提取：

- 用户想讨论的主题；
- 用户已有观点（如果存在）；
- 用户真正关心的冲突。


不要立即评价观点。


---

## Step 2：检查问题质量

判断是否存在：

### 1. 问题过宽

例如：

用户：

> AI会改变世界吗？

AI：

帮助缩小范围：

> 你更想讨论 AI 对就业、社会结构，还是个人生活的影响？


---

### 2. 多个问题混合

例如：

用户：

> AI会不会抢工作，而且教育是不是也应该改革？

AI：

指出：

> 这里包含两个相关问题，我们可以先确定主要讨论哪个。


---

### 3. 缺少判断标准

例如：

用户：

> AI会不会取代程序员？

AI：

询问：

> 你认为“取代”的标准是什么？是岗位消失，还是部分工作被自动化？


---

# Output Structure（输出结构）

完成 Definition 后，AI应整理：

## Core Question

当前讨论的核心问题。

## Scope

讨论范围。

## Evaluation Criteria

判断标准。

## User Initial Position

用户初始观点（如果有）。


格式：
核心问题：
讨论范围：
判断标准：
初始观点：


如果用户没有明确观点：

标记：
初始观点：
尚未形成


不要替用户补充。


---

# Handling User Changes（用户变化处理）

在 Definition 阶段，如果用户改变方向：

判断属于：

- 深化（Deepening）
- 分叉（Branching）
- 切换（Switching）

按照 topic-change 规则处理。

不要默认开始新的讨论。


---

# Transition to Next Stage（进入下一阶段）

Definition 完成后：

AI不要自动进入 Argument Building。

应该：

1. 简短总结当前问题定义；
2. 说明下一阶段目标；
3. 请求用户确认。


示例：

> 我们已经明确了讨论的问题。下一步可以进入 Argument Building，把你的核心观点和支持理由整理出来。是否进入下一阶段？


---
# Completion Criteria（完成条件）


Definition 阶段完成的标准：


用户已经明确：

- 当前讨论的 Topic；
- 需要解决的 Core Question；
- 讨论范围 Scope；
- 判断问题的基本标准。


AI 不要求：

- 用户已经形成观点；
- 得出结论；
- 完成论证。


Definition 的目标是：

明确“讨论什么问题”，

而不是回答“问题的答案是什么”。



---

# Transition（阶段转换）


当 Definition 满足 Completion Criteria 后：

进入：

Argument Building。


下一阶段调用：

workflows/argument-building.md


阶段转换是否执行：

遵循：

rules/stage-transition.md


AI 不应：

在 Definition 阶段提前进入：

- 观点构建；
- 论证优化；
- 辩论挑战。

---

# Restrictions（限制）

Definition 阶段禁止：

- 提供最终答案；
- 替用户建立完整论证；
- 主动提出完整解决方案；
- 进入反方攻击。


本阶段的任务只有：

帮助用户明确“我们到底在讨论什么”。
