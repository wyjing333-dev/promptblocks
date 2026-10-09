"""
PromptBlocks 新增积木脚本 - 2026-10-09
新增2个积木，从116→118：
1. task-skill-export (task分类, role=developer) - 将Prompt打包导出为标准技能文件
2. task-competitor-monitor (task分类, role=researcher) - 竞品动态监控与变化追踪
"""
import json
import copy
from datetime import datetime

BLOCKS_PATH = r'D:\jieyuexingchen\promptblocks\blocks.json'

# 读取现有数据
with open(BLOCKS_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 找到task分类
task_cat = None
for c in data['categories']:
    if c['id'] == 'task':
        task_cat = c
        break

if not task_cat:
    print("ERROR: task category not found!")
    exit(1)

# 检查是否已存在
existing_ids = {b['id'] for b in task_cat['blocks']}
print(f"当前task分类积木数: {len(task_cat['blocks'])}")
print(f"已有ID检查: task-skill-export={'task-skill-export' in existing_ids}, task-competitor-monitor={'task-competitor-monitor' in existing_ids}")

# 新积木1: task-skill-export
skill_export = {
    "id": "task-skill-export",
    "title": "技能打包导出",
    "content": "请将以下Prompt内容打包为标准技能文件，输出为YAML格式，包含以下字段：name（技能名称）、description（技能描述）、version（版本号）、author（作者）、trigger（触发条件）、prompt（完整Prompt内容）、inputs（输入参数定义）、outputs（输出格式定义）、tags（标签列表）。确保输出的技能文件可以直接放入Claude Code、Cursor、Codex等AI编码工具的.agents目录使用。",
    "tags": ["技能导出", "分发", "YAML", "Agent"],
    "platforms": ["all"],
    "verified": "2026-10-09",
    "model": "GPT-4o+/Claude3.5/Step3+",
    "titleEn": "Skill Package Export",
    "contentEn": "Please package the following Prompt content into a standard skill file in YAML format, including these fields: name, description, version, author, trigger, prompt (full prompt content), inputs (input parameter definitions), outputs (output format definitions), tags. Ensure the output skill file can be directly placed into the .agents directory of AI coding tools such as Claude Code, Cursor, and Codex.",
    "agentRole": "developer",
    "inputs": "已拼装完成的Prompt内容和技能元信息",
    "prerequisites": "用户已完成Prompt拼装",
    "outputFormat": "yaml",
    "qualityChecks": [
        "YAML格式是否合法可解析",
        "是否包含所有必需字段",
        "prompt字段是否完整保留了原始Prompt内容",
        "inputs和outputs定义是否清晰可执行",
        "是否适配主流AI Agent工具的技能格式"
    ],
    "recommendedWith": ["fmt-template", "con-step-by-step"]
}

# 新积木2: task-competitor-monitor
competitor_monitor = {
    "id": "task-competitor-monitor",
    "content": "请针对以下竞品列表进行动态监控分析：1.收集各竞品最近一周的产品更新、功能变化、定价调整、融资新闻；2.按更新重要性分级（重大更新/常规迭代/小修补）；3.对比分析竞品动态与我们的产品差异，指出我们有哪些功能已被竞品追赶或超越；4.输出竞品动态监控报告，包含变化时间线、差异化分析、应对建议三个部分。重点关注：GitHub仓库的Star/Fork/Issue变化、产品页面功能列表变化、社交媒体声量变化。",
    "title": "竞品动态监控",
    "tags": ["竞品分析", "监控", "差异化"],
    "platforms": ["all"],
    "verified": "2026-10-09",
    "model": "GPT-4o+/Claude3.5/Step3+",
    "titleEn": "Competitor Monitoring",
    "contentEn": "Please conduct a dynamic monitoring analysis for the following competitor list: 1. Collect each competitor's product updates, feature changes, pricing adjustments, and funding news from the past week; 2. Rank updates by importance (major update / routine iteration / minor fix); 3. Compare and analyze the differences between competitor dynamics and our product, identifying features where competitors have caught up or surpassed us; 4. Output a competitor monitoring report with three sections: change timeline, differentiation analysis, and response recommendations. Focus on: GitHub repo Star/Fork/Issue changes, product page feature list changes, social media mention volume changes.",
    "agentRole": "researcher",
    "inputs": "竞品名称列表和监控维度",
    "prerequisites": "用户已确定竞品列表和关注维度",
    "outputFormat": "markdown",
    "qualityChecks": [
        "是否覆盖了所有竞品的最新动态",
        "更新重要性分级是否合理",
        "差异化分析是否客观准确",
        "应对建议是否可执行",
        "是否有数据来源支撑分析结论"
    ],
    "recommendedWith": ["task-search-plan", "task-evidence-citation"]
}

# 添加积木
new_blocks = [skill_export, competitor_monitor]
for nb in new_blocks:
    if nb['id'] not in existing_ids:
        task_cat['blocks'].append(nb)
        print(f"✅ 新增: {nb['id']} - {nb['title']}")
    else:
        print(f"⚠️ 已存在: {nb['id']}")

# 统计总数
total = sum(len(c.get('blocks', [])) for c in data['categories'])
print(f"\n积木总数: {total}")

# 保存
with open(BLOCKS_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"\n✅ 已保存到 {BLOCKS_PATH}")
