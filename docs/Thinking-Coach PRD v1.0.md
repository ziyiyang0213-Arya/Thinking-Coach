# Thinking Coach Product Requirements Document (PRD) v1.0

**产品阶段：** Agent Runtime Prototype  
**文档语言：** 中文主体，保留必要英文术语  
**产品形态目标：** Web-based AI Thinking Assistant

## Executive Summary

Thinking Coach 是一个帮助用户进行结构化思考的 AI 思考伙伴。它不替用户寻找答案、做决定或完成核心推理，而是通过问题定义、观点构建、论证强化、反方挑战、结辩与反思，帮助用户形成更清晰、更完整、可被检验的个人理解。产品的核心产出不是“标准答案”，而是一段由用户主导、经由挑战与复盘形成的思考过程。

本 PRD 将当前 Agent Skill 设计转化为可实现、可测试的产品需求基线。当前优先验证 Agent Runtime Prototype 的流程有效性、规则一致性、Memory 连续性和 Reflection 价值；Web MVP 及后续产品在此基础上实现长期、多轮的结构化思考空间。

# Part 1 Product Definition（产品定义）

## 1. Product Vision（产品愿景）

Thinking Coach 帮助用户针对复杂问题进行结构化思考。它不替用户寻找答案，而是引导用户明确问题、建立观点、检验论证、接受挑战并观察认知变化，最终形成属于用户自己的理解。

**核心价值：** 帮助用户从“拥有一个想法”，走向“理解自己的想法为什么成立”。

English summary: *Thinking Coach transforms thoughts into structured understanding through user-owned reasoning, challenge, and reflection.*

## 2. Problem Statement（问题定义）

面对“是否换工作”“AI 是否会取代人”“这个选择是否正确”等复杂问题，用户常直接跳到结论，却没有明确核心问题、判断标准和讨论边界。即使用户已有观点，也往往缺少支持理由、隐藏假设、适用条件和可被检验的推理链。

普通聊天 AI 常以认可、建议和快速答案为默认行为，难以提供真正的逻辑压力测试；而用户完成一次讨论后通常只留下原始聊天记录，无法清楚看见当时如何理解问题、哪些挑战改变了判断、后续认知如何演化。

Thinking Coach 要解决的不是“信息不够”，而是“用户缺少一个由自己掌控的完整思考过程”。

## 3. Product Positioning（产品定位）

Thinking Coach 是一个帮助用户进行深度思考与认知迭代的 AI Agent。它不是 AI Search Tool，不以快速检索为主；不是 AI Advisor，不替用户做决定；也不是通用 AI Assistant，不以代办执行为核心。

传统 AI 的默认链路是“用户提问 → AI 给答案”。Thinking Coach 的链路是“用户提出问题 → 定义问题 → 构建自己的观点 → 接受挑战 → 完成表达 → 记录认知变化”。产品必须保持用户对讨论方向、观点调整和阶段推进的最终解释权。

## 4. Target Users（目标用户）

核心用户是经常面对复杂判断、希望提升独立思考能力且不满足于简单答案的人，包括产品经理、创业者、管理者、知识工作者与学习者。典型需求包括：决策前拆解问题；表达观点时建立逻辑；面对争议时获得高质量挑战；长期观察自己的认知变化。

## 5. Product Form（产品形态）

最终产品形态为 Web-based AI Thinking Assistant：用户在网页内开展长期、多轮的思考 Session，体验重点不是普通聊天窗口，而是一个结构化思考空间。

当前阶段是 Agent Runtime Prototype，验证 Workflow、Rules、Memory 与 Reflection 是否有效。产品演进路径为：Skill Design → Agent Prototype → Web MVP → Full Product。

## Product Evolution Strategy（产品演进策略）

Thinking Coach 分为两个阶段。

### Phase 1: Agent Runtime Prototype

目标是验证核心思考机制，重点验证 Workflow 是否有效、Rules 是否一致、Memory 是否支持连续思考，以及 Reflection 是否产生价值。当前阶段不关注 UI 设计、用户系统、商业化能力或多用户场景。

### Phase 2: Web MVP

目标是将经过验证的 Thinking Coach Agent 转化为用户可持续使用的产品，可增加 Web 交互界面、Session 管理、Reflection History、Topic 管理与可视化思考过程。Web MVP 不改变 Agent 核心行为，只提供更好的使用体验。

# Part 2 Core Experience（核心体验）

## 6. User Journey（用户旅程）

一个 Session 默认对应一个独立的思考空间。用户提出需要深入分析的问题后，Agent 先帮助明确 Topic、Core Question、Scope 和 Evaluation Criteria；随后由用户形成核心立场、论点与理由；再协作式强化论证；进入反方压力测试；由用户完成结辩；最后记录本次完整思考后的认知快照。

```text
Definition → Argument Building → Argument Refinement → Debate → Closing Statement → Reflection
```

任何阶段完成后，AI 只能说明当前完成情况、下一阶段目的并询问用户；未经确认不得自动推进。用户可明确请求跳过阶段，但目标阶段仍必须满足最低输入要求；缺少信息时，AI 应补齐必要输入，而不是强制回到前置阶段。

## 7. Thinking Workflow（思考工作流）

| 阶段 | 用户目标 | AI 角色 | 核心产出 | 不应做什么 |
|---|---|---|---|---|
| Definition | 明确讨论什么 | 澄清者 | Core Question、Scope、Criteria | 直接回答复杂问题或替用户立论 |
| Argument Building | 表达自己怎么看 | 结构化伙伴 | Position、Arguments、Reasoning | 反驳、攻击、补写核心立场 |
| Argument Refinement | 让论证更清楚 | 合作伙伴 | 假设、逻辑链、边界条件 | 进入反方对抗或替换立场 |
| Debate | 压力测试主张 | 反方 | 核心分歧、挑战与回应 | 帮用户补论或宣判胜负 |
| Closing Statement | 完成自己的最终表达 | 表达引导者 | 当前立场、回应、未确定性 | 替用户写结辩 |
| Reflection | 记录认知快照 | 反思引导者 | Reflection Record 与版本 | 把反思写成总结、评价成长或新增洞察 |

Argument Refinement 与 Debate 可检查同类问题，例如隐藏假设、逻辑跳跃、反例和边界条件，但目的不同：前者帮助用户回答“我的观点如何更清晰”，后者挑战“你的观点为什么可能不成立”。

## 8. Core Interaction Model（核心交互模型）

AI 的默认交互是提问、反例、假设检验与逻辑分析，而非替用户输出完整观点或最终答案。挑战对象始终是观点、论证、推理链、假设与因果关系，不是用户能力、人格或智力。

当用户提出新的问题、方向、角度或条件时，系统先判断是否仍服务当前 Core Question；若不是，进入 Topic Change 确认流程；若是，再判断属于 Deepening 或 Branching。用户可以接受、拒绝或重新界定 AI 的观察，AI 不自行决定用户“真正想讨论什么”。

# Part 3 Functional Requirements（功能需求）

## 9. Topic Management（话题管理）

每个 Conversation 默认只承载一个 Topic。Topic 由 Core Question、Scope、Argument Map 与 Workflow State 构成。新内容不因出现新关键词或范围扩大而自动切换；只有无法继续服务当前 Core Question、需要重新定义问题或无法复用 Argument Map 时，才候选为 Topic Switching。

对于模糊情况，AI 必须发起确认。用户确认切换后，当前 Topic Conversation 生命周期结束，当前 Workflow State 停止使用，旧 Topic 的 Memory 与 Reflection 不加载到新 Conversation；新 Conversation 创建新的 Current Topic 与 Memory Context，并从 Definition 开始。用户拒绝切换并确认留在当前 Topic 时，系统交由 Viewpoint Change Rule 判断 Branching。

## 10. Workflow Engine（工作流引擎）

Workflow Engine 管理六个阶段的加载与执行。Workflow 只定义阶段目标、角色、引导方式、输出结构与完成标准；Stage Transition Rule 是唯一可以改变阶段状态的规则。所有进入、退出、跳过和回退均需经该 Rule 判断，Rule 与 Workflow 冲突时以 Rule 为准。

Workflow Engine 根据当前 Workflow State 加载对应 Workflow，系统默认只加载当前阶段 Workflow；Rules 作为全局判断层始终可访问。

默认流程向前推进。用户可跳过任意阶段，但最低输入不可省略：Building 需要 Core Question；Refinement 需要 User Position 与 Basic Reasoning；Debate 需要 Position、Reasoning 与至少一个可挑战 Argument；Closing 需要完成 Debate 或用户明确结束讨论；Reflection 需要 Original Thinking 与 Current Thinking。唯一允许的回退为用户主动提出的 Debate → Argument Refinement。

## 11. Debate System（辩论系统）

Debate 只在用户已有可被挑战的 Position、Arguments 与 Reasoning 后进行。AI 自动承担高质量反方，依次进行 Questioning、Counter Argument 与 Open Debate。质询一次聚焦一个核心问题，优先攻击隐藏假设、薄弱环节、边界条件与反例；反方立论给出 1–3 个有竞争力且彼此有区分的反方论点；自由辩围绕核心分歧连续攻防。

反方攻击必须忠实于用户真实主张。AI 可以挑战论据、假设、边界和判断标准，但不得将概率判断极端化、强迫用户证明绝对命题或攻击用户未提出的立场。AI 可以承认用户回应中有效的部分，但应继续测试剩余限制与分歧，而不是转为协助补论。

## 12. Reflection System（反思系统）

Reflection 是一次完整思考周期结束后的认知快照，不是持续编辑的笔记。Reflection Record 包含 Original Thinking、Current Thinking、Thinking Evolution、Key Drivers 和 Remaining Questions，重点记录用户如何理解问题发生变化，不评价观点是否正确、是否进步或是否成长。

完成 Reflection 后，Conversation 不自动结束。对于当前 Topic，用户可选择 Topic Completed：保存当前 Reflection Record、结束 Topic、不生成新版本；或选择继续探索同一 Topic：当前 Reflection 不修改、不生成 Supplement，系统从 Definition 开启新的完整周期。只有在同一 Conversation、同一 Topic 内重新完成完整 Workflow，才生成 Reflection v2+ 并与先前版本比较。

## 13. Memory System（记忆系统）

Memory 只服务当前 Conversation，保存 Conversation Context、Workflow State、Thinking State、Argument Structure、Viewpoint State、Branch State 与 Reflection History。它不保存人格评价、固定观点标签或与当前 Conversation 无关的信息。

Memory 有两层更新机制。Current State Update 在用户产生有效的新观点、论据、条件、回应或方向时更新，以维持当前 Workflow 连续运行；它不生成版本。Stage Snapshot Update 在阶段完成并确认后保存稳定状态：Definition 保存问题边界，Building 保存 Position/Reasoning/Arguments，Refinement 保存强化后的论证与假设，Debate 保存主要挑战、回应与剩余问题，Reflection 保存 Record 与 Version。

Memory 不等同于 Conversation History。Conversation History 保存完整交互记录；Memory 保存经过整理的结构化状态，用于支持 Workflow 执行与 Reflection。系统不应将所有聊天内容无差别写入 Memory。

# Part 4 Agent Architecture（Agent 架构）

## 14. Agent Behavior Model（行为模型）

Agent 的不可违背原则是：不替代用户思考；挑战观点而非用户；用户拥有最终解释权；AI 管理流程、用户控制路径；默认不主动完成用户核心推理。用户可以选择讨论方向、是否接受挑战、是否调整观点、是否进入下一阶段。

运行时采用分层加载。SKILL.md 与四类 Rules 始终加载，用于保持产品定位、判断与状态边界；当前阶段只加载对应 Workflow，降低无关指令对阶段行为的干扰。Rules 回答“系统现在应该发生什么”，Workflow 回答“进入这个阶段以后，AI 应如何工作”。

## 15. Rules System（规则系统）

Rules 的优先级为：Topic Change → Viewpoint Change → Stage Transition → Memory Update。Topic Change 先判断是否还是同一个问题；确认仍属当前 Topic 后，Viewpoint Change 再判断 Deepening 或 Branching；Stage Transition 判断是否允许状态变化；Memory Update 维护当前状态与阶段快照。

Deepening 指仍围绕当前 Core Question 进入更深层原因、条件或问题本质；Branching 指仍能影响当前结论但不属于当前主线的新方向，可继续或暂存。Branch 不等于 Topic Change，Topic Change 也不因范围扩大而自动发生。

## 16. State Management（状态管理）

核心状态层级为：Conversation → Topic → Workflow Stage → Thinking State → Memory。Conversation 是独立思考空间；Topic 是当前核心问题；Workflow Stage 是当前阶段；Thinking State 包含用户的立场、论证与变化；Memory 保存维持本 Conversation 连续性所需的信息。

Workflow Stage 采用状态机管理。默认合法路径为：Definition → Argument Building → Argument Refinement → Debate → Closing Statement → Reflection；跳过、回退及其他异常变化必须经过 Stage Transition Rule 判断。

系统必须可解释当前状态：正在讨论什么、处于哪个阶段、哪些输入已形成、是否存在暂停分支、反方挑战了什么、哪些问题尚未解决、当前 Reflection Version 是什么。状态变化不得因用户一句话被默默执行，必须符合 Rule 判断、完成条件与用户确认要求。

# Part 5 MVP Scope（MVP 范围）

## 17. MVP Features（MVP 能力）

### Prototype Must Have（必须具备）

Agent Runtime Prototype 必须支持用户完成 Definition → Argument Building → Argument Refinement → Debate → Closing Statement → Reflection 的完整思考流程；保持各阶段角色与 Stage Transition 规则；执行忠实于用户主张的反方辩论；保存基础结构化 Memory；生成不可直接编辑的 Reflection 快照；并在同一 Conversation、同一 Topic 的新完整周期结束后生成 Reflection v2+ 与版本比较逻辑。系统须按 Scenario Based Testing 验证行为。

### Prototype Should Have（增强能力）

基础 Runtime 稳定后，可增加 Topic Change 确认、Viewpoint Deepening/Branching 与分支暂存，以及 Reflection Version Comparison Visualization（Reflection Version 展示能力）。这些能力增强路径管理与理解体验，但不改变核心 Agent 行为。

MVP 的成功不以用户是否改变观点衡量，而以用户能否完成一个由自己主导、边界清晰、论证可见、挑战有效且可复盘的思考周期衡量。

## 18. Future Features（后续能力）

Web MVP 可在不改变核心 Agent 行为的前提下增加结构化 Session 视图、Argument Map 可视化、阶段进度、分支恢复入口、Reflection 版本对比视图与测试案例执行面板。Full Product 可探索多设备连续性、用户可控的导出与归档、团队讨论模式以及更丰富的可视化，但任何能力不得削弱用户对 Topic、观点和路径的控制权。

**非目标：** 本 PRD 不要求 UI 页面或按钮定义，不指定模型供应商、检索系统、账号体系、商业化方案，也不将“给出正确答案”定义为产品输出。

# Part 6 Acceptance Criteria（验收标准）

## 19. Quality Standards（质量标准）

| 质量维度 | 验收要求 |
|---|---|
| 用户主导性 | AI 不替用户选择立场、决定 Topic、自动推进阶段或宣判辩论胜负 |
| 阶段边界 | Building 不攻击，Refinement 不对抗，Debate 不补论，Closing 不代写，Reflection 不总结或新增洞察 |
| 路由一致性 | 新方向先经过 Topic Change；仍属当前 Topic 后才进入 Viewpoint Change |
| 状态一致性 | 所有阶段变化经 Stage Transition Rule；Workflow 不直接改状态 |
| Memory 一致性 | 有效信息可实时支持对话；阶段完成后保存快照；普通更新不改变 Reflection Version |
| Reflection 完整性 | Record 只记录用户表达的认知状态；v2+ 只来自同 Conversation 内的新完整周期 |
| 对话安全性 | 挑战观点而非用户，不使用人格、能力或智力评价 |

## 20. Test Scenarios（测试场景）

测试采用 Scenario Based Testing，关注“AI 是否按设计行为运行”，而非是否产生固定答案。每个案例包含 Scenario、Expected Behavior 与 Failure Conditions。

1. **Definition 边界测试：** 用户提出宽泛且混合的问题；AI 应帮助确定 Core Question、Scope 与 Criteria，不能直接给结论。
2. **Building 所有权测试：** 用户没有立场；AI 应提问或允许“尚未形成”，不能代用户选择观点。
3. **Refinement/ Debate 边界测试：** Refinement 应帮助澄清假设；Debate 应以反方挑战相同假设，但不得替用户修复论证。
4. **真实主张测试：** 用户作出概率或范围判断；反方应攻击其条件和标准，不得改写为绝对命题。
5. **Topic/ Viewpoint 路由测试：** 新内容先判断是否服务 Core Question；相关新角度进入 Branching，深层条件进入 Deepening，不相关新问题走 Topic Switching 确认。
6. **Transition 测试：** 正常六阶段流程需要确认；用户跳过时检查最低输入；仅允许用户主动 Debate → Refinement 回退。
7. **Memory 测试：** Debate 中的新回应即时可用；各阶段完成后生成对应 Snapshot；切换 Topic 后旧 Memory 不加载。
8. **Reflection 生命周期测试：** Reflection 完成后补充一句话不得修改当前 Record；用户继续同一 Topic 时必须重新完成完整周期后才生成 v2+。
9. **Full Session 测试：** 从 Topic 到 Reflection 完成全流程，验证状态、Memory、挑战、结辩与 Reflection Record 的一致性。

## Release Gate（发布门槛）

在 Agent Runtime Prototype 进入 Web MVP 前，所有关键 Scenario 必须可重复验证，且不能出现以下失败：AI 替用户形成核心观点；未经确认改变阶段；将同一 Topic 的角度变化误判为新 Topic；将用户真实主张极端化；在 Debate 中补论；在 Reflection 中写入用户未表达的结论；或因普通 Memory 更新产生新的 Reflection Version。

---

**Document status:** PRD v1.0 baseline. Future revisions should preserve the product principles in SKILL.md and record any behavior change together with its Rule, Workflow, Memory, and test impact.
