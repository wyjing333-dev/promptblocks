# -*- coding: utf-8 -*-
"""Add 2 new blocks from GitHub Trending 2026-10-07:
1. con-adhd-output (约束类) - from ayghri/i-have-adhd (54k stars, +326 today)
   Core idea: Stop burying the answer. ADHD-friendly output. BLUF (Bottom Line Up Front).
2. role-growth-hacker (角色类) - from msitarzewski/agency-agents (158k stars, +623 today)
   Core idea: A complete AI agency - Growth hacker specializing in rapid experimentation
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
blocks_path = os.path.join(BASE, "blocks.json")

with open(blocks_path, "r", encoding="utf-8") as f:
    data = json.load(f)

categories = data.get("categories", [])

# Find category indices
cat_map = {c["id"]: i for i, c in enumerate(categories)}
print("Categories:", list(cat_map.keys()))

# --- Block 1: con-adhd-output (约束类) ---
adhd_block = {
    "id": "con-adhd-output",
    "title": "ADHD友好输出",
    "content": "所有输出遵循BLUF原则（Bottom Line Up Front）：第一句直接给出结论或答案，绝不埋在段落深处。规则：1.第一行就是最终结论，不写\"让我来分析\"\"首先我们需要\"等前缀；2.关键发现用**粗体**标注，让扫读即可抓住重点；3.每段不超过3个逻辑层级，超了就拆段；4.所有输出末尾附TL;DR一行，10个字以内总结核心答案；5.如果回答有多个部分，开头先列一句话目录（如：1.结论 2.理由 3.方案），再展开。核心理念：读者注意力有限，把最重要的信息放在最前面。",
    "tags": ["结论先行", "BLUF", "不埋答案", "精简输出", "注意力友好"],
    "platforms": ["chatgpt", "claude", "stepfun", "gemini", "wenxin", "tongyi"],
    "verified": "2026-10-07",
    "model": "GPT-4o+/Claude3.5/Step3+/Gemini2.0",
    "titleEn": "ADHD-Friendly Output",
    "contentEn": "All output follows BLUF (Bottom Line Up Front): the very first sentence gives the conclusion or answer, never buried in paragraphs. Rules: 1. First line is the final conclusion, no \"Let me analyze\" or \"First we need to\" preamble; 2. Key findings in **bold** for scanning; 3. Max 3 logical levels per paragraph, split if exceeded; 4. End every response with a TL;DR line, 10 words or less; 5. If multi-part, start with a one-line table of contents (e.g., 1.Answer 2.Reasoning 3.Plan) before expanding. Core: reader attention is finite, put the most important information first."
}

# --- Block 2: role-growth-hacker (角色类) ---
growth_block = {
    "id": "role-growth-hacker",
    "title": "增长黑客",
    "content": "你是一位增长黑客，专注于通过数据驱动的快速实验实现用户增长。你的思维方式：1.永远从数据出发，不凭直觉做判断，每个决策都有指标支撑；2.构建增长漏斗（获客→激活→留存→推荐→变现），找出最弱环节集中突破；3.设计A/B测试，一次只改一个变量，最小样本1000用户，统计显著性p<0.05才算有效；4.寻找病毒传播系数K>1的增长循环，设计自传播机制（邀请奖励/内容裂变/社交货币）；5.关注北极星指标（NSM），所有实验都指向提升NSM。输出格式：增长实验方案（假设/变量/样本/周期/指标/预期效果）、转化漏斗分析（各环节转化率/流失原因/优化建议）、渠道评估矩阵（成本/速度/规模/质量四维评分）。",
    "tags": ["增长黑客", "A/B测试", "转化漏斗", "数据驱动", "病毒传播"],
    "platforms": ["chatgpt", "claude", "stepfun", "gemini", "wenxin", "tongyi"],
    "verified": "2026-10-07",
    "model": "GPT-4o+/Claude3.5/Step3+/Gemini2.0",
    "titleEn": "Growth Hacker",
    "contentEn": "You are a Growth Hacker, focused on achieving user growth through data-driven rapid experimentation. Mindset: 1. Always start from data, no gut-feel decisions, every choice backed by metrics; 2. Build the growth funnel (Acquire > Activate > Retain > Refer > Monetize), find the weakest link and concentrate; 3. Design A/B tests, change one variable at a time, minimum 1000 users, statistical significance p<0.05; 4. Seek viral coefficient K>1 growth loops, design self-propagation mechanisms (referral rewards / content virality / social currency); 5. Focus on North Star Metric (NSM), all experiments aim to lift NSM. Output: Growth experiment plans (hypothesis/variable/sample/duration/metric/expected lift), funnel analysis (step conversion rates / churn reasons / optimization), channel matrix (cost/speed/scale/quality 4D scoring)."
}

# Add blocks to their categories
added = 0

# Add adhd_block to constraints category
if "constraints" in cat_map:
    idx = cat_map["constraints"]
    existing_ids = [b["id"] for b in categories[idx]["blocks"]]
    if adhd_block["id"] not in existing_ids:
        categories[idx]["blocks"].append(adhd_block)
        added += 1
        print(f"Added {adhd_block['id']} to constraints (now {len(categories[idx]['blocks'])} blocks)")
    else:
        print(f"{adhd_block['id']} already exists in constraints")

# Add growth_block to role category
if "role" in cat_map:
    idx = cat_map["role"]
    existing_ids = [b["id"] for b in categories[idx]["blocks"]]
    if growth_block["id"] not in existing_ids:
        categories[idx]["blocks"].append(growth_block)
        added += 1
        print(f"Added {growth_block['id']} to role (now {len(categories[idx]['blocks'])} blocks)")
    else:
        print(f"{growth_block['id']} already exists in role")

# Count total blocks
total = sum(len(c["blocks"]) for c in categories)
print(f"\nTotal blocks: {total} (was 80, added {added})")

if added > 0:
    with open(blocks_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("blocks.json saved successfully!")
else:
    print("No changes made.")
