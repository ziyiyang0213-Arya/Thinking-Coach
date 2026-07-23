# Thinking Coach Technical Architecture v1.0

**状态：** Agent Runtime Prototype 架构基线

**目标读者：** 产品、AI 工程、后端工程与未来 Web 工程协作者
**依据：** `SKILL.md`、`rules/`、`workflows/`、`tests/README.md` 与 `docs/Thinking-Coach PRD v1.0.md`

## 1. Architecture Overview（整体架构）

Thinking Coach 的 Prototype 先验证“思考系统”而非网页体验。推荐实现为 **Python CLI + OpenAI API + SQLite**：CLI 负责本地交互，Runtime 负责状态、规则与工作流，SQLite 持久化 Conversation History 和结构化状态。系统不应把 LLM 当作状态管理者；LLM 负责在受控上下文中生成阶段内回应与结构化候选，Runtime 是唯一可以提交状态变化的执行者。

```text
CLI
  ↓
Runtime Controller
  ├── Specification Loader (SKILL / Rules / Current Workflow)
  ├── Rule Engine
  ├── Workflow Engine
  ├── LLM Interaction Layer
  └── State & Memory Store (SQLite)
```

Prototype 采用自定义显式状态机，而不依赖 LangGraph。原因是当前六阶段、唯一回退、跳过最低输入、用户确认与 Reflection 新周期规则已经明确；显式状态与可测试的转移表更容易保证行为可解释。未来如出现并行 Agent、复杂异步任务或图式恢复需求，再评估图编排框架。

### 技术边界

| 层 | Prototype 选择 | 职责 |
|---|---|---|
| Runtime | Python 3.12+ | 运行编排、状态变更、错误处理 |
| Interface | CLI | 创建/继续 Conversation、输入消息、显示回应 |
| LLM | OpenAI API，通过 `LLMClient` 抽象 | 语义理解、阶段内引导、结构化候选输出 |
| Persistence | SQLite | Conversation History、结构化 Memory、快照与事件 |
| Validation | Scenario Based Testing | 验证行为而非固定文案 |

非目标：Web UI、账号体系、多用户协作、检索系统、向量数据库、跨 Conversation 记忆和商业化能力。

## 2. Runtime Architecture（运行架构）

Runtime 的单次处理入口应为：`handle_turn(conversation_id, user_input) -> TurnResult`。该接口由 CLI 调用，未来 Web API 也复用同一服务；接口返回用户可见回复、最新状态摘要、是否等待确认及可用下一步，不直接暴露内部 Prompt。

### 单轮处理流程

```text
User Input
  ↓
Load Conversation History + Structured Memory + Workflow State
  ↓
Rule Pipeline: Topic Change → Viewpoint Change → Stage Transition → Memory Update
  ↓
Resolve pending confirmation and permitted state action
  ↓
Load SKILL + always-loaded Rules + current Workflow
  ↓
Call LLM for stage behavior and structured candidate output
  ↓
Validate candidate output and proposed memory facts
  ↓
Persist message, approved state changes, memory updates, and audit event atomically
  ↓
Return TurnResult
```

状态变更分为两类。**候选变更**由用户意图或 LLM 结构化输出提出，不写入最终状态；**批准变更**必须经 Rule Engine、最低输入校验和用户确认后，由 Runtime 提交。模型失败、超时或结构化输出校验失败时，不得改变阶段、Topic、Reflection 或 Memory Snapshot。

### Specification Loading（规范加载）

每轮均可访问系统原则和四类 Rules；只加载当前阶段对应 Workflow。Prototype 可在启动时读取并缓存 Markdown 规范，在每次请求中按需要组装提示词。缓存失效或文件缺失必须显式报错，不得静默退化为无规则对话。

| 始终加载 | 按阶段加载 |
|---|---|
| `SKILL.md`、Topic Change、Viewpoint Change、Stage Transition、Memory | `definition`、`building`、`refinement`、`debate`、`closing` 或 `reflection` 的对应 Workflow |

## 3. Workflow Engine（阶段执行机制）

Workflow Engine 维护一个以 Stage 为键的 Handler Registry。Handler 只负责当前阶段的提示词构造、输入完整性提示、阶段内对话与完成候选信号；它不写数据库、不自行切换阶段，也不绕过 Rule Engine。

```python
Stage = Literal[
    "definition", "building", "refinement",
    "debate", "closing", "reflection",
]

class WorkflowHandler(Protocol):
    stage: Stage
    def build_context(self, context: WorkflowContext) -> str: ...
    def evaluate_output(self, output: LLMOutput) -> WorkflowSignal: ...
```

`WorkflowContext` 至少包含当前 Stage、Core Question、当前结构化 Memory、当前 Cycle 的 Reflection History、必要的 Conversation History 摘要和待确认动作。Definition 负责澄清问题；Building 只帮助组织用户论证；Refinement 保持合作强化；Debate 保持反方压力测试；Closing 只引导用户表达；Reflection 只记录已表达的认知状态。

## 4. Rule Engine（规则判断机制）

Rule Engine 是状态判断层，向 Runtime 返回显式 `RuleDecision`，而不是直接修改状态。每个 Decision 应包含 `action`、`reason`、`requires_confirmation`、`required_inputs` 与 `memory_effects`，用于界面解释、测试断言和审计。

```text
Topic Change Rule
  └── 若不再服务当前 Core Question：创建 Topic Switching 候选并等待确认
Viewpoint Change Rule
  └── 仅在仍属当前 Topic 时：判定 Deepening 或 Branching
Stage Transition Rule
  └── 判定前进、跳过、唯一允许回退或 Reflection 后新周期
Memory Rule
  └── 提交实时状态更新或已确认阶段快照
```

Topic Change 必须先于 Viewpoint Change。用户确认 Topic Switching 后，旧 Conversation 标记结束，新 Conversation 创建新的 Current Topic、Memory Context 与 Definition 状态；不得加载旧 Topic 的 Memory 或 Reflection。用户拒绝切换后，才继续同 Topic 的观点变化判断。

用户确认应建模为 `PendingAction`，例如 `confirm_topic_switch`、`confirm_stage_transition`、`confirm_stage_skip` 或 `confirm_restart_cycle`。待确认期间，Runtime 必须先处理用户对该动作的确认、拒绝或重新表述，不能假设确认已经发生。

## 5. Memory Architecture（记忆存储设计）

Conversation History 与 Memory 必须分离。前者保存完整交互原文以支持审计、回放和必要上下文摘要；后者保存经规则确认的结构化状态，以支持工作流执行与 Reflection。不得将所有聊天文本无差别复制到 Memory。

### 两层更新模型

| 类型 | 触发时机 | 写入内容 | 是否生成版本 |
|---|---|---|---|
| Current State Update | 用户提供有效的新观点、论据、条件、回应或方向 | 当前 Position、Reasoning、Arguments、条件与回应 | 否 |
| Stage Snapshot Update | 阶段完成且用户确认 | 当前阶段稳定产出 | 仅 Reflection 保存 Version |

Snapshot 至少覆盖：Definition 的 Core Question/Scope/Boundary；Building 的 Position/Reasoning/Arguments；Refinement 的 Refined Argument/Assumptions；Debate 的 Challenges/Responses/Remaining Questions；Reflection 的 Record/Version。

Reflection 是不可直接编辑的快照。普通 Memory 更新不修改 Reflection，也不生成新版本；只有同一 Conversation、同一 Topic 重新完成完整六阶段周期后，才创建 Reflection v2+。Topic Switching 不继承任何旧 Reflection History。

## 6. State Management（状态管理）

### 状态机

默认合法路径为：

```text
Definition → Argument Building → Argument Refinement → Debate → Closing Statement → Reflection
```

Stage Transition Rule 是唯一状态控制者。用户可以请求跳过阶段，但目标阶段必须通过最低输入校验；唯一允许的回退是用户主动请求的 `Debate → Argument Refinement`。Reflection 后不自动前进：用户可完成 Topic，或在同一 Conversation、同一 Topic 内从 Definition 开启新 Cycle。

### 最小状态对象

```python
class WorkflowState(BaseModel):
    current_stage: Stage
    stage_status: Literal["active", "awaiting_confirmation", "completed"]
    pending_action: PendingAction | None
    cycle_number: int

class ConversationState(BaseModel):
    conversation_id: str
    status: Literal["active", "topic_completed", "closed"]
    current_topic_id: str
    workflow: WorkflowState
```

每一次已批准的状态变化必须记录为不可变 `StateEvent`，包含前后状态、触发者、适用 Rule、理由与时间。事件日志用于恢复、排障和 Scenario Test 断言，而不是代替结构化 Memory。

## 7. LLM Interaction Layer（模型调用层）

`LLMClient` 应隔离 OpenAI SDK 细节，最小接口为 `generate(messages, response_schema) -> LLMOutput`。初期使用单一模型配置和环境变量注入 API Key；模型名、超时、最大输出长度和重试次数放入独立配置，不写死在 Workflow 中。

调用上下文由 Runtime 构造，按以下优先级组装：产品原则、全局 Rules 摘要、当前 Workflow 规范、当前结构化 Memory、必要的 History 摘要、当前用户输入和 PendingAction。模型必须返回可校验的结构化 Envelope：`assistant_message`、`extracted_facts`、`workflow_signal`、`proposed_actions`。Runtime 只接受通过 Schema 与 Rule 校验的字段；用户可见回复应在校验通过后返回。

模型调用失败时保留原状态，并返回可重试的系统提示。结构化输出不合法时可进行一次受限修复调用；再次失败则不持久化任何候选事实或状态变更。日志默认记录请求 ID、阶段、规则决策、模型配置与错误类型，避免在调试日志中无必要地复制用户原文。

## 8. Data Model（数据结构）

Prototype 采用 Pydantic 模型定义运行时数据，并以 SQLite 存储。可变的细粒度思考内容使用 JSON 字段，稳定的生命周期对象使用独立表；这样可以先验证 Agent 行为，后续再迁移为更严格的关系模型。

| 实体 | 关键字段 | 用途 |
|---|---|---|
| Conversation | `id`、`status`、`created_at`、`closed_at` | 独立思考空间与生命周期 |
| Message | `id`、`conversation_id`、`role`、`content`、`created_at` | 完整 Conversation History |
| Topic | `id`、`conversation_id`、`core_question`、`scope`、`criteria` | 当前 Topic 定义 |
| WorkflowState | `conversation_id`、`current_stage`、`pending_action`、`cycle_number` | 当前状态机位置 |
| MemoryState | `conversation_id`、`thinking_json`、`arguments_json`、`branches_json` | 结构化实时状态 |
| StageSnapshot | `id`、`conversation_id`、`stage`、`cycle_number`、`data_json` | 已确认阶段快照 |
| ReflectionRecord | `id`、`conversation_id`、`version`、`cycle_number`、`data_json` | 不可编辑的 Reflection 快照 |
| StateEvent | `id`、`conversation_id`、`event_type`、`payload_json` | 状态变更审计与测试证据 |

`Conversation` 与 `Topic` 在 Prototype 中保持一对一的有效生命周期：确认 Topic Switching 时关闭旧 Conversation 并创建新 Conversation，而不是复用旧 Conversation 写入多个 Topic。

## 9. Prototype Implementation Plan（Prototype 开发范围）

实现应按风险由高到低推进：

1. **Foundation**：建立 Python 项目、配置加载、SQLite 连接、Pydantic 数据模型与 CLI 骨架。
2. **State Core**：实现 Conversation/WorkflowState、默认状态机、PendingAction、原子持久化与 StateEvent。
3. **Specification Runtime**：实现 Markdown 规范加载、Workflow Registry、RuleDecision 与 Prompt Context Builder。
4. **Core Experience**：依次实现 Definition、Building、Refinement、Debate、Closing、Reflection，并接入结构化 LLM 输出校验。
5. **Memory and Versioning**：实现实时状态、阶段快照、Reflection v1/v2+ 与同 Conversation 的比较数据。
6. **Enhancements**：实现 Topic Switching、Deepening/Branching、Parked Branch，以及版本展示所需的读取模型。
7. **Scenario Harness**：把 `tests/README.md` 的 Scenario、Expected Behavior、Failure Conditions 转换为可重复执行的测试夹具与断言。

在第 4 步完成前，不实现 Web UI；在第 7 步通过关键场景前，不开始 Web MVP。

## 10. Future Web Architecture（未来 Web 扩展方向）

Web MVP 应将已验证的 Runtime 作为无界面核心，而不是将 Workflow、Rules 或 Memory 逻辑重写在前端。建议未来结构为：Web Client 通过 HTTP/streaming API 调用 `RuntimeService.handle_turn`；服务层管理身份、Session 列表与访问控制；Runtime 继续拥有状态机、规则、Memory 和 LLM 调用；数据库层在需要多用户与并发时从 SQLite 迁移至 PostgreSQL。

前端仅展示当前 Stage、待确认动作、Conversation History、结构化 Argument Map、Reflection History 和 Version Comparison Visualization。前端不得根据按钮点击自行改变 Stage 或 Topic；所有状态请求仍由 Runtime 的 Rule Engine 裁决。

## 11. Acceptance and Test Strategy（验收与测试策略）

每项实现均须对照现有 Scenario Based Testing。至少覆盖：正常六阶段流程；未确认不得自动推进；跳过的最低输入校验；Debate 到 Refinement 的唯一回退；Topic Change 先于 Viewpoint Change；Debate 忠实攻击真实主张；实时 Memory 与 Snapshot 的边界；Reflection 不可直接编辑；同 Conversation 新 Cycle 产生 v2+；Topic Switching 不继承旧 Memory 或 Reflection。

Prototype 的完成标准不是生成固定措辞，而是每个 Scenario 都能验证正确的 RuleDecision、状态事件、结构化 Memory 和用户控制权。
