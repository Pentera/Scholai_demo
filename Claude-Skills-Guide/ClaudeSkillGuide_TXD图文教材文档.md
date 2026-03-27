## 基本信息

| 字段 | 内容 |
|------|------|
| **关联 IOD** | ClaudeSkillGuide_IOD教学目标文档.md |
| **关联 PD** | ClaudeSkillGuide_PD教学法文档.md |

# The Complete Guide to Building Skills for Claude

**学完本课，你将能回答：**
• Skill 的基本构成是什么？它遵循哪些核心设计原则？
• 如何定义具体的技能用例触发条件与步骤？
• 如何执行规范的文件结构搭建，并编写准确的 YAML 和 Markdown？
• 如何验证技能的触发准确率与功能完整性？
• 如何运用高级架构模式设计复杂的技能指令结构？

---

## 第一部分：基础概念与原理导入——理解技能与MCP的协同

技能（Skill）是一个包含了指令的简单文件夹，它教会 Claude 如何处理特定的任务或工作流。通过技能，你无需在每次对话中重复解释你的偏好、流程和领域专业知识，而是教 Claude 一次，之后每次都能直接受益。

一个标准的技能文件夹通常包含必须的 `SKILL.md`（带有 YAML Frontmatter 的 Markdown 指令），以及可选的 `scripts/`（可执行代码）、`references/`（参考文档）和 `assets/`（模板、资产）。

在设计技能时，一个非常重要的原则是“渐进式披露（Progressive Disclosure）”。记住：**“三个层级，按需加载”**。不要把所有指令塞给 Claude，正确做法是通过首层的 YAML 元数据让 Claude 知道何时触发，次层的 Markdown 主体提供完整指令，第三层级的参考文件仅在需要时去读取。

对于正在构建 MCP（模型上下文协议）集成的开发者来说，技能提供了在其之上的一层强大的知识抽象。为了更清楚地理解这一点，来看一个具体的类比：

【概念类比】厨房类比模型

MCP provides the professional kitchen: access to tools, ingredients, and equipment. Skills provide the recipes: step-by-step instructions on how to create something valuable.

[图：左侧显示 MCP 抽象为厨房（包含锅碗瓢盆和食材），右侧显示 Skill 抽象为菜谱（包含分步的烹饪指南）]

**类比解析**：
打个比方：**“将 MCP 比作提供工具和原料的专业厨房，将 Skill 比作菜谱”**。没有技能时，用户面对一堆 API 工具往往不知道下一步该做什么；有了技能，预设的业务工作流就能在需要时自动激活，提供一致且可靠的最佳实践。

理解了基本概念和定位之后，我们来看如何规划一个具体的技能场景。

---

## 第二部分：规划与规范设计——从构思到文件落地

在编写任何代码之前，你需要先明确 2 到 3 个具体的用例。你需要问自己：用户想完成什么？需要哪些多步工作流？需要哪些内置工具或 MCP？必须嵌入哪些最佳实践？

一个清晰的用例必须包含触发词（Trigger）、拆解步骤（Steps）以及预期结果（Result）。简单来说：**“写代码前，先定义触发词、步骤和预期结果”**。

下面通过一个具体情境来分析：

【用例分析】项目 Sprint 规划用例

Use Case: Project Sprint Planning
Trigger: User says "help me plan this sprint" or "create sprint tasks"
Steps: 1. Fetch current project status from Linear (via MCP); 2. Analyze team velocity and capacity; 3. Suggest task prioritization; 4. Create tasks in Linear with proper labels and estimates.
Result: Fully planned sprint with tasks created.

**解析步骤**：
1. 明确用户的触发语句（如 "help me plan this sprint"）。
2. 将操作拆分为获取数据、逻辑分析、优先级排序和最终写入工具四步。
3. 设定预期结果为“带有任务的完整 Sprint 计划”。

再来看另一个总结性的情况。在 Anthropic 团队的实战中，我们观察到技能通常分为三大类：

【概念演示】三大技能类别实例

Category 1: frontend-design skill (Document & Asset Creation).
Category 2: skill-creator skill (Workflow Automation). 
Category 3: sentry-code-review skill (MCP Enhancement).

**分类逻辑**：
这三类分别代表了：仅依赖原生能力生成规范资产（如前端设计技能）、多步骤的方法论自动化（如技能创建向导）、以及强化特定 MCP 的工具调用逻辑（如 Sentry 代码审查）。记住：**“如果需要外部系统数据，立刻想到它属于 Category 3: MCP Enhancement”**。

有了清晰的用例，我们需要定义怎么才算“好”。

【评估标准】成功标准度量

Quantitative metrics: Skill triggers on 90% of relevant queries; Completes workflow in X tool calls; 0 failed API calls per workflow.
Qualitative metrics: Users don't need to prompt Claude about next steps; Workflows complete without user correction; Consistent results across sessions.

**评估指标体系**：
判断技能好坏，一个实用的口诀是：**“定量的 API 成功率与定性的用户免干预率”**。我们需要同时关注机器视角的数据（0 报错）和人类视角的体验（无需纠正）。容易犯的错误是**“没有明确衡量标准，全凭感觉”**，正确做法是结合这些定量与定性指标。

有了目标和评估标准，现在可以进入代码实现阶段。

技能的核心文件是 `SKILL.md`。请注意文件命名的绝对规范：必须是 kebab-case（如 `my-cool-skill`），记住：**“文件夹命名绝对不能有空格”**。

最重要的部分是文件头部的 YAML Frontmatter，这是 Claude 决定是否加载你技能的唯一依据。你需要在这段 1024 字符以内的描述里做到极致的精准。

【方法示范】YAML Frontmatter 编写示范

Good: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".
Bad: Helps with projects.

**正确写法分解**：
1. 包含功能说明（Analyzes Figma...）
2. 包含具体的触发原话（asks for "design specs"...）

在编写描述时，记住：**“公式：What it does + When to use it”**。容易犯的错误是**“在 YAML 中使用 XML 标签 (< >)”**，绝对禁止，因为这是系统提示词注入口，有安全限制。同时也要避免**“描述里全是技术术语，缺乏口语化短语”**。

配置好 YAML 后，接下来是 Markdown 主体的编写。

【结构示范】Markdown 主体指令模板

```markdown
# Your Skill Name
## Instructions
### Step 1: [First Major Step]
...
## Examples
### Example 1: [common scenario]
...
## Troubleshooting
```

**结构说明**：
一个标准的技能主体包含三大块：操作步骤（Instructions）、案例参考（Examples）和排障指南（Troubleshooting）。记住：**“写 Markdown 主体，三大块：步骤、案例、排错”**。

---

## 第三部分：测试、迭代与分发——验证你的技能

技能开发完成后，不能盲目发布，必须进行测试。测试分为触发测试、功能测试和性能对比。

对于触发测试，我们需要构造正向和负向样本：

【边界测试】技能触发测试用例

Should trigger: "Help me set up a new ProjectHub workspace", "I need to create a project in ProjectHub"
Should NOT trigger: "What's the weather in San Francisco?", "Create a spreadsheet"

**测试方法**：
既要测试它该触发的时候触发，也要测试它不该触发的时候闭嘴。这就像**“安检的白名单测试，拒绝无关内容”**。

如果在测试中发现问题，可以通过“症状驱动排错法”来解决。比如当你发现技能“欠触发（Undertriggering）”时，记住：**“补充更多具体的业务关键词”**。相反如果过触发，则需要在描述中增加负向排除语句（Do NOT use for...）。容易犯的错误是**“一上来就做庞大的自动化测试集”**，正确做法是先在单个高难度任务上跑通并抽取成功经验。

---

## 第四部分：高级架构模式解析——解决复杂业务需求

当面对更复杂的业务需求时，基础的单线指令可能不够用。这里为你总结了 5 种高级技能架构模式。

【架构实例】5 种高级模式整合

**Pattern 1: Sequential workflow orchestration**
Workflow: Onboard New Customer
Step 1: Create Account -> Step 2: Setup Payment -> Step 3: Create Subscription -> Step 4: Send Welcome Email

**Pattern 2: Multi-MCP coordination**
Phase 1: Design Export (Figma MCP) -> Phase 2: Asset Storage (Drive MCP) -> Phase 3: Task Creation (Linear MCP) -> Phase 4: Notification (Slack MCP)

**Pattern 3: Iterative refinement**
Initial Draft -> Quality Check (Run validation script) -> Refinement Loop (Address issues, Re-validate) -> Finalization

**Pattern 4: Context-aware tool selection**
Decision Tree: Check file type and size -> >10MB to Cloud MCP, collaborative to Notion MCP, code to GitHub MCP -> Execute Storage.

**Pattern 5: Domain-specific intelligence**
Before Processing (Compliance Check): Fetch details -> Apply compliance rules (sanctions, jurisdiction, risk) -> IF passed: Process transaction ELSE: Flag for review.

[图：展示五种模式的流程图简图，从线性的 Pattern 1 到带有循环的 Pattern 3 以及带决策树的 Pattern 4]

**模式选择指南**：
- 如果你需要把上一步的结果传给下一步，记住：**“使用 Pattern 1 或 Pattern 2，明确定义参数传递逻辑”**。
- 如果生成的初稿质量差，记住：**“引入 Pattern 3 (Refinement Loop) 自动化校验脚手架”**。
- 如果你的工作流涉及高风险动作（如支付），记住：**“使用 Pattern 5，在执行前插入领域知识拦截”**。
- 容易犯的错误是**“依赖自然语言让 LLM 自己判断分支”**，正确做法是提供明确的 If-Else 决策树（Pattern 4）。

---

## 本课总结

### 核心要点
• Skill 的定义与核心设计原则（渐进式披露、可组合性、可移植性）
• 用例定义方法与常见类别（资产生成、流程自动化、MCP增强）
• SKILL.md 的技术规范（文件命名、YAML Frontmatter 规则与 Markdown 结构）
• 技能的测试方法（触发测试、功能测试、性能对比）与迭代策略
• 常见的高级架构模式（顺序流、跨系统、循环优化、动态路由、规则封装）

### 易错提醒
• 警告：直接将所有指令塞给 Claude。正确做法是通过渐进式披露按需加载。
• 警告：没有明确衡量标准，全凭感觉。正确做法是结合定量与定性指标。
• 警告：在 YAML 中使用 XML 标签 (< >)。这是系统提示词注入口，有严格安全限制。
• 警告：描述里全是技术术语。正确做法是必须包含用户触发时会说的口语化短语。
• 警告：一上来就做庞大的自动化测试集。正确做法是先在单个高难度任务上跑通并抽取经验。
• 警告：依赖自然语言让 LLM 自己判断分支。正确做法是提供明确的 If-Else 决策树。

### 知识应用范围
本课内容适用于评估是否需要为特定任务构建 Skill，在设计初期确立正确的架构思路，梳理自动化工作流的需求指标。同时适用于编写任何基于文本指令驱动的 LLM 配置文件、提示词模板、复杂的 Agent 编排逻辑或多工具协同的工作流架构。也可用于评估 AI 代理提示词的稳健性。