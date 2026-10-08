# -*- coding: utf-8 -*-
"""
Phase 2: 角色技能包 - 批量新增积木

按调研员报告的候选清单，为6个角色补缺新积木。
优先级：tester(0个) > pm > researcher > designer > marketer > developer
"""

import json
import os
from datetime import datetime

BLOCKS_PATH = 'D:/jieyuexingchen/promptblocks/blocks.json'

# 新增积木定义
# 每个积木包含完整的15字段（9原有+6标准化）
NEW_BLOCKS = [
    # ═══ 测试员积木包 (8个, 当前0个) ═══
    {
        "category": "task",
        "block": {
            "id": "task-test-scope",
            "title": "测试范围定义",
            "content": "请根据以下功能需求，定义测试范围。列出需要测试的功能模块、测试类型（功能/边界/异常/性能）、测试优先级、不测试的内容及原因。输出一份结构化测试范围文档。",
            "tags": ["测试", "范围", "计划"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Test Scope Definition",
            "contentEn": "Based on the following feature requirements, define the test scope. List functional modules to test, test types (functional/boundary/exception/performance), test priorities, and items excluded from testing with reasons. Output a structured test scope document.",
            "agentRole": "tester",
            "inputs": "功能需求文档或需求描述",
            "prerequisites": "已明确功能需求和验收标准",
            "outputFormat": "report",
            "qualityChecks": ["测试范围是否覆盖所有核心功能", "是否标注了不测试项及原因", "优先级是否合理", "测试类型是否全面"],
            "recommendedWith": ["task-acceptance-criteria", "task-test-case"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-test-case",
            "title": "测试用例生成",
            "content": "请根据以下功能描述，生成完整的测试用例。每个用例包含：用例编号、前置条件、测试步骤、预期结果、实际结果（留空）、优先级（P0/P1/P2）。覆盖正常流程、边界条件和异常场景。",
            "tags": ["测试", "用例", "质量"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Test Case Generation",
            "contentEn": "Based on the following feature description, generate complete test cases. Each case includes: case ID, preconditions, test steps, expected result, actual result (blank), and priority (P0/P1/P2). Cover normal flows, boundary conditions, and exception scenarios.",
            "agentRole": "tester",
            "inputs": "功能描述和测试范围",
            "prerequisites": "已定义测试范围",
            "outputFormat": "table",
            "qualityChecks": ["用例是否覆盖正常/边界/异常", "步骤是否可重复执行", "预期结果是否可验证", "优先级是否合理"],
            "recommendedWith": ["task-test-scope", "task-bug-repro"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-boundary-analysis",
            "title": "边界条件分析",
            "content": "请对以下功能进行边界值分析。找出所有输入参数的边界值（最小值、最大值、临界值、空值、超长值、特殊字符），列出每个边界条件的测试点和预期行为。",
            "tags": ["测试", "边界", "健壮性"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Boundary Condition Analysis",
            "contentEn": "Perform boundary value analysis on the following feature. Identify boundary values for all input parameters (min, max, critical, empty, overflow, special characters), and list test points and expected behavior for each boundary condition.",
            "agentRole": "tester",
            "inputs": "功能描述和输入参数",
            "prerequisites": "已明确功能输入范围",
            "outputFormat": "table",
            "qualityChecks": ["边界值是否全面", "是否考虑了空值和特殊字符", "预期行为是否明确", "是否有遗漏的边界场景"],
            "recommendedWith": ["task-test-case", "task-exception-flow"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-exception-flow",
            "title": "异常流程分析",
            "content": "请分析以下功能的异常处理流程。列出所有可能的异常场景（网络超时、权限不足、数据不存在、并发冲突、格式错误等），对每个异常场景给出：触发条件、系统行为、用户提示、恢复方式。",
            "tags": ["测试", "异常", "容错"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Exception Flow Analysis",
            "contentEn": "Analyze exception handling flows for the following feature. List all possible exception scenarios (network timeout, insufficient permissions, data not found, concurrency conflict, format error, etc.), and for each: trigger condition, system behavior, user message, and recovery method.",
            "agentRole": "tester",
            "inputs": "功能描述和系统架构",
            "prerequisites": "已了解系统架构和依赖",
            "outputFormat": "table",
            "qualityChecks": ["异常场景是否全面", "恢复方式是否可行", "用户提示是否友好", "是否有遗漏的异常路径"],
            "recommendedWith": ["task-boundary-analysis", "task-test-case"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-bug-repro",
            "title": "Bug复现步骤",
            "content": "请将以下Bug描述转化为标准复现步骤。包含：环境信息（系统/浏览器/版本）、前置条件、复现步骤（编号）、预期结果、实际结果、严重程度（致命/严重/一般/轻微）、优先级、截图说明。",
            "tags": ["测试", "Bug", "复现"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Bug Reproduction Steps",
            "contentEn": "Convert the following bug description into standard reproduction steps. Include: environment info (system/browser/version), preconditions, numbered reproduction steps, expected result, actual result, severity (fatal/serious/minor/cosmetic), priority, and screenshot description.",
            "agentRole": "tester",
            "inputs": "Bug描述和相关信息",
            "prerequisites": "已收到Bug报告",
            "outputFormat": "report",
            "qualityChecks": ["复现步骤是否可重复", "环境信息是否完整", "严重程度是否准确", "预期与实际是否区分清楚"],
            "recommendedWith": ["task-test-case", "task-regression-list"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-regression-list",
            "title": "回归测试清单",
            "content": "请根据以下变更内容，生成回归测试清单。分析变更影响范围，列出需要回归测试的功能点、测试优先级、是否需要全量回归。输出检查清单格式，每项可标记通过/未通过/不适用。",
            "tags": ["测试", "回归", "清单"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Regression Test Checklist",
            "contentEn": "Based on the following changes, generate a regression test checklist. Analyze the impact scope, list functional points requiring regression testing, test priority, and whether full regression is needed. Output in checklist format with pass/fail/N/A markers.",
            "agentRole": "tester",
            "inputs": "变更内容和影响范围",
            "prerequisites": "已了解代码变更内容",
            "outputFormat": "checklist",
            "qualityChecks": ["影响范围分析是否准确", "回归项是否完整", "优先级是否合理", "清单格式是否可执行"],
            "recommendedWith": ["task-test-case", "task-test-report"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-api-test",
            "title": "API测试设计",
            "content": "请为以下API接口设计测试方案。覆盖：正常请求（200）、参数缺失（400）、权限不足（403）、资源不存在（404）、服务器错误（500）、边界值、并发请求、幂等性测试。每个测试点给出请求参数和预期响应。",
            "tags": ["测试", "API", "接口"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "API Test Design",
            "contentEn": "Design a test plan for the following API endpoint. Cover: normal request (200), missing parameters (400), insufficient permissions (403), resource not found (404), server error (500), boundary values, concurrent requests, and idempotency. Provide request parameters and expected response for each test point.",
            "agentRole": "tester",
            "inputs": "API文档和接口定义",
            "prerequisites": "已有API文档",
            "outputFormat": "table",
            "qualityChecks": ["是否覆盖所有HTTP状态码", "并发和幂等性是否测试", "参数边界是否考虑", "预期响应是否明确"],
            "recommendedWith": ["task-test-case", "task-boundary-analysis"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-test-report",
            "title": "测试报告",
            "content": "请根据以下测试执行结果，生成标准测试报告。包含：测试概况（范围/时间/环境）、执行结果统计（用例总数/通过/失败/阻塞/通过率）、缺陷统计（按严重程度分布）、风险评估、测试结论（通过/有条件通过/不通过）和建议。",
            "tags": ["测试", "报告", "总结"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Test Report",
            "contentEn": "Based on the following test execution results, generate a standard test report. Include: test overview (scope/time/environment), execution statistics (total/pass/fail/blocked/pass rate), defect statistics (by severity), risk assessment, test conclusion (pass/conditional pass/fail), and recommendations.",
            "agentRole": "tester",
            "inputs": "测试执行结果和缺陷列表",
            "prerequisites": "测试执行已完成",
            "outputFormat": "report",
            "qualityChecks": ["统计数据是否准确", "风险评估是否合理", "结论是否有依据", "建议是否可执行"],
            "recommendedWith": ["task-regression-list", "task-bug-repro"]
        }
    },

    # ═══ PM积木包 (6个新增) ═══
    {
        "category": "task",
        "block": {
            "id": "task-prd",
            "title": "PRD生成",
            "content": "请根据以下需求信息，生成完整的产品需求文档（PRD）。包含：需求背景与目标、目标用户、使用场景、功能需求列表（按优先级排序）、非功能需求（性能/安全/可用性）、交互流程、数据指标定义、验收标准、发布计划。",
            "tags": ["PM", "PRD", "需求"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "PRD Generation",
            "contentEn": "Based on the following requirement information, generate a complete Product Requirements Document (PRD). Include: background and goals, target users, use cases, feature requirements (sorted by priority), non-functional requirements (performance/security/usability), interaction flows, data metrics, acceptance criteria, and release plan.",
            "agentRole": "pm",
            "inputs": "需求描述和用户反馈",
            "prerequisites": "已完成需求调研和竞品分析",
            "outputFormat": "report",
            "qualityChecks": ["需求是否可验证", "优先级是否合理", "非功能需求是否完整", "验收标准是否可量化"],
            "recommendedWith": ["task-requirements-clarify", "task-competitive-analysis"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-competitive-analysis",
            "title": "竞品分析",
            "content": "请对以下产品进行竞品分析。从6个维度对比：核心功能、目标用户、商业模式、技术方案、用户体验、市场表现。输出竞品矩阵表格，并给出差异化机会和可借鉴的具体功能点。",
            "tags": ["PM", "竞品", "分析"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Competitive Analysis",
            "contentEn": "Conduct competitive analysis on the following products. Compare across 6 dimensions: core features, target users, business model, technical approach, user experience, and market performance. Output a competitive matrix table, and identify differentiation opportunities and specific features worth adopting.",
            "agentRole": "pm",
            "inputs": "竞品名称和分析重点",
            "prerequisites": "已收集竞品基本信息",
            "outputFormat": "table",
            "qualityChecks": ["对比维度是否全面", "数据是否准确", "差异化机会是否有依据", "建议是否可执行"],
            "recommendedWith": ["task-prd", "task-user-interview"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-user-interview",
            "title": "用户访谈提纲",
            "content": "请根据以下研究目标，生成用户访谈提纲。包含：访谈目的、目标受访者画像、预热问题（3个）、核心问题（按主题分组，每组3-5个）、深入追问策略、结束语。问题应为开放式，避免引导性提问。",
            "tags": ["PM", "用户研究", "访谈"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "User Interview Outline",
            "contentEn": "Based on the following research objective, generate a user interview outline. Include: interview purpose, target respondent profile, warm-up questions (3), core questions (grouped by theme, 3-5 per group), follow-up probing strategies, and closing remarks. Questions should be open-ended and avoid leading questions.",
            "agentRole": "pm",
            "inputs": "研究目标和用户群体",
            "prerequisites": "已明确研究目标",
            "outputFormat": "list",
            "qualityChecks": ["问题是否开放式", "是否有引导性提问", "逻辑是否递进", "覆盖面是否全面"],
            "recommendedWith": ["task-competitive-analysis", "task-prd"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-metric-design",
            "title": "指标设计",
            "content": "请为以下产品目标设计数据指标体系。区分北极星指标、核心指标、辅助指标。每个指标包含：名称、定义、计算公式、数据来源、目标值、监测频率。确保指标符合SMART原则（可量化、可达成、相关性、时限性）。",
            "tags": ["PM", "指标", "数据"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Metric Design",
            "contentEn": "Design a data metrics system for the following product goals. Distinguish between North Star metric, core metrics, and auxiliary metrics. Each metric includes: name, definition, calculation formula, data source, target value, and monitoring frequency. Ensure metrics follow SMART principles (Specific, Measurable, Achievable, Relevant, Time-bound).",
            "agentRole": "pm",
            "inputs": "产品目标和业务场景",
            "prerequisites": "已明确产品目标",
            "outputFormat": "table",
            "qualityChecks": ["指标是否符合SMART", "北极星指标是否聚焦", "数据来源是否可行", "监测频率是否合理"],
            "recommendedWith": ["task-prd", "task-release-plan"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-release-plan",
            "title": "发布计划",
            "content": "请根据以下功能需求和优先级，制定发布计划。包含：版本规划（v1.0/v1.1/v2.0）、每版本功能列表、里程碑时间线、资源需求、风险依赖项、灰度策略、回滚方案。",
            "tags": ["PM", "发布", "计划"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Release Plan",
            "contentEn": "Based on the following feature requirements and priorities, create a release plan. Include: version planning (v1.0/v1.1/v2.0), feature list per version, milestone timeline, resource requirements, risk dependencies, gradual rollout strategy, and rollback plan.",
            "agentRole": "pm",
            "inputs": "功能需求列表和优先级",
            "prerequisites": "已完成PRD和优先级排序",
            "outputFormat": "report",
            "qualityChecks": ["版本规划是否合理", "时间线是否可行", "风险是否识别", "回滚方案是否完善"],
            "recommendedWith": ["task-prd", "task-metric-design"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-retrospective",
            "title": "复盘报告",
            "content": "请根据以下项目或迭代结果，生成复盘报告。包含：目标回顾（原定目标vs实际结果）、亮点（做得好的3件事）、不足（需要改进的3件事）、根因分析（对每个不足用5Why分析）、行动项（具体改进行动、负责人、截止时间）。",
            "tags": ["PM", "复盘", "改进"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Retrospective Report",
            "contentEn": "Based on the following project or iteration results, generate a retrospective report. Include: goal review (original vs actual), highlights (3 things done well), issues (3 things to improve), root cause analysis (5 Why for each issue), and action items (specific improvements, owner, deadline).",
            "agentRole": "pm",
            "inputs": "项目结果和过程数据",
            "prerequisites": "项目或迭代已完成",
            "outputFormat": "report",
            "qualityChecks": ["目标对比是否客观", "根因分析是否深入", "行动项是否可执行", "是否有负责人和截止时间"],
            "recommendedWith": ["task-release-plan", "task-metric-design"]
        }
    },

    # ═══ 调研员积木包 (5个新增) ═══
    {
        "category": "task",
        "block": {
            "id": "task-search-plan",
            "title": "搜索计划",
            "content": "请根据以下调研目标，制定搜索计划。列出：搜索关键词组合（中英文）、搜索平台（GitHub/Google Scholar/Product Hunt/HN）、搜索范围（时间/语言/领域）、预期产出、筛选标准（star数/引用数/更新频率）。",
            "tags": ["调研", "搜索", "计划"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Search Plan",
            "contentEn": "Based on the following research objective, create a search plan. List: keyword combinations (Chinese/English), search platforms (GitHub/Google Scholar/Product Hunt/HN), search scope (time/language/domain), expected output, and filtering criteria (stars/citations/update frequency).",
            "agentRole": "researcher",
            "inputs": "调研目标和关键词",
            "prerequisites": "已明确调研目标",
            "outputFormat": "list",
            "qualityChecks": ["关键词是否全面", "平台选择是否合理", "筛选标准是否可量化", "是否有中英文覆盖"],
            "recommendedWith": ["task-source-credibility", "task-competitive-analysis"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-source-credibility",
            "title": "来源可信度评分",
            "content": "请对以下信息来源进行可信度评分。从5个维度评估：权威性（作者/机构资质）、时效性（发布/更新时间）、客观性（是否有利益偏向）、可验证性（是否有数据支撑）、完整性（是否覆盖多角度）。每维度0-5分，输出总分和可信度等级（高/中/低）。",
            "tags": ["调研", "可信度", "验证"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Source Credibility Scoring",
            "contentEn": "Score the credibility of the following information sources. Evaluate across 5 dimensions: authority (author/institution credentials), timeliness (publication/update date), objectivity (potential bias), verifiability (data support), and completeness (multi-perspective coverage). Score each 0-5, output total score and credibility level (high/medium/low).",
            "agentRole": "researcher",
            "inputs": "信息来源URL或内容",
            "prerequisites": "已收集信息来源",
            "outputFormat": "table",
            "qualityChecks": ["评分维度是否全面", "评分是否有依据", "可信度等级是否合理", "是否区分了事实与观点"],
            "recommendedWith": ["task-search-plan", "task-fact-separation"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-fact-separation",
            "title": "事实与推测分离",
            "content": "请将以下内容中的信息分为三类：已验证事实（有数据/引用支撑）、合理推测（基于逻辑推断但无直接证据）、待验证假设（需要进一步调研确认）。对每类信息标注来源和可信度，重点标出可能被误读为事实的推测。",
            "tags": ["调研", "事实核查", "分析"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Fact-Speculation Separation",
            "contentEn": "Categorize information in the following content into three types: verified facts (supported by data/citations), reasonable speculation (logical inference without direct evidence), and unverified hypotheses (requiring further research). Tag each with source and credibility, highlighting speculations that might be misread as facts.",
            "agentRole": "researcher",
            "inputs": "待分析的内容或报告",
            "prerequisites": "已收集相关资料",
            "outputFormat": "table",
            "qualityChecks": ["分类是否准确", "来源标注是否完整", "推测是否被正确识别", "待验证项是否有后续计划"],
            "recommendedWith": ["task-source-credibility", "task-research-conclusion"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-market-scan",
            "title": "市场扫描",
            "content": "请对以下领域进行市场扫描。分析：市场规模（TAM/SAM/SOM）、增长趋势、竞争格局（头部玩家/长尾）、用户需求痛点、技术趋势、政策影响。输出市场地图，标注机会区间和风险区间。",
            "tags": ["调研", "市场", "趋势"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Market Scan",
            "contentEn": "Conduct a market scan on the following domain. Analyze: market size (TAM/SAM/SOM), growth trends, competitive landscape (top players/long tail), user pain points, technology trends, and policy impact. Output a market map with opportunity zones and risk zones.",
            "agentRole": "researcher",
            "inputs": "目标领域和市场范围",
            "prerequisites": "已明确调研领域",
            "outputFormat": "report",
            "qualityChecks": ["市场规模是否有依据", "竞争格局是否准确", "趋势判断是否合理", "机会和风险是否标注清楚"],
            "recommendedWith": ["task-competitive-analysis", "task-search-plan"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-research-conclusion",
            "title": "研究结论与建议",
            "content": "请根据以下调研数据，输出研究结论。结构为：核心发现（3-5条关键结论，每条附数据支撑）、风险提示、行动建议（按优先级排序，每条建议附预期收益和实施难度）、后续调研方向。确保结论与数据对应，不过度推断。",
            "tags": ["调研", "结论", "建议"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Research Conclusion",
            "contentEn": "Based on the following research data, output research conclusions. Structure: key findings (3-5 major conclusions, each with data support), risk alerts, action recommendations (sorted by priority, each with expected benefit and implementation difficulty), and follow-up research directions. Ensure conclusions match data without over-inference.",
            "agentRole": "researcher",
            "inputs": "调研数据和分析结果",
            "prerequisites": "已完成数据收集和分析",
            "outputFormat": "report",
            "qualityChecks": ["结论是否有数据支撑", "建议是否有可操作性", "风险是否识别", "是否避免过度推断"],
            "recommendedWith": ["task-fact-separation", "task-market-scan"]
        }
    },

    # ═══ 设计师积木包 (4个新增) ═══
    {
        "category": "task",
        "block": {
            "id": "task-user-journey",
            "title": "用户旅程图",
            "content": "请根据以下产品功能，绘制用户旅程图。按阶段列出：用户目标、触点、行为、情绪曲线（满意/中性/挫败）、痛点、机会点。覆盖从认知到留存的全流程，标注关键体验节点和改进优先级。",
            "tags": ["设计", "用户旅程", "UX"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "User Journey Map",
            "contentEn": "Based on the following product features, create a user journey map. List by stage: user goals, touchpoints, behaviors, emotion curve (satisfied/neutral/frustrated), pain points, and opportunities. Cover the full flow from awareness to retention, marking key experience nodes and improvement priorities.",
            "agentRole": "designer",
            "inputs": "产品功能和用户画像",
            "prerequisites": "已明确产品功能和目标用户",
            "outputFormat": "table",
            "qualityChecks": ["阶段是否完整", "情绪曲线是否合理", "痛点是否有依据", "机会点是否可执行"],
            "recommendedWith": ["task-design-review", "ctx-audience-general"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-design-review",
            "title": "设计评审报告",
            "content": "请对以下界面/产品进行设计评审。从6个维度评分（0-10分）：布局一致性、配色协调性、视觉层级、移动端适配、可访问性、交互流畅度。每个维度给出具体问题和改进建议，附优先级（P0/P1/P2）。",
            "tags": ["设计", "评审", "UI"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Design Review Report",
            "contentEn": "Conduct a design review of the following interface/product. Score across 6 dimensions (0-10): layout consistency, color harmony, visual hierarchy, mobile adaptation, accessibility, and interaction smoothness. Provide specific issues and improvement suggestions for each dimension, with priority (P0/P1/P2).",
            "agentRole": "designer",
            "inputs": "界面截图或代码链接",
            "prerequisites": "已有可审查的界面",
            "outputFormat": "report",
            "qualityChecks": ["评分是否有依据", "问题描述是否具体", "建议是否可执行", "优先级是否合理"],
            "recommendedWith": ["task-user-journey", "con-anti-ai-slop"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-accessibility-check",
            "title": "可访问性检查",
            "content": "请对以下界面进行可访问性检查。按WCAG 2.1 AA标准检查：颜色对比度（≥4.5:1）、键盘导航、焦点可见性、ARIA标签完整性、图片alt文本、表单标签关联、语义化HTML。输出问题清单和修复建议。",
            "tags": ["设计", "无障碍", "WCAG"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Accessibility Check",
            "contentEn": "Perform an accessibility check on the following interface following WCAG 2.1 AA standards: color contrast (≥4.5:1), keyboard navigation, focus visibility, ARIA label completeness, image alt text, form label association, and semantic HTML. Output issue list and fix recommendations.",
            "agentRole": "designer",
            "inputs": "HTML代码或界面描述",
            "prerequisites": "已有界面代码",
            "outputFormat": "checklist",
            "qualityChecks": ["是否覆盖WCAG核心项", "对比度是否量化", "修复建议是否具体", "是否有优先级"],
            "recommendedWith": ["task-design-review", "task-user-journey"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-design-system",
            "title": "设计规范提取",
            "content": "请从以下界面中提取设计规范。定义：主色/辅助色/中性色阶（附色值和命名）、字体层级（标题/正文/标注的字号字重行高）、间距系统（基准值和倍数）、圆角/阴影规范、组件规范（按钮/输入框/卡片）。输出可直接使用的CSS变量定义。",
            "tags": ["设计", "规范", "Design Token"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Design System Extraction",
            "contentEn": "Extract design specifications from the following interface. Define: primary/secondary/neutral color scales (with values and names), typography hierarchy (heading/body/caption sizes, weights, line heights), spacing system (base value and multipliers), border-radius/shadow specs, and component specs (button/input/card). Output ready-to-use CSS variable definitions.",
            "agentRole": "designer",
            "inputs": "界面代码或设计稿",
            "prerequisites": "已有完整界面",
            "outputFormat": "report",
            "qualityChecks": ["色彩是否成体系", "字号是否有层级", "间距是否有基准", "CSS变量是否可用"],
            "recommendedWith": ["task-design-review", "task-accessibility-check"]
        }
    },

    # ═══ 运营官补缺 (3个新增) ═══
    {
        "category": "task",
        "block": {
            "id": "task-content-calendar",
            "title": "内容日历",
            "content": "请根据以下产品节奏和目标，制定4周内容日历。每周一个主题，每天一条内容（含：发布平台、内容类型、标题方向、关键词、CTA）。确保内容类型多样化（教程/案例/互动/资讯），并标注与产品更新的联动节点。",
            "tags": ["运营", "内容", "日历"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Content Calendar",
            "contentEn": "Based on the following product rhythm and goals, create a 4-week content calendar. One theme per week, one content piece per day (including: platform, content type, title direction, keywords, CTA). Ensure content type diversity (tutorial/case/interactive/news), and mark nodes aligned with product updates.",
            "agentRole": "marketer",
            "inputs": "产品信息和运营目标",
            "prerequisites": "已明确运营目标和平台",
            "outputFormat": "table",
            "qualityChecks": ["主题是否连贯", "内容类型是否多样", "关键词是否覆盖", "与产品节奏是否联动"],
            "recommendedWith": ["task-write-article", "task-write-copy"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-seo-optimize",
            "title": "SEO优化",
            "content": "请对以下网页内容进行SEO优化。检查并改进：标题标签（≤60字符）、描述标签（≤160字符）、H1-H3层级、关键词密度（2-5%）、图片alt文本、内链结构、结构化数据（JSON-LD）、移动端友好性。输出优化前后的对比。",
            "tags": ["运营", "SEO", "优化"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "SEO Optimization",
            "contentEn": "Perform SEO optimization on the following web content. Check and improve: title tag (≤60 chars), meta description (≤160 chars), H1-H3 hierarchy, keyword density (2-5%), image alt text, internal link structure, structured data (JSON-LD), and mobile friendliness. Output before/after comparison.",
            "agentRole": "marketer",
            "inputs": "网页URL或HTML内容",
            "prerequisites": "已有网页内容",
            "outputFormat": "report",
            "qualityChecks": ["标题是否合规", "关键词密度是否合理", "结构化数据是否正确", "对比是否清晰"],
            "recommendedWith": ["task-content-calendar", "task-write-article"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-conversion-funnel",
            "title": "转化漏斗分析",
            "content": "请根据以下用户行为数据，进行转化漏斗分析。定义漏斗各阶段（曝光→点击→注册→激活→付费）、计算各阶段转化率和流失率、找出流失最大的环节、分析流失原因、给出优化建议（附预期提升幅度）。",
            "tags": ["运营", "转化", "漏斗"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Conversion Funnel Analysis",
            "contentEn": "Based on the following user behavior data, conduct conversion funnel analysis. Define funnel stages (exposure→click→register→activate→pay), calculate conversion rate and churn rate at each stage, identify the biggest drop-off point, analyze churn reasons, and provide optimization suggestions with expected improvement.",
            "agentRole": "marketer",
            "inputs": "用户行为数据和漏斗定义",
            "prerequisites": "已有行为数据",
            "outputFormat": "report",
            "qualityChecks": ["漏斗阶段是否合理", "转化率计算是否准确", "流失分析是否有依据", "优化建议是否可量化"],
            "recommendedWith": ["task-content-calendar", "task-metric-design"]
        }
    },

    # ═══ 程序员补缺 (2个新增) ═══
    {
        "category": "task",
        "block": {
            "id": "task-architecture-design",
            "title": "架构设计",
            "content": "请根据以下需求，设计系统架构。包含：架构图描述（模块划分和依赖关系）、技术选型（框架/数据库/中间件及理由）、数据模型设计（核心表结构和关系）、接口设计（RESTful API列表）、部署方案、扩展性和可维护性考量。",
            "tags": ["开发", "架构", "设计"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Architecture Design",
            "contentEn": "Based on the following requirements, design system architecture. Include: architecture diagram description (module division and dependencies), technology selection (framework/database/middleware with rationale), data model design (core table structures and relationships), API design (RESTful API list), deployment plan, and scalability/maintainability considerations.",
            "agentRole": "developer",
            "inputs": "需求文档和技术约束",
            "prerequisites": "已完成需求分析",
            "outputFormat": "report",
            "qualityChecks": ["模块划分是否合理", "技术选型是否有依据", "数据模型是否完整", "扩展性是否考虑"],
            "recommendedWith": ["task-code", "task-requirements-clarify"]
        }
    },
    {
        "category": "task",
        "block": {
            "id": "task-code-review",
            "title": "代码审查",
            "content": "请对以下代码进行审查。从5个维度评估：可读性（命名/注释/结构）、正确性（逻辑/边界/异常）、性能（时间复杂度/内存/数据库查询）、安全性（注入/XSS/权限）、可维护性（耦合度/扩展性）。每个问题标注严重程度（critical/major/minor）和修复建议。",
            "tags": ["开发", "审查", "质量"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Code Review",
            "contentEn": "Review the following code across 5 dimensions: readability (naming/comments/structure), correctness (logic/boundary/exceptions), performance (time complexity/memory/DB queries), security (injection/XSS/permissions), and maintainability (coupling/extensibility). Mark each issue with severity (critical/major/minor) and fix suggestions.",
            "agentRole": "developer",
            "inputs": "代码片段或文件",
            "prerequisites": "已有可审查的代码",
            "outputFormat": "report",
            "qualityChecks": ["5个维度是否都覆盖", "严重程度是否准确", "修复建议是否具体", "是否有遗漏的安全问题"],
            "recommendedWith": ["task-code", "task-architecture-design"]
        }
    },

    # ═══ v3.0已设计的2个积木（程序员生成但未入库）═══
    {
        "category": "task",
        "block": {
            "id": "task-requirements-clarify",
            "title": "需求澄清",
            "content": "你是一名严谨的需求分析师。请先理解用户目标，不要直接开始执行。围绕目标、用户、使用场景、输入资料、期望产出、优先级、限制条件和成功标准进行检查；区分已知事实、合理假设与待确认问题。若信息不足，列出不超过7个最关键的问题，并说明每个问题对结果的影响；若信息足够，整理成一份可执行的需求确认单，最后给出你的理解和仍存在的风险。",
            "tags": ["需求", "澄清", "前置条件", "工作流"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Requirements Clarification",
            "contentEn": "Act as a rigorous requirements analyst. Understand the user's goal before executing anything. Check the goal, users, use cases, available inputs, expected deliverables, priorities, constraints, and success criteria. Separate known facts, reasonable assumptions, and open questions. If information is missing, ask no more than seven critical questions and explain the impact of each. If the requirements are sufficient, produce an actionable requirements brief and state your understanding and remaining risks.",
            "agentRole": "pm",
            "inputs": "用户的任务描述和目标",
            "prerequisites": "用户已提出初始需求",
            "outputFormat": "report",
            "qualityChecks": ["是否区分了事实/假设/待确认", "问题是否不超过7个", "每个问题是否说明了影响", "需求确认单是否可执行"],
            "recommendedWith": ["task-prd", "con-acceptance-criteria"]
        }
    },
    {
        "category": "constraints",
        "block": {
            "id": "con-acceptance-criteria",
            "title": "验收标准",
            "content": "请将本次任务转化为可验证的验收标准，避免使用'高质量''尽可能完整'等模糊表述。先概括交付目标，再分别列出必备内容、格式要求、功能或逻辑要求、边界条件、禁止事项和通过条件；每条标准都应可观察、可检查，必要时提供示例或反例。输出完成后，对结果逐项核对，标记为通过、不通过或无法判断，并列出需要补充的信息。",
            "tags": ["验收", "质量门禁", "检查清单", "可验证"],
            "platforms": ["all"],
            "verified": "2026-10-08",
            "model": "GPT-4o+/Claude3.5/Step3+",
            "titleEn": "Acceptance Criteria",
            "contentEn": "Turn this task into verifiable acceptance criteria. Avoid vague phrases such as \"high quality\" or \"as complete as possible.\" Summarize the delivery goal, then define required content, format requirements, functional or logical requirements, edge cases, prohibitions, and pass conditions. Each criterion must be observable and testable, with examples or counterexamples where useful. After producing the result, check it item by item and mark each criterion as pass, fail, or undetermined, noting any missing information.",
            "agentRole": "pm",
            "inputs": "任务描述和交付目标",
            "prerequisites": "已明确任务目标",
            "outputFormat": "checklist",
            "qualityChecks": ["标准是否可观察可检查", "是否避免了模糊表述", "是否有边界条件", "通过条件是否明确"],
            "recommendedWith": ["task-requirements-clarify", "task-prd"]
        }
    },
]


def add_blocks():
    """批量添加新积木到blocks.json"""
    with open(BLOCKS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 收集现有积木id（防止重复）
    existing_ids = set()
    for cat in data['categories']:
        for b in cat.get('blocks', []):
            existing_ids.add(b['id'])

    added = 0
    skipped = 0
    role_stats = {}

    for item in NEW_BLOCKS:
        cat_id = item['category']
        block = item['block']
        bid = block['id']

        if bid in existing_ids:
            print(f'  ⏭️ 跳过（已存在）: {bid}')
            skipped += 1
            continue

        # 找到对应分类
        for cat in data['categories']:
            if cat['id'] == cat_id:
                cat['blocks'].append(block)
                existing_ids.add(bid)
                added += 1
                role = block.get('agentRole', 'general')
                role_stats[role] = role_stats.get(role, 0) + 1
                print(f'  ✅ 添加: {bid} ({block["title"]}) -> {cat_id} [role={role}]')
                break
        else:
            print(f'  ❌ 分类不存在: {cat_id} for {bid}')

    # 写回
    with open(BLOCKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'\n✅ 添加完成: +{added}个积木, 跳过{skipped}个已存在')
    print(f'总积木数: {len(existing_ids)}')
    print('\n新增积木角色分布:')
    for role, count in sorted(role_stats.items(), key=lambda x: -x[1]):
        print(f'  {role}: +{count}个')


if __name__ == '__main__':
    add_blocks()
