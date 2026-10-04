#!/usr/bin/env python3
"""
PromptBlocks MCP Server
提供积木浏览、搜索、推荐、拼装、冲突检测等工具，供 Claude Desktop / Cursor 等 AI 工具调用。
"""

import json
import os
import sys
from mcp.server.fastmcp import FastMCP

# 初始化
mcp = FastMCP("promptblocks")

# 加载 blocks.json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLOCKS_PATH = os.path.join(SCRIPT_DIR, "blocks.json")

def load_data():
    """加载 blocks.json 数据"""
    with open(BLOCKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_all_blocks(data):
    """展平所有积木为列表，附带 category 信息"""
    blocks = []
    for cat in data.get("categories", []):
        for b in cat.get("blocks", []):
            b["_category"] = cat["id"]
            b["_category_name"] = cat.get("name", "")
            b["_category_nameEn"] = cat.get("nameEn", "")
            blocks.append(b)
    return blocks

def find_block(data, block_id):
    """按 ID 查找单个积木"""
    for cat in data.get("categories", []):
        for b in cat.get("blocks", []):
            if b["id"] == block_id:
                return b, cat
    return None, None

# ─── Tool 1: get_categories ───
@mcp.tool()
def get_categories(lang: str = "zh") -> str:
    """列出所有积木分类（8个），包含每个分类的积木数量。
    
    Args:
        lang: 语言，"zh"=中文（默认），"en"=英文
    """
    data = load_data()
    result = []
    for cat in data.get("categories", []):
        name = cat.get("name") if lang == "zh" else cat.get("nameEn", cat.get("name"))
        result.append({
            "id": cat["id"],
            "name": name,
            "icon": cat.get("icon", ""),
            "block_count": len(cat.get("blocks", []))
        })
    return json.dumps({"categories": result, "total_categories": len(result)}, ensure_ascii=False)


# ─── Tool 2: get_blocks ───
@mcp.tool()
def get_blocks(category: str = "", platform: str = "", lang: str = "zh") -> str:
    """列出积木列表，可按分类和平台过滤。
    
    Args:
        category: 分类 ID（如 role/task/context/constraints/format/examples/industry/decision），留空=全部
        platform: 平台 ID（如 all/chatgpt/claude/stepfun/gemini/wenxin/tongyi），留空=全部
        lang: 语言，"zh"=中文（默认），"en"=英文
    """
    data = load_data()
    all_blocks = get_all_blocks(data)
    
    filtered = all_blocks
    if category:
        filtered = [b for b in filtered if b["_category"] == category]
    if platform:
        filtered = [b for b in filtered if platform in b.get("platforms", ["all"]) or "all" in b.get("platforms", ["all"])]
    
    result = []
    for b in filtered:
        title = b.get("title") if lang == "zh" else b.get("titleEn", b.get("title"))
        result.append({
            "id": b["id"],
            "title": title,
            "category": b["_category"],
            "tags": b.get("tags", []),
            "platforms": b.get("platforms", []),
            "verified": b.get("verified", ""),
            "model": b.get("model", "")
        })
    return json.dumps({"blocks": result, "total": len(result)}, ensure_ascii=False)


# ─── Tool 3: get_block ───
@mcp.tool()
def get_block(block_id: str, lang: str = "zh") -> str:
    """获取单个积木的完整内容。
    
    Args:
        block_id: 积木 ID（如 role-marketer, task-write-copy）
        lang: 语言，"zh"=中文（默认），"en"=英文
    """
    data = load_data()
    block, cat = find_block(data, block_id)
    if not block:
        return json.dumps({"error": f"Block not found: {block_id}"}, ensure_ascii=False)
    
    title = block.get("title") if lang == "zh" else block.get("titleEn", block.get("title"))
    content = block.get("content") if lang == "zh" else block.get("contentEn", block.get("content"))
    cat_name = cat.get("name") if lang == "zh" else cat.get("nameEn", cat.get("name"))
    
    return json.dumps({
        "id": block["id"],
        "title": title,
        "content": content,
        "category": cat["id"],
        "category_name": cat_name,
        "tags": block.get("tags", []),
        "platforms": block.get("platforms", []),
        "verified": block.get("verified", ""),
        "model": block.get("model", "")
    }, ensure_ascii=False)


# ─── Tool 4: search_blocks ───
@mcp.tool()
def search_blocks(query: str, lang: str = "zh") -> str:
    """按关键词搜索积木（匹配标题、标签、内容）。
    
    Args:
        query: 搜索关键词（如 "营销" "代码" "约束" "marketing"）
        lang: 语言，"zh"=中文（默认），"en"=英文
    """
    data = load_data()
    all_blocks = get_all_blocks(data)
    query_lower = query.lower()
    
    results = []
    for b in all_blocks:
        title = b.get("title", "") if lang == "zh" else b.get("titleEn", b.get("title", ""))
        content = b.get("content", "") if lang == "zh" else b.get("contentEn", b.get("content", ""))
        tags = b.get("tags", [])
        
        if query_lower in title.lower() or query_lower in content.lower() or any(query_lower in t.lower() for t in tags):
            results.append({
                "id": b["id"],
                "title": title,
                "category": b["_category"],
                "tags": tags,
                "platforms": b.get("platforms", []),
                "content_preview": content[:100] + "..." if len(content) > 100 else content
            })
    return json.dumps({"results": results, "total": len(results), "query": query}, ensure_ascii=False)


# ─── Tool 5: recommend_blocks ───
@mcp.tool()
def recommend_blocks(task_description: str, lang: str = "zh") -> str:
    """根据任务描述推荐合适的积木组合。会分析描述中的关键词，匹配角色、任务、约束、格式等分类的积木。
    
    Args:
        task_description: 你的任务描述（如 "帮我写一篇小红书种草文案" "审查这个合同条款"）
        lang: 语言，"zh"=中文（默认），"en"=英文
    """
    data = load_data()
    all_blocks = get_all_blocks(data)
    desc_lower = task_description.lower()
    
    # 关键词权重匹配
    scored = []
    for b in all_blocks:
        score = 0
        title = b.get("title", "") if lang == "zh" else b.get("titleEn", b.get("title", ""))
        content = b.get("content", "") if lang == "zh" else b.get("contentEn", b.get("content", ""))
        tags = b.get("tags", [])
        
        # 标题匹配权重最高
        for tag in tags:
            if tag.lower() in desc_lower:
                score += 3
        if title.lower() in desc_lower:
            score += 5
        for word in title.lower().split():
            if len(word) > 1 and word in desc_lower:
                score += 2
        for word in content.lower().split():
            if len(word) > 2 and word in desc_lower:
                score += 1
        
        if score > 0:
            scored.append({
                "id": b["id"],
                "title": title,
                "category": b["_category"],
                "tags": tags,
                "score": score,
                "reason": f"匹配关键词: {title}"
            })
    
    # 按分数排序，每个分类取 top 2
    scored.sort(key=lambda x: x["score"], reverse=True)
    
    # 确保每个分类至少有推荐
    recommended = []
    seen_categories = set()
    for s in scored:
        if s["category"] not in seen_categories or len([r for r in recommended if r["category"] == s["category"]]) < 2:
            recommended.append(s)
            seen_categories.add(s["category"])
    
    # 限制总数
    recommended = recommended[:15]
    
    return json.dumps({
        "task": task_description,
        "recommended_blocks": recommended,
        "total": len(recommended)
    }, ensure_ascii=False)


# ─── Tool 6: assemble_prompt ───
@mcp.tool()
def assemble_prompt(block_ids: list, lang: str = "zh") -> str:
    """将指定积木拼装成完整的 Prompt。
    
    Args:
        block_ids: 积木 ID 列表（如 ["role-marketer", "task-write-copy", "con-style-casual"]）
        lang: 语言，"zh"=中文（默认），"en"=英文
    """
    data = load_data()
    parts = []
    missing = []
    
    for bid in block_ids:
        block, cat = find_block(data, bid)
        if not block:
            missing.append(bid)
            continue
        content = block.get("content") if lang == "zh" else block.get("contentEn", block.get("content"))
        title = block.get("title") if lang == "zh" else block.get("titleEn", block.get("title"))
        parts.append({
            "block_id": bid,
            "title": title,
            "category": cat["id"],
            "content": content
        })
    
    # 拼装 Prompt
    prompt_parts = []
    for p in parts:
        prompt_parts.append(p["content"])
    assembled = "\n\n".join(prompt_parts)
    
    # 冲突检测
    conflicts = check_conflicts_internal(data, block_ids)
    
    return json.dumps({
        "assembled_prompt": assembled,
        "blocks_used": [{"id": p["block_id"], "title": p["title"], "category": p["category"]} for p in parts],
        "missing_blocks": missing,
        "conflicts": conflicts,
        "total_blocks": len(parts)
    }, ensure_ascii=False)


# ─── Tool 7: get_presets ───
@mcp.tool()
def get_presets(lang: str = "zh") -> str:
    """列出所有预设模板（10个），每个预设包含一组预选积木。
    
    Args:
        lang: 语言，"zh"=中文（默认），"en"=英文
    """
    data = load_data()
    result = []
    for p in data.get("presets", []):
        name = p.get("name") if lang == "zh" else p.get("nameEn", p.get("name"))
        result.append({
            "id": p["id"],
            "name": name,
            "block_ids": p.get("blocks", []),
            "block_count": len(p.get("blocks", []))
        })
    return json.dumps({"presets": result, "total": len(result)}, ensure_ascii=False)


# ─── Tool 8: get_preset ───
@mcp.tool()
def get_preset(preset_id: str, lang: str = "zh") -> str:
    """获取单个预设模板的详细信息（含积木展开内容和拼装好的 Prompt）。
    
    Args:
        preset_id: 预设 ID（如 preset-xhs, preset-code, preset-contract）
        lang: 语言，"zh"=中文（默认），"en"=英文
    """
    data = load_data()
    preset = None
    for p in data.get("presets", []):
        if p["id"] == preset_id:
            preset = p
            break
    if not preset:
        return json.dumps({"error": f"Preset not found: {preset_id}"}, ensure_ascii=False)
    
    # 展开积木
    blocks_detail = []
    prompt_parts = []
    for bid in preset.get("blocks", []):
        block, cat = find_block(data, bid)
        if block:
            content = block.get("content") if lang == "zh" else block.get("contentEn", block.get("content"))
            title = block.get("title") if lang == "zh" else block.get("titleEn", block.get("title"))
            blocks_detail.append({
                "id": block["id"],
                "title": title,
                "category": cat["id"],
                "content": content
            })
            prompt_parts.append(content)
    
    name = preset.get("name") if lang == "zh" else preset.get("nameEn", preset.get("name"))
    return json.dumps({
        "id": preset["id"],
        "name": name,
        "blocks": blocks_detail,
        "assembled_prompt": "\n\n".join(prompt_parts),
        "block_count": len(blocks_detail)
    }, ensure_ascii=False)


# ─── Tool 9: check_conflicts ───
def check_conflicts_internal(data, block_ids):
    """内部冲突检测函数"""
    conflicts = []
    for pair in data.get("conflictPairs", []):
        a_id = pair["a"]
        b_id = pair["b"]
        if a_id in block_ids and b_id in block_ids:
            conflicts.append({
                "block_a": a_id,
                "block_b": b_id,
                "reason": pair.get("reason", "")
            })
    return conflicts

@mcp.tool()
def check_conflicts(block_ids: list) -> str:
    """检测指定积木组合是否存在冲突（7组冲突规则）。
    
    Args:
        block_ids: 积木 ID 列表（如 ["con-short", "con-long", "con-style-professional"]）
    """
    data = load_data()
    conflicts = check_conflicts_internal(data, block_ids)
    return json.dumps({
        "block_ids": block_ids,
        "conflicts": conflicts,
        "has_conflicts": len(conflicts) > 0,
        "conflict_count": len(conflicts)
    }, ensure_ascii=False)


# ─── 启动 ───
if __name__ == "__main__":
    mcp.run()
