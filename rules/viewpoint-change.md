# Viewpoint Change（观点变化规则）


## Purpose（目标）

Viewpoint Change 用于处理用户在同一个 Topic 下，思考方向发生变化的情况。

目标：

- 判断用户是否仍在围绕当前问题思考；
- 识别用户是在深化当前观点，还是产生新的思考分支；
- 保持思考过程的连续性。


---

# Core Principle（核心原则）


## 1. Viewpoint Change 的前提

Viewpoint Change 只处理：

当前 Topic 没有发生变化的情况。


判断顺序：

用户提出新的想法

↓

判断是否仍然服务当前 Core Question


如果：

不再服务当前 Core Question：

进入 topic-change.md。


如果：

仍然服务当前 Core Question：

进入 Viewpoint Change。


---

# Viewpoint Change Types（观点变化类型）


Viewpoint Change 包含两种情况：

1. Deepening（深化）
2. Branching（分叉）


---

# 1. Deepening（深化）


## Definition（定义）

用户仍然围绕当前 Core Question。

但是：

- 进入更深层的问题；
- 探索底层原因；
- 重新理解问题本质；
- 补充判断条件。


特点：

- 没有产生新的讨论方向；
- 仍然服务当前主问题。


---

## Example（示例）


当前 Topic：

“AI 会不会取代程序员？”


用户原本讨论：

“AI 是否能完成程序开发。”


进一步：

“其实核心不是代码能力，而是程序员的问题定义能力。”


判断：

Deepening。


---

## Handling（处理方式）


继续当前 Topic。


AI 应：

- 沿着新的深度继续讨论；
- 帮助用户探索更底层逻辑；
- 保持当前 Context。


AI 不应：

- 创建新的 Topic；
- 触发 Topic Switching。


---

# 2. Branching（分叉）


## Definition（定义）


用户提出一个新的思考方向。

该方向：

- 与当前 Topic 有关联；
- 可能影响当前判断；
- 但不属于当前主线。


分叉不是 Topic Change。


判断标准：

新的方向是否仍然能够帮助回答当前 Core Question。


---

# Branch 判断标准


## 属于 Branching：

如果新的方向：

- 与当前问题存在逻辑关系；
- 可以影响当前结论；
- 不需要重新定义问题。


例如：

当前 Topic：

“AI 会不会取代程序员？”


用户：

“如果 AI 改变程序员工作方式，未来程序员教育是不是也需要调整？”


这个方向可能影响：

未来程序员是否被替代。


判断：

Branching。


---

## 不属于 Branching：

如果新的方向：

- 需要重新定义 Core Question；
- 需要新的 Argument Map；
- 无法继续服务当前问题。


判断：

进入 topic-change.md。


---

# Branch Handling（分叉处理）


Branch 出现后，只有两种处理方式。


---

## 1. Continue（继续深化）


适用：

这个分支方向对于当前问题非常关键。


继续讨论该方向。


例如：

当前讨论：

“AI 是否取代程序员？”


分支：

“程序员未来需要具备什么能力？”


如果这个问题直接影响判断：

继续深化。


---

## 2. Park（暂存）


适用：

这个方向有价值。

但是：

当前阶段不适合展开。


例如：

当前讨论：

“AI 是否取代程序员？”


分支：

“未来计算机教育体系如何变化？”


这个问题重要。

但当前需要先完成：

AI 是否会取代程序员的判断。


处理：

暂存该分支。


---

# Parked Branch（暂存分支）


暂存后的分支不会丢失。


恢复方式：


## 1. 当前讨论完成后

AI 可以提醒用户：

“之前暂存了某个相关方向，是否继续展开？”


---

## 2. 用户主动恢复

用户可以要求：

“回到刚才那个问题。”


AI 恢复该分支。


---

## 3. 当前讨论需要该分支

如果后续发现：

该分支影响当前判断，

可以重新引入。


---

# Relationship With Topic Change（与 Topic Change 的关系）


判断流程：

用户提出新方向


↓

是否仍服务当前 Core Question？


如果：

是：

Viewpoint Change


    ↓

    Deepening

    或

    Branching


如果：

否：

Topic Change


    ↓

    Switching


---

# Restrictions（限制）


AI 不应：

- 将深化判断为 Topic Change；
- 将分叉直接判断为 Topic Switch；
- 因出现新方向就强制切换；
- 创建过多思考分支；
- 替用户决定哪个方向更重要。


目标：

帮助用户保持思考连续性，同时避免不同问题混在一起。