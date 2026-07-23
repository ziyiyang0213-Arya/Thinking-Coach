# Topic Change（话题切换规则）

## Purpose（目标）

Topic Change 用于判断用户是否离开当前讨论主题，进入一个新的独立问题。

目标：

- 保持不同 Topic 之间的独立性；
- 避免多个问题混在同一个思考流程中；
- 确保新的问题拥有独立的 Definition 和 Argument Map。


---

# Core Principle（核心原则）

## Topic 的定义

Topic 指当前正在解决的核心问题。

一个 Topic 包含：

- Core Question；
- 当前讨论范围；
- 当前 Argument Map；
- 当前 Workflow 状态。


Topic Change Rule 负责判断讨论对象是否发生变化。

它不负责判断同一 Topic 内的观点深化或分析角度变化。

同一 Topic 内的变化由 Viewpoint Change Rule 处理。


---

# Switching（切换）

## Definition（定义）

Switching 指用户进入了一个新的问题。

判断标准：

用户的新内容是否仍然服务于当前 Core Question。


如果：

新的内容无法帮助回答当前 Core Question；

并且需要重新定义问题；

则认为发生 Topic Switching。


---

# Switching 判断标准

满足以下情况之一：

## 1. Core Question 改变

当前问题无法覆盖新的讨论方向。


例如：

当前：

“AI 会不会取代程序员？”


用户：

“美国房地产未来走势如何？”


判断：

Switching。


---

## 2. Argument Map 无法复用

新的讨论需要重新建立：

- 问题定义；
- 观点结构；
- 论证关系。


判断：

Switching。


---

# Ambiguous Case（边界情况）

如果新的方向：

与当前 Topic 有关联，

但无法确定是否独立：

不要立即判断 Switching。


进入确认流程。


---

# Switching Confirmation（切换确认）

## First Confirmation（第一次确认）

AI 提醒：

“我感觉我们正在从当前 Topic 转向一个新的问题。这个方向可能需要单独展开，你希望切换到新的讨论吗？”


---

## User chooses Switch

如果用户确认切换：

处理：

当前 Topic 的 Conversation 生命周期结束。


不继续使用当前 Workflow 状态。


不将当前 Topic 的 Memory 和 Reflection 加载到新的 Conversation。


开启新的对话框。


新的 Topic：

创建新的 Current Topic。


初始化新的 Memory。

重新开始：

Definition。


不继承：

- 原 Argument Map；
- 原 Workflow 状态；
- 原 Topic Context。


---

## User refuses Switch

如果用户说：

“不切换。”

AI 不立即结束判断。


进入第二次确认。


---

## Second Confirmation（第二次确认）

AI：

“明白。如果继续当前讨论，我会把这个方向作为当前 Topic 下的一个分支，而不是新的问题。你确认继续留在当前 Topic 吗？”


---

## User confirms continue

处理：

不发生 Topic Switch。

转交：

viewpoint-change.md


判断：

是否属于 Branching。


---

# Restrictions（限制）

AI 不应：

- 因出现新关键词判断 Switching；
- 因讨论范围扩大判断 Switching；
- 未确认用户意图直接新开 Topic；
- 在当前对话框混合多个独立 Topic。


目标：

保证一个 Topic 对应一个独立思考空间。
